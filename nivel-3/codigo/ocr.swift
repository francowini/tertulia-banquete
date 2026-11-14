// ocr.swift — OCR 100% local (offline) con Apple Vision (VNRecognizeTextRequest).
// Ninguna imagen sale de la computadora: no hay red ni IA externa.
//
// Uso:  swift nivel-3/codigo/ocr.swift [--out DIR] img1.jpg [img2.jpg ...]
//   - Escribe DIR/<nombre>.txt por imagen (si --out), o imprime a stdout.
//   - Cada línea reconocida sale ordenada por posición (arriba->abajo, izq->der),
//     agrupada en FILAS (observaciones con centro vertical parecido) para
//     reconstruir renglones de tabla. Formato de cada fila:
//        y=0.123 | [x=0.05] texto1 | [x=0.40] texto2 | ...
//     (coordenadas normalizadas 0..1, origen arriba-izquierda; conf = confianza)
//   - Config: recognitionLevel .accurate, idiomas es-ES/en-US,
//     usesLanguageCorrection = false (no "corrige" números ni códigos).
import Foundation
import Vision
import AppKit

struct Obs { let text: String; let x: Double; let y: Double; let h: Double; let conf: Float }

func ocr(_ path: String) -> [Obs] {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("no se pudo abrir \(path)\n".data(using: .utf8)!); return []
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["es-ES", "en-US"]
    req.usesLanguageCorrection = false
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try? handler.perform([req])
    var out: [Obs] = []
    for o in req.results ?? [] {
        guard let c = o.topCandidates(1).first else { continue }
        let b = o.boundingBox  // origen abajo-izquierda
        out.append(Obs(text: c.string, x: Double(b.minX), y: Double(1 - b.midY), h: Double(b.height), conf: c.confidence))
    }
    return out
}

func rows(_ obs: [Obs]) -> String {
    let s = obs.sorted { $0.y < $1.y }
    var groups: [[Obs]] = []
    for o in s {
        if var last = groups.last, let ref = last.first,
           abs(o.y - (last.map { $0.y }.reduce(0, +) / Double(last.count))) < max(ref.h, o.h) * 0.5 {
            last.append(o); groups[groups.count - 1] = last
        } else { groups.append([o]) }
    }
    var lines: [String] = []
    for g in groups {
        let y = g.map { $0.y }.reduce(0, +) / Double(g.count)
        let cells = g.sorted { $0.x < $1.x }.map { String(format: "[x=%.2f c=%.2f] ", $0.x, $0.conf) + $0.text }
        lines.append(String(format: "y=%.3f | ", y) + cells.joined(separator: " | "))
    }
    return lines.joined(separator: "\n") + "\n"
}

var args = Array(CommandLine.arguments.dropFirst())
var outDir: String? = nil
if let i = args.firstIndex(of: "--out"), i + 1 < args.count { outDir = args[i + 1]; args.removeSubrange(i...(i + 1)) }
for p in args {
    let txt = rows(ocr(p))
    if let d = outDir {
        let name = ((p as NSString).lastPathComponent as NSString).deletingPathExtension
        try? txt.write(toFile: "\(d)/\(name).txt", atomically: true, encoding: .utf8)
        print("ok \(name)")
    } else { print("=== \(p)"); print(txt) }
}
