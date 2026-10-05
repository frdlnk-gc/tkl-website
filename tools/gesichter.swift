// Gesichter + Köpfe erkennen: swift gesichter.swift bild1.webp ...
// -> JSON {datei: [[x,y,w,h], ...]} Kopfbereiche als Anteile (Ursprung oben links)
import Foundation
import Vision
import AppKit
var out: [String: [[Double]]] = [:]
func r3(_ v: CGFloat) -> Double { (Double(v) * 1000).rounded() / 1000 }
for p in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: p), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
  let f = VNDetectFaceRectanglesRequest()
  let m = VNDetectHumanRectanglesRequest(); m.upperBodyOnly = false
  try? VNImageRequestHandler(cgImage: cg).perform([f, m])
  var boxen: [[Double]] = (f.results ?? []).filter { $0.confidence > 0.5 }.map { r in
    let b = r.boundingBox; return [r3(b.minX), r3(1 - b.maxY), r3(b.width), r3(b.height)] }
  for h in (m.results ?? []) where h.confidence > 0.4 {
    let b = h.boundingBox  // Kopf ≈ oberes Fünftel der Person
    let kh = b.height * 0.2
    boxen.append([r3(b.minX + b.width * 0.2), r3(1 - b.maxY), r3(b.width * 0.6), r3(kh)])
  }
  out[(p as NSString).lastPathComponent] = boxen
}
print(String(data: try! JSONSerialization.data(withJSONObject: out, options: [.sortedKeys]), encoding: .utf8)!)
