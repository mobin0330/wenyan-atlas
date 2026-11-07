import Foundation
import Vision
struct Row: Codable { let text:String; let confidence:Float; let x:Double; let y:Double; let w:Double; let h:Double }
struct Output: Codable { let file:String; let rows:[Row] }
for path in CommandLine.arguments.dropFirst() {
 do {
  let req = VNRecognizeTextRequest()
  req.recognitionLevel = .accurate
  req.recognitionLanguages = ["zh-Hans", "en-US"]
  req.usesLanguageCorrection = false
  let handler = VNImageRequestHandler(url: URL(fileURLWithPath:path), options: [:])
  try handler.perform([req])
  var rows:[Row]=[]
  for r in req.results ?? [] {
   guard let c=r.topCandidates(1).first else {continue}
   let bb=r.boundingBox
   rows.append(Row(text:c.string,confidence:c.confidence,x:bb.minX,y:bb.minY,w:bb.width,h:bb.height))
  }
  let data=try JSONEncoder().encode(Output(file:path,rows:rows))
  print(String(data:data,encoding:.utf8)!)
 } catch { fputs("OCR error: \(error)\n",stderr) }
}
