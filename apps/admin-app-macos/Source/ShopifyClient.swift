import Foundation

class ShopifyClient {
    
    // Shopify Store Credentials (read securely from environment)
    private let shopName = ProcessInfo.processInfo.environment["SHOPIFY_SHOP_NAME"] ?? "aylesvamx.myshopify.com"
    private let accessToken = ProcessInfo.processInfo.environment["SHOPIFY_ACCESS_TOKEN"] ?? ""
    private let apiVersion = "2025-01"
    
    private var baseURL: String {
        return "https://\(shopName)/admin/api/\(apiVersion)"
    }
    
    // Shopify API models
    struct ShopifyImage: Codable {
        let src: String
    }
    
    struct ShopifyVariant: Codable {
        let price: String
        let sku: String?
        let inventory_quantity: Int
        let inventory_management: String
    }
    
    struct ShopifyProduct: Codable {
        let title: String
        let body_html: String
        let vendor: String
        let product_type: String
        let status: String // "active" or "draft"
        let images: [ShopifyImage]
        let variants: [ShopifyVariant]
    }
    
    struct ShopifyPayload: Codable {
        let product: ShopifyProduct
    }
    
    struct ShopifyResponse: Codable {
        struct ProductResponse: Codable {
            let id: Int64
            let handle: String
        }
        let product: ProductResponse
    }
    
    /**
     * Uploads the artisan product to Aylesva's Shopify store catalog.
     */
    func createProduct(from product: ArtisanProduct) async throws -> (id: Int64, handle: String) {
        let url = URL(string: "\(baseURL)/products.json")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(accessToken, forHTTPHeaderField: "X-Shopify-Access-Token")
        
        // Prepare images payloads
        let shopifyImages = product.imageUrls.map { ShopifyImage(src: $0) }
        
        // Prepare variant (price and inventory stock)
        let skuPrefix = product.artisanName.prefix(3).uppercased()
        let sku = "\(skuPrefix)-\(Int.random(in: 10000...99999))"
        let shopifyVariant = ShopifyVariant(
            price: String(format: "%.2f", product.price),
            sku: sku,
            inventory_quantity: product.stock,
            inventory_management: "shopify"
        )
        
        // Build the Authenticity Passport HTML
        let passportHtml = """
        <div class="aylesva-authenticity-passport" style="border: 2px solid #C5A47E; border-radius: 8px; padding: 20px; margin-top: 30px; font-family: sans-serif; background-color: #FDFCF9;">
            <div style="display: flex; align-items: center; border-bottom: 1px solid #C5A47E; padding-bottom: 12px; margin-bottom: 16px;">
                <span style="font-size: 16px; font-weight: bold; letter-spacing: 0.1em; color: #1A1A1A;">PASAPORTE DE AUTENTICIDAD Y ORIGEN</span>
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #333333; margin-bottom: 16px;">
                <tr>
                    <td style="padding: 6px 0; font-weight: bold; width: 40%; color: #888888; text-transform: uppercase; font-size: 10px;">Artesano Creador</td>
                    <td style="padding: 6px 0; color: #1A1A1A; font-weight: 600;">\(product.artisanName)</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; font-weight: bold; color: #888888; text-transform: uppercase; font-size: 10px;">Región de Origen</td>
                    <td style="padding: 6px 0; color: #1A1A1A; font-weight: 600;">\(product.originRegion)</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; font-weight: bold; color: #888888; text-transform: uppercase; font-size: 10px;">Técnica Utilizada</td>
                    <td style="padding: 6px 0; color: #1A1A1A; font-weight: 600;">\(product.artisanTechnique)</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; font-weight: bold; color: #888888; text-transform: uppercase; font-size: 10px;">Materiales e Insumos</td>
                    <td style="padding: 6px 0; color: #1A1A1A; font-weight: 600;">\(product.materialsUsed)</td>
                </tr>
            </table>
            <div style="border-top: 1px dashed #E5D5C5; padding-top: 12px; font-size: 12.5px; line-height: 1.5; color: #555555;">
                <strong style="color: #1A1A1A; display: block; margin-bottom: 4px;">Historia y Tradición de la Pieza:</strong>
                \(product.history.isEmpty ? "Pieza única elaborada con métodos tradicionales." : product.history)
            </div>
        </div>
        """
        
        let bodyHtml = """
        <p>\(product.description)</p>
        \(passportHtml)
        """
        
        // Build Shopify product object
        let shopifyProduct = ShopifyProduct(
            title: product.title,
            body_html: bodyHtml,
            vendor: product.artisanName,
            product_type: product.category,
            status: "active", // Published directly to active catalog
            images: shopifyImages,
            variants: [shopifyVariant]
        )
        
        let payload = ShopifyPayload(product: shopifyProduct)
        
        let encoder = JSONEncoder()
        request.httpBody = try encoder.encode(payload)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "ShopifyClient", code: -1, userInfo: [NSLocalizedDescriptionKey: "Respuesta de servidor inválida"])
        }
        
        if !(200...299).contains(httpResponse.statusCode) {
            let errorString = String(data: data, encoding: .utf8) ?? "Desconocido"
            throw NSError(domain: "ShopifyClient", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Error de Shopify: \(errorString)"])
        }
        
        let decoder = JSONDecoder()
        let result = try decoder.decode(ShopifyResponse.self, from: data)
        return (result.product.id, result.product.handle)
    }
}
