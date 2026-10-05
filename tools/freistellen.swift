// Stellt Personen/Objekte per Apple Vision frei: swift freistellen.swift in.jpg out.png [maxKante]
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
let inURL = URL(fileURLWithPath: args[1]); let outURL = URL(fileURLWithPath: args[2])
let maxEdge = args.count > 3 ? Double(args[3])! : 1600
guard var ci = CIImage(contentsOf: inURL, options: [.applyOrientationProperty: true]) else { print("lesen fehlgeschlagen"); exit(1) }
let s = min(1.0, maxEdge / max(ci.extent.width, ci.extent.height))
ci = ci.transformed(by: CGAffineTransform(scaleX: s, y: s))
let ctx = CIContext()
let cg = ctx.createCGImage(ci, from: ci.extent)!
let req = VNGenerateForegroundInstanceMaskRequest()
let h = VNImageRequestHandler(cgImage: cg)
try h.perform([req])
guard let r = req.results?.first else { print("kein Motiv"); exit(2) }
let buf = try r.generateMaskedImage(ofInstances: r.allInstances, from: h, croppedToInstancesExtent: true)
let out = CIImage(cvPixelBuffer: buf)
let rep = NSBitmapImageRep(cgImage: ctx.createCGImage(out, from: out.extent)!)
try rep.representation(using: .png, properties: [:])!.write(to: outURL)
print("ok", Int(out.extent.width), Int(out.extent.height), r.allInstances.count)
