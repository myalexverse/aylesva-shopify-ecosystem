import Foundation
import Combine

class ProductViewModel: ObservableObject {
    
    private let firebaseService: FirebaseService
    private let shopifyClient = ShopifyClient()
    
    @Published var selectedStatus: ProductStatus = .pending
    @Published var isLoading = false
    @Published var alertMessage: String?
    
    // Form fields for editing
    @Published var editTitle = ""
    @Published var editDescription = ""
    @Published var editPrice = 0.0
    @Published var editStock = 0
    @Published var editCategory = ""
    @Published var rejectionReason = ""
    @Published var editOriginRegion = ""
    @Published var editArtisanTechnique = ""
    @Published var editMaterialsUsed = ""
    @Published var editHistory = ""
    
    private var cancellables = Set<AnyCancellable>()
    
    init(firebaseService: FirebaseService) {
        self.firebaseService = firebaseService
    }
    
    var filteredProducts: [ArtisanProduct] {
        return firebaseService.products.filter { $0.status == selectedStatus }
    }
    
    func selectProduct(_ product: ArtisanProduct) {
        editTitle = product.title
        editDescription = product.description
        editPrice = product.price
        editStock = product.stock
        editCategory = product.category
        rejectionReason = ""
        editOriginRegion = product.originRegion
        editArtisanTechnique = product.artisanTechnique
        editMaterialsUsed = product.materialsUsed
        editHistory = product.history
    }
    
    /**
     * Approves the product: uploads it to Shopify, then marks it as Approved in Firebase.
     */
    func approveProduct(_ product: ArtisanProduct) async {
        guard !isLoading else { return }
        
        await MainActor.run {
            self.isLoading = true
            self.alertMessage = nil
        }
        
        // Assemble updated values from edits
        var updatedProduct = product
        updatedProduct.title = editTitle
        updatedProduct.description = editDescription
        updatedProduct.price = editPrice
        updatedProduct.stock = editStock
        updatedProduct.category = editCategory
        updatedProduct.originRegion = editOriginRegion
        updatedProduct.artisanTechnique = editArtisanTechnique
        updatedProduct.materialsUsed = editMaterialsUsed
        updatedProduct.history = editHistory
        
        do {
            // 1. Upload to Shopify store catalog
            let shopifyResult = try await shopifyClient.createProduct(from: updatedProduct)
            
            // 2. Save approval state in Firebase
            try await firebaseService.approveProduct(
                id: product.id,
                shopifyId: shopifyResult.id,
                shopifyHandle: shopifyResult.handle,
                updatedCategory: editCategory,
                updatedTitle: editTitle,
                updatedPrice: editPrice
            )
            
            await MainActor.run {
                self.isLoading = false
                self.alertMessage = "¡Producto '\(editTitle)' aprobado e importado a Shopify exitosamente!"
            }
        } catch {
            await MainActor.run {
                self.isLoading = false
                self.alertMessage = "Error al aprobar: \(error.localizedDescription)"
            }
        }
    }
    
    /**
     * Rejects the product: saves status and reason in Firebase without publishing to Shopify.
     */
    func rejectProduct(_ product: ArtisanProduct) async {
        guard !isLoading else { return }
        guard !rejectionReason.trimmingCharacters(in: .whitespaces).isEmpty else {
            await MainActor.run {
                self.alertMessage = "Debes ingresar un motivo de rechazo."
            }
            return
        }
        
        await MainActor.run {
            self.isLoading = true
            self.alertMessage = nil
        }
        
        do {
            try await firebaseService.rejectProduct(id: product.id, reason: rejectionReason)
            
            await MainActor.run {
                self.isLoading = false
                self.alertMessage = "Producto rechazado. Se notificó al artesano."
            }
        } catch {
            await MainActor.run {
                self.isLoading = false
                self.alertMessage = "Error al rechazar: \(error.localizedDescription)"
            }
        }
    }
}
