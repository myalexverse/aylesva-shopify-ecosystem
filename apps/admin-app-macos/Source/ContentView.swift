import SwiftUI
import CoreImage.CIFilterBuiltins
import Charts

enum SidebarItem: Hashable {
    case status(ProductStatus)
    case dashboard
}

struct ContentView: View {
    @StateObject private var firebaseService = FirebaseService()
    @StateObject private var viewModel: ProductViewModel
    @State private var sidebarSelection: SidebarItem = .status(.pending)
    @State private var selectedProduct: ArtisanProduct?
    
    // Categories matching the Android App
    let categories = [
        "Calzado", "Ropa Caballero", "Ropa Dama", "Joyería y Accesorios",
        "Bolsas y Carteras", "Velas y Aromaterapia", "Decoración Hogar",
        "Cocina y Comedor", "Organizadores", "Alimentos", "Otros"
    ]
    
    init() {
        let fService = FirebaseService()
        _firebaseService = StateObject(wrappedValue: fService)
        _viewModel = StateObject(wrappedValue: ProductViewModel(firebaseService: fService))
    }
    
    var body: some View {
        NavigationSplitView {
            // 1. Sidebar navigation
            List(selection: $sidebarSelection) {
                Section("Estados de Revisión") {
                    ForEach(ProductStatus.allCases, id: \.self) { status in
                        NavigationLink(value: SidebarItem.status(status)) {
                            Label(status.label, systemImage: statusIcon(status))
                        }
                    }
                }
                
                Section("Reportes Gubernamentales") {
                    NavigationLink(value: SidebarItem.dashboard) {
                        Label("Impacto Social", systemImage: "map.fill")
                    }
                }
            }
            .navigationTitle("Aylesva Admin")
            .listStyle(.sidebar)
        } content: {
            // 2. Middle column: Products list (only shown for review statuses)
            switch sidebarSelection {
            case .status(let status):
                List(firebaseService.products.filter { $0.status == status }, selection: $selectedProduct) { product in
                    NavigationLink(value: product) {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(product.title)
                                .font(.headline)
                                .lineLimit(1)
                            Text("De: \(product.artisanName)")
                                .font(.subheadline)
                                .foregroundColor(.gray)
                            HStack {
                                Text(product.category)
                                    .font(.caption)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.secondary.opacity(0.1))
                                    .cornerRadius(4)
                                Spacer()
                                Text(String(format: "$%.2f", product.price))
                                    .font(.subheadline)
                                    .fontWeight(.semibold)
                                    .foregroundColor(.green)
                            }
                        }
                        .padding(.vertical, 4)
                    }
                }
                .navigationTitle(status.label)
                .overlay {
                    if firebaseService.products.filter({ $0.status == status }).isEmpty {
                        AylesvaPlaceholderView(title: "No hay productos", systemImage: "archivebox", description: "No hay elementos en este estado de revisión.")
                    }
                }
            case .dashboard:
                List {
                    Text("Métricas Generales")
                        .font(.headline)
                        .foregroundColor(.gray)
                        .padding(.vertical, 8)
                    Text("Selecciona 'Impacto Social' en el sidebar para ver los gráficos detallados en el panel derecho.")
                        .foregroundColor(.gray)
                        .font(.subheadline)
                }
                .navigationTitle("Dashboard")
            }
        } detail: {
            // 3. Detail Pane: Product editor OR Government Dashboard
            switch sidebarSelection {
            case .status:
                if let product = selectedProduct {
                    ProductDetailsView(
                        product: product,
                        selectedProduct: $selectedProduct,
                        viewModel: viewModel,
                        categories: categories
                    )
                } else {
                    AylesvaPlaceholderView(title: "Selecciona un producto", systemImage: "selection.pin.in.out", description: "Selecciona un producto del listado para iniciar su revisión y aprobación.")
                }
            case .dashboard:
                ImpactDashboardView(products: firebaseService.products)
            }
        }
        .onAppear {
            firebaseService.startObservingProducts()
        }
        .onDisappear {
            firebaseService.stopObserving()
        }
    }
    
    private func statusIcon(_ status: ProductStatus) -> String {
        switch status {
        case .pending: return "clock.badge.exclamationmark.fill"
        case .approved: return "checkmark.seal.fill"
        case .rejected: return "xmark.octagon.fill"
        }
    }
}

struct ProductDetailsView: View {
    let product: ArtisanProduct
    @Binding var selectedProduct: ArtisanProduct?
    @ObservedObject var viewModel: ProductViewModel
    let categories: [String]
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                // Image Gallery
                if !product.imageUrls.isEmpty {
                    ScrollView(.horizontal, showsIndicators: true) {
                        HStack(spacing: 16) {
                            ForEach(product.imageUrls, id: \.self) { url in
                                AsyncImage(url: URL(string: url)) { image in
                                    image.resizable()
                                        .aspectRatio(contentMode: .fit)
                                        .frame(height: 220)
                                        .cornerRadius(8)
                                } placeholder: {
                                    ProgressView()
                                        .frame(width: 220, height: 220)
                                }
                            }
                        }
                        .padding(12)
                    }
                    .frame(height: 250)
                    .background(Color.black.opacity(0.05))
                    .cornerRadius(12)
                }
                
                // Form Fields (Editable by admin before approval)
                GroupBox("Detalles del Producto (Edición)") {
                    VStack(alignment: .leading, spacing: 16) {
                        TextField("Título", text: $viewModel.editTitle)
                            .textFieldStyle(.roundedBorder)
                        
                        Picker("Categoría", selection: $viewModel.editCategory) {
                            ForEach(categories, id: \.self) { cat in
                                Text(cat).tag(cat)
                            }
                        }
                        .pickerStyle(.menu)
                        
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Precio (MXN)")
                                    .font(.caption2)
                                    .foregroundColor(.gray)
                                TextField("Precio", value: $viewModel.editPrice, format: .number)
                                    .textFieldStyle(.roundedBorder)
                            }
                            
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Stock disponible")
                                    .font(.caption2)
                                    .foregroundColor(.gray)
                                TextField("Stock", value: $viewModel.editStock, format: .number)
                                    .textFieldStyle(.roundedBorder)
                            }
                        }
                        
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Descripción general")
                                .font(.caption2)
                                .foregroundColor(.gray)
                            TextEditor(text: $viewModel.editDescription)
                                .frame(height: 80)
                                .border(Color.gray.opacity(0.2))
                                .cornerRadius(4)
                        }
                    }
                    .padding(.vertical, 8)
                }
                
                // Heritage & Origin Fields (Traceability)
                GroupBox("Pasaporte de Patrimonio y Trazabilidad") {
                    VStack(alignment: .leading, spacing: 16) {
                        TextField("Comunidad / Municipio de Origen", text: $viewModel.editOriginRegion)
                            .textFieldStyle(.roundedBorder)
                        TextField("Técnica Artesanal", text: $viewModel.editArtisanTechnique)
                            .textFieldStyle(.roundedBorder)
                        TextField("Materiales e Insumos", text: $viewModel.editMaterialsUsed)
                            .textFieldStyle(.roundedBorder)
                        
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Historia y Significado de la Pieza")
                                .font(.caption2)
                                .foregroundColor(.gray)
                            TextEditor(text: $viewModel.editHistory)
                                .frame(height: 80)
                                .border(Color.gray.opacity(0.2))
                                .cornerRadius(4)
                        }
                    }
                    .padding(.vertical, 8)
                }
                
                // Action Buttons
                VStack(alignment: .leading, spacing: 12) {
                    if product.status == .pending {
                        HStack(spacing: 16) {
                            Button {
                                Task {
                                    await viewModel.approveProduct(product)
                                    if !viewModel.isLoading && viewModel.alertMessage?.contains("aprobado") == true {
                                        selectedProduct = nil
                                    }
                                }
                            } label: {
                                HStack {
                                    Image(systemName: "checkmark.seal.fill")
                                    Text("Aprobar y Publicar en Shopify")
                                }
                                .frame(maxWidth: .infinity, minHeight: 38)
                                .background(Color.green)
                                .foregroundColor(.white)
                                .cornerRadius(8)
                            }
                            .buttonStyle(.plain)
                            .disabled(viewModel.isLoading)
                        }
                        
                        Divider()
                            .padding(.vertical, 8)
                        
                        GroupBox("Rechazar Registro") {
                            VStack(alignment: .leading, spacing: 8) {
                                TextField("Motivo de rechazo...", text: $viewModel.rejectionReason)
                                    .textFieldStyle(.roundedBorder)
                                
                                Button {
                                    Task {
                                        await viewModel.rejectProduct(product)
                                        if !viewModel.isLoading && viewModel.alertMessage?.contains("rechazado") == true {
                                            selectedProduct = nil
                                        }
                                    }
                                } label: {
                                    HStack {
                                        Image(systemName: "xmark.octagon.fill")
                                        Text("Rechazar")
                                    }
                                    .frame(maxWidth: .infinity, minHeight: 30)
                                    .background(Color.red)
                                    .foregroundColor(.white)
                                    .cornerRadius(6)
                                }
                                .buttonStyle(.plain)
                                .disabled(viewModel.isLoading)
                            }
                            .padding(.vertical, 4)
                        }
                    } else if product.status == .approved {
                        VStack(alignment: .leading, spacing: 16) {
                            HStack {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.green)
                                Text("Este producto ya fue aprobado y publicado en Shopify.")
                                    .font(.subheadline)
                                    .fontWeight(.semibold)
                            }
                            .padding()
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.green.opacity(0.1))
                            .cornerRadius(8)
                            
                            // Authenticity Passport PDF/Print QR Code Generator
                            GroupBox("Pasaporte de Autenticidad (Código QR)") {
                                HStack(spacing: 20) {
                                    let productUrl = "https://aylesvamx.myshopify.com/products/\(product.shopifyProductHandle)"
                                    if let qrImage = generateQRCode(from: productUrl) {
                                        Image(nsImage: qrImage)
                                            .resizable()
                                            .frame(width: 110, height: 110)
                                            .padding(4)
                                            .background(Color.white)
                                            .cornerRadius(6)
                                            .shadow(radius: 2)
                                    }
                                    
                                    VStack(alignment: .leading, spacing: 6) {
                                        Text("Enlace de Autenticidad")
                                            .font(.headline)
                                        Text(productUrl)
                                            .font(.caption)
                                            .foregroundColor(.blue)
                                            .underline()
                                            .lineLimit(1)
                                            .onTapGesture {
                                                if let url = URL(string: productUrl) {
                                                    NSWorkspace.shared.open(url)
                                                }
                                            }
                                        Text("Imprime este código QR y colócalo como pasaporte digital en la etiqueta del producto. Permite a los compradores escanearlo y conocer el origen cultural de su pieza.")
                                            .font(.caption2)
                                            .foregroundColor(.gray)
                                            .lineLimit(nil)
                                    }
                                }
                                .padding(.vertical, 6)
                            }
                        }
                    } else if product.status == .rejected {
                        VStack(alignment: .leading, spacing: 6) {
                            HStack {
                                Image(systemName: "xmark.circle.fill")
                                    .foregroundColor(.red)
                                Text("Producto Rechazado")
                                    .font(.subheadline)
                                    .fontWeight(.semibold)
                            }
                            Text("Motivo: \(product.rejectionReason)")
                                .font(.subheadline)
                                .foregroundColor(.red)
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(Color.red.opacity(0.1))
                        .cornerRadius(8)
                    }
                }
                
                // Alert or message feedback
                if let message = viewModel.alertMessage {
                    Text(message)
                        .font(.callout)
                        .foregroundColor(message.contains("Error") ? .red : .blue)
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .center)
                        .background(Color.gray.opacity(0.1))
                        .cornerRadius(8)
                }
            }
            .padding(32)
        }
        .navigationTitle("Detalles de Revisión")
        .onChange(of: product) { newProduct in
            viewModel.selectProduct(newProduct)
        }
        .onAppear {
            viewModel.selectProduct(product)
        }
        .overlay {
            if viewModel.isLoading {
                ZStack {
                    Color.black.opacity(0.1)
                    ProgressView("Subiendo a Shopify...")
                        .padding()
                        .background(Color.white)
                        .cornerRadius(8)
                }
            }
        }
    }
    
    // QR Code Generator using CoreImage
    private func generateQRCode(from string: String) -> NSImage? {
        let context = CIContext()
        let filter = CIFilter.qrCodeGenerator()
        filter.message = Data(string.utf8)
        
        if let outputImage = filter.outputImage {
            let transform = CGAffineTransform(scaleX: 10, y: 10)
            let scaledImage = outputImage.transformed(by: transform)
            if let cgImage = context.createCGImage(scaledImage, from: scaledImage.extent) {
                return NSImage(cgImage: cgImage, size: NSSize(width: 150, height: 150))
            }
        }
        return nil
    }
}

// 4. Government impact analytics dashboard view
struct ImpactDashboardView: View {
    let products: [ArtisanProduct]
    
    // Helper structures for Swift Charts
    struct RegionStat: Identifiable {
        let id = UUID()
        let region: String
        let stock: Int
    }
    
    struct TechStat: Identifiable {
        let id = UUID()
        let technique: String
        let count: Int
    }
    
    var approvedProducts: [ArtisanProduct] {
        return products.filter { $0.status == .approved }
    }
    
    var totalEconomicValue: Double {
        return approvedProducts.map { $0.price * Double($0.stock) }.reduce(0, +)
    }
    
    var totalArtisansRegistered: Int {
        return Set(products.map { $0.artisanName }).count
    }
    
    // Aggregate data by region
    var regionData: [RegionStat] {
        var counts = [String: Int]()
        for p in approvedProducts {
            let region = p.originRegion.trimmingCharacters(in: .whitespaces).isEmpty ? "Oaxaca Central" : p.originRegion
            counts[region, default: 0] += p.stock
        }
        return counts.map { RegionStat(region: $0.key, stock: $0.value) }
            .sorted(by: { $0.stock > $1.stock })
    }
    
    // Aggregate data by technique
    var techniqueData: [TechStat] {
        var counts = [String: Int]()
        for p in approvedProducts {
            let tech = p.artisanTechnique.trimmingCharacters(in: .whitespaces).isEmpty ? "Tradicional" : p.artisanTechnique
            counts[tech, default: 0] += 1
        }
        return counts.map { TechStat(technique: $0.key, count: $0.value) }
            .sorted(by: { $0.count > $1.count })
    }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 28) {
                // Title and intro
                VStack(alignment: .leading, spacing: 6) {
                    Text("DASHBOARD DE IMPACTO SOCIAL")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.gray)
                        .kerning(1.5)
                    Text("Reporte de Desarrollo Económico y Preservación")
                        .font(.title)
                        .fontWeight(.bold)
                    Text("Métricas consolidadas para uso en reportes gubernamentales de inclusión digital e impacto regional de la plataforma Aylesva.")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
                
                // Stat cards Row
                HStack(spacing: 20) {
                    StatCard(
                        title: "VALOR ECONÓMICO",
                        value: String(format: "$%.2f MXN", totalEconomicValue),
                        subtitle: "Monto total del inventario publicado",
                        icon: "dollarsign.circle",
                        color: .green
                    )
                    
                    StatCard(
                        title: "PRODUCTOS REGISTRADOS",
                        value: "\(products.count)",
                        subtitle: "\(approvedProducts.count) aprobados y en tienda",
                        icon: "tag.fill",
                        color: .blue
                    )
                    
                    StatCard(
                        title: "ARTESANOS INCLUIDOS",
                        value: "\(totalArtisansRegistered)",
                        subtitle: "Artesanos con inclusión digital activa",
                        icon: "person.2.fill",
                        color: .purple
                    )
                }
                
                Divider()
                    .padding(.vertical, 8)
                
                // Graphical Charts Sections
                HStack(alignment: .top, spacing: 32) {
                    // Region Chart
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Producción por Región / Municipio")
                            .font(.title3)
                            .fontWeight(.bold)
                        Text("Volumen de piezas artesanales activas distribuidas en la tienda por comunidad.")
                            .font(.caption)
                            .foregroundColor(.gray)
                        
                        if regionData.isEmpty {
                            Text("Sin datos de regiones disponibles.")
                                .foregroundColor(.gray)
                                .frame(height: 200)
                        } else {
                            Chart(regionData.prefix(5)) { item in
                                BarMark(
                                    x: .value("Piezas", item.stock),
                                    y: .value("Comunidad", item.region)
                                )
                                .foregroundStyle(Color.blue.gradient)
                                .annotation(position: .trailing) {
                                    Text("\(item.stock) pz").font(.caption2).foregroundColor(.gray)
                                }
                            }
                            .frame(height: 200)
                            .padding(.trailing, 40)
                        }
                    }
                    .padding()
                    .background(Color.black.opacity(0.02))
                    .cornerRadius(12)
                    .frame(maxWidth: .infinity)
                    
                    // Technique Chart
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Diversidad de Técnicas Artesanales")
                            .font(.title3)
                            .fontWeight(.bold)
                        Text("Cantidad de diseños únicos catalogados y clasificados según técnica familiar.")
                            .font(.caption)
                            .foregroundColor(.gray)
                        
                        if techniqueData.isEmpty {
                            Text("Sin datos de técnicas disponibles.")
                                .foregroundColor(.gray)
                                .frame(height: 200)
                        } else {
                            Chart(techniqueData.prefix(5)) { item in
                                BarMark(
                                    x: .value("Piezas", item.count),
                                    y: .value("Técnica", item.technique)
                                )
                                .foregroundStyle(Color.purple.gradient)
                                .annotation(position: .trailing) {
                                    Text("\(item.count) prod").font(.caption2).foregroundColor(.gray)
                                }
                            }
                            .frame(height: 200)
                            .padding(.trailing, 40)
                        }
                    }
                    .padding()
                    .background(Color.black.opacity(0.02))
                    .cornerRadius(12)
                    .frame(maxWidth: .infinity)
                }
                
                // Privacy disclaimer box (critical for government trust)
                GroupBox("Gobernanza de Datos y Privacidad") {
                    HStack(spacing: 16) {
                        Image(systemName: "lock.shield.fill")
                            .font(.system(size: 32))
                            .foregroundColor(.blue)
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Arquitectura de Privacidad Estricta")
                                .fontWeight(.bold)
                            Text("Este panel calcula métricas de impacto económico de forma anónima y agregada. La información personal de contacto y detalles específicos de los artesanos se encuentran encriptados y protegidos en la base de datos de origen, garantizando la confidencialidad de la información y la confianza del usuario final.")
                                .font(.caption)
                                .foregroundColor(.gray)
                        }
                    }
                    .padding(.vertical, 8)
                }
            }
            .padding(40)
        }
        .background(Color.white)
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let subtitle: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(title)
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.gray)
                Spacer()
                Image(systemName: icon)
                    .foregroundColor(color)
                    .font(.title2)
            }
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
            Text(subtitle)
                .font(.caption2)
                .foregroundColor(.gray)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: Color.black.opacity(0.04), radius: 6, x: 0, y: 3)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.gray.opacity(0.15), lineWidth: 1)
        )
    }
}

struct AylesvaPlaceholderView: View {
    let title: String
    let systemImage: String
    let description: String
    
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: systemImage)
                .font(.system(size: 40))
                .foregroundColor(.secondary)
            Text(title)
                .font(.title3)
                .fontWeight(.semibold)
            Text(description)
                .font(.body)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 24)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
