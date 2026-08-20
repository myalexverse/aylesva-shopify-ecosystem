import Foundation

enum ProductStatus: String, Codable, CaseIterable {
    case pending = "PENDING"
    case approved = "APPROVED"
    case rejected = "REJECTED"
    
    var label: String {
        switch self {
        case .pending: return "Pendiente"
        case .approved: return "Aprobado"
        case .rejected: return "Rechazado"
        }
    }
}

struct ArtisanProduct: Codable, Identifiable, Hashable {
    var id: String = ""
    var title: String = ""
    var description: String = ""
    var price: Double = 0.0
    var stock: Int = 0
    var category: String = ""
    var artisanName: String = ""
    var status: ProductStatus = .pending
    var imageUrls: [String] = []
    var rejectionReason: String = ""
    var createdAt: Int64 = Int64(Date().timeIntervalSince1970 * 1000)
    var originRegion: String = ""
    var artisanTechnique: String = ""
    var materialsUsed: String = ""
    var history: String = ""
    var shopifyProductId: String = ""
    var shopifyProductHandle: String = ""
    
    // Coding keys to map case conventions if needed (Firestore uses standard camelCase)
    enum CodingKeys: String, CodingKey {
        case id
        case title
        case description
        case price
        case stock
        case category
        case artisanName
        case status
        case imageUrls
        case rejectionReason
        case createdAt
        case originRegion
        case artisanTechnique
        case materialsUsed
        case history
        case shopifyProductId
        case shopifyProductHandle
    }
}
