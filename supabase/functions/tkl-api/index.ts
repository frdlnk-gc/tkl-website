// TKL Website-API (Supabase Edge Function, verify_jwt = false – eigene Anmeldung).
// Öffentlich:  POST /lead (Kundenanfrage/Bewerbung), POST /track (Seitenaufruf, ohne Cookies)
// Geschützt:   POST /login, GET /me, GET /leads, PATCH /leads/:id, GET /stats, POST /demo-loeschen
// Zugriff auf die Tabellen nur hier mit Service-Role (RLS ist an, keine Policies).
import { createClient } from "npm:@supabase/supabase-js@2";

const SB_URL = Deno.env.get("SUPABASE_URL")!;
const SB_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const db = createClient(SB_URL, SB_KEY, { auth: { persistSession: false } });

const ERLAUBT = [/^https:\/\/tkl\.greenfield-digital\.de$/, /^https:\/\/(www\.)?tkl\.gmbh$/, /^https:\/\/frdlnk-gc\.github\.io$/, /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/];
const enc = new TextEncoder();

function cors(origin: string | null) {
  const ok = origin && ERLAUBT.some((r) => r.test(origin));
  return {
    "Access-Control-Allow-Origin": ok ? origin! : "https://tkl.greenfield-digital.de",
    "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
    "Access-Control-Allow-Headers": "content-type,authorization",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}
const json = (o: unknown, status: number, h: Record<string, string>) =>
  new Response(JSON.stringify(o), { status, headers: { ...h, "content-type": "application/json; charset=utf-8" } });

const b64u = (b: ArrayBuffer | Uint8Array) =>
  btoa(String.fromCharCode(...new Uint8Array(b instanceof Uint8Array ? b : new Uint8Array(b)))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const hex = (b: ArrayBuffer) => [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");

let hmacKey: CryptoKey | null = null;
async function signKey() {
  if (!hmacKey) {
    const raw = await crypto.subtle.digest("SHA-256", enc.encode(SB_KEY + "|tkl-sitzung-v1"));
    hmacKey = await crypto.subtle.importKey("raw", raw, { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
  }
  return hmacKey;
}
async function tokenErstellen(uid: string, name: string) {
  const body = b64u(enc.encode(JSON.stringify({ uid, name, exp: Date.now() + 12 * 3600e3 })));
  const sig = b64u(await crypto.subtle.sign("HMAC", await signKey(), enc.encode(body)));
  return body + "." + sig;
}
async function tokenPruefen(req: Request): Promise<{ uid: string; name: string } | null> {
  const t = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  const [body, sig] = t.split(".");
  if (!body || !sig) return null;
  const sigBytes = Uint8Array.from(atob(sig.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0));
  const ok = await crypto.subtle.verify("HMAC", await signKey(), sigBytes, enc.encode(body));
  if (!ok) return null;
  const p = JSON.parse(atob(body.replace(/-/g, "+").replace(/_/g, "/")));
  if (p.exp < Date.now()) return null;
  return { uid: p.uid, name: p.name };
}
async function pbkdf2(pw: string, saltHex: string) {
  const salt = Uint8Array.from(saltHex.match(/.{2}/g)!.map((h) => parseInt(h, 16)));
  const k = await crypto.subtle.importKey("raw", enc.encode(pw), "PBKDF2", false, ["deriveBits"]);
  return hex(await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt, iterations: 210000 }, k, 256));
}
const gleich = (a: string, b: string) => a.length === b.length && [...a].reduce((d, c, i) => d | (c.charCodeAt(0) ^ b.charCodeAt(i)), 0) === 0;

const s = (v: unknown, max = 300) => (typeof v === "string" ? v.trim().slice(0, max) : "") || null;
const BOT = /bot|crawl|spider|slurp|facebookexternalhit|preview|headless|lighthouse|pingdom|uptime/i;

Deno.serve(async (req) => {
  const h = cors(req.headers.get("origin"));
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
  const url = new URL(req.url);
  const pfad = url.pathname.replace(/^.*\/tkl-api/, "") || "/";

  try {
    // ---------- öffentlich ----------
    if (req.method === "POST" && pfad === "/track") {
      const b = await req.json().catch(() => ({}));
      const ua = req.headers.get("user-agent") || "";
      if (BOT.test(ua) || !s(b.pfad, 200)) return new Response(null, { status: 204, headers: h });
      // Besucher-Kennung ohne Cookies/Speicher: Tages-Hash aus IP + Browser, nicht rückrechenbar
      const ip = req.headers.get("x-forwarded-for")?.split(",")[0].trim() || "";
      const sid = hex(await crypto.subtle.digest("SHA-256", enc.encode(ip + "|" + ua + "|" + new Date().toISOString().slice(0, 10) + "|" + SB_KEY.slice(-12)))).slice(0, 20);
      await db.from("tkl_events").insert({
        sid, typ: ["view", "cta", "funnel_start"].includes(b.typ) ? b.typ : "view",
        pfad: s(b.pfad, 200), ref: s(b.ref, 200), quelle: s(b.quelle, 60), geraet: /mobile|iphone|android/i.test(ua) ? "mobil" : "desktop",
      });
      return new Response(null, { status: 204, headers: h });
    }

    if (req.method === "POST" && pfad === "/lead") {
      const b = await req.json().catch(() => null);
      if (!b) return json({ fehler: "Ungültige Anfrage" }, 400, h);
      if (b.website || (typeof b.dauer === "number" && b.dauer < 2500)) return json({ ok: true }, 200, h); // Honigtopf / zu schnell
      const typ = b.typ === "bewerbung" ? "bewerbung" : b.typ === "anfrage" ? "anfrage" : null;
      const name = s(b.name, 120);
      if (!typ || !name) return json({ fehler: "Bitte Namen angeben." }, 400, h);
      const email = s(b.email, 160), telefon = s(b.telefon, 60);
      if (!email && !telefon) return json({ fehler: "Bitte Telefon oder E-Mail angeben." }, 400, h);
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ fehler: "Bitte E-Mail-Adresse prüfen." }, 400, h);
      if (b.datenschutz !== true) return json({ fehler: "Bitte der Datenschutzerklärung zustimmen." }, 400, h);
      const ip = req.headers.get("x-forwarded-for")?.split(",")[0].trim() || "";
      const ipHash = ip ? hex(await crypto.subtle.digest("SHA-256", enc.encode(ip + new Date().toISOString().slice(0, 10)))).slice(0, 24) : null;
      if (ipHash) {
        const { count } = await db.from("tkl_leads").select("id", { count: "exact", head: true }).eq("ip_hash", ipHash).gte("created_at", new Date(Date.now() - 600e3).toISOString());
        if ((count ?? 0) >= 5) return json({ fehler: "Zu viele Anfragen – bitte später erneut versuchen oder anrufen." }, 429, h);
      }
      const daten: Record<string, unknown> = {};
      if (b.daten && typeof b.daten === "object") for (const [k, v] of Object.entries(b.daten).slice(0, 30)) daten[s(k, 40) || "x"] = Array.isArray(v) ? v.slice(0, 12).map((x) => s(x, 120)) : s(v, 600);
      const { error } = await db.from("tkl_leads").insert({
        typ, name, email, telefon, firma: s(b.firma, 160), ort: s(b.ort, 120), nachricht: s(b.nachricht, 3000),
        daten, quelle: s(b.quelle, 200), utm: b.utm && typeof b.utm === "object" ? b.utm : null, ip_hash: ipHash,
      });
      if (error) throw error;
      return json({ ok: true }, 200, h);
    }

    if (req.method === "POST" && pfad === "/login") {
      const b = await req.json().catch(() => ({}));
      const email = (s(b.email, 160) || "").toLowerCase();
      const { data: u } = await db.from("tkl_users").select("*").eq("email", email).eq("aktiv", true).maybeSingle();
      await new Promise((r) => setTimeout(r, 350));
      if (!u || !gleich(await pbkdf2(String(b.passwort || ""), u.pw_salt), u.pw_hash)) return json({ fehler: "E-Mail oder Passwort stimmt nicht." }, 401, h);
      await db.from("tkl_users").update({ last_login: new Date().toISOString() }).eq("id", u.id);
      return json({ token: await tokenErstellen(u.id, u.name), name: u.name }, 200, h);
    }

    // ---------- geschützt ----------
    const nutzer = await tokenPruefen(req);
    if (!nutzer) return json({ fehler: "Bitte neu anmelden." }, 401, h);

    if (req.method === "GET" && pfad === "/me") return json(nutzer, 200, h);

    if (req.method === "GET" && pfad === "/leads") {
      let q = db.from("tkl_leads").select("id,created_at,updated_at,typ,status,name,firma,email,telefon,ort,nachricht,daten,notizen,quelle,utm,demo").order("created_at", { ascending: false }).limit(500);
      const typ = url.searchParams.get("typ");
      if (typ) q = q.eq("typ", typ);
      const { data, error } = await q;
      if (error) throw error;
      return json(data, 200, h);
    }

    const m = pfad.match(/^\/leads\/([0-9a-f-]{36})$/);
    if (req.method === "PATCH" && m) {
      const b = await req.json().catch(() => ({}));
      const { data: alt } = await db.from("tkl_leads").select("notizen,status").eq("id", m[1]).single();
      if (!alt) return json({ fehler: "Nicht gefunden" }, 404, h);
      const upd: Record<string, unknown> = { updated_at: new Date().toISOString() };
      const notizen = [...(alt.notizen || [])];
      const STATUS = ["neu", "kontaktiert", "termin", "angebot", "gewonnen", "eingestellt", "abgesagt", "archiviert"];
      if (b.status && STATUS.includes(b.status) && b.status !== alt.status) {
        upd.status = b.status;
        notizen.push({ t: new Date().toISOString(), von: nutzer.name, text: `Status: ${alt.status} → ${b.status}`, system: true });
      }
      if (s(b.notiz, 2000)) notizen.push({ t: new Date().toISOString(), von: nutzer.name, text: s(b.notiz, 2000) });
      upd.notizen = notizen;
      const { data, error } = await db.from("tkl_leads").update(upd).eq("id", m[1]).select().single();
      if (error) throw error;
      return json(data, 200, h);
    }

    if (req.method === "GET" && pfad === "/stats") {
      const tage = Math.min(365, Math.max(7, parseInt(url.searchParams.get("tage") || "30")));
      const { data, error } = await db.rpc("tkl_stats", { tage });
      if (error) throw error;
      return json(data, 200, h);
    }

    if (req.method === "POST" && pfad === "/demo-loeschen") {
      await db.from("tkl_leads").delete().eq("demo", true);
      await db.from("tkl_events").delete().eq("demo", true);
      return json({ ok: true }, 200, h);
    }

    return json({ fehler: "Unbekannter Pfad" }, 404, h);
  } catch (e) {
    console.error(e);
    return json({ fehler: "Serverfehler – bitte später erneut versuchen." }, 500, h);
  }
});
