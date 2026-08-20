import Foundation
import FirebaseFirestore
import Combine

class FirebaseService: ObservableObject {
    
    private let db = Firestore.firestore()
    private let productsCollection = "products"
    
    @Published var products: [ArtisanProduct] = []
    private var listenerRegistration: ListenerRegistration?
    
    /**
     * Subscribes to real-time updates of all registered products in the system.
     */
    func startObservingProducts() {
        listenerRegistration?.remove()
        
        listenerRegistration = db.collection(productsCollection)
            .order(by: "createdAt", descending: true)
            .addSnapshotListener { [weak self] snapshot, error in
                guard let self = self else { return }
                
                if let error = error {
                    print("Error observing products: \(error.localizedDescription)")
                    return
                }
                
                guard let documents = snapshot?.documents else { return }
                
                self.products = documents.compactMap { doc -> ArtisanProduct? in
                    try? doc.data(as: ArtisanProduct.self)
                }
            }
    }
    
    func stopObserving() {
        listenerRegistration?.remove()
    }
    
    /**
     * Updates the product state to Approved and stores the generated Shopify Product ID.
     */
    func approveProduct(id: String, shopifyId: Int64, shopifyHandle: String, updatedCategory: String, updatedTitle: String, updatedPrice: Double) async throws {
        let docRef = db.collection(productsCollection).document(id)
        try await docRef.updateData([
            "status": ProductStatus.approved.rawValue,
            "shopifyProductId": String(shopifyId),
            "shopifyProductHandle": shopifyHandle,
            "category": updatedCategory,
            "title": updatedTitle,
            "price": updatedPrice
        ])
    }
    
    /**
     * Updates the product state to Rejected with feedback comments.
     */
    func rejectProduct(id: String, reason: String) async throws {
        let docRef = db.collection(productsCollection).document(id)
        try await docRef.updateData([
            "status": ProductStatus.rejected.rawValue,
            "rejectionReason": reason
        ])
    }
}
