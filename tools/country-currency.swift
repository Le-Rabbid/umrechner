// Code geschrieben von Claude (KI-Modell von Anthropic), siehe README.md.
import Foundation

// Gibt für jedes Land (ISO-Code) die Landeswährung als JSON aus, z. B. {"CH":"CHF","DE":"EUR",…}.
var result: [String: String] = [:]
for region in Locale.Region.isoRegions where region.identifier.count == 2 {
    let identifier = Locale.identifier(fromComponents: [NSLocale.Key.countryCode.rawValue: region.identifier])
    if let currency = Locale(identifier: identifier).currency?.identifier {
        result[region.identifier] = currency
    }
}
let data = try JSONSerialization.data(withJSONObject: result, options: [.sortedKeys])
print(String(decoding: data, as: UTF8.self))
