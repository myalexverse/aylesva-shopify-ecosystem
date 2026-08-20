package com.aylesva.artisan.data.model

data class ArtisanProduct(
    val id: String = "",
    val title: String = "",
    val description: String = "",
    val price: Double = 0.0,
    val stock: Int = 0,
    val category: String = "", // e.g. "Calzado", "Ropa", "Hogar", etc.
    val artisanName: String = "",
    val status: ProductStatus = ProductStatus.PENDING,
    val imageUrls: List<String> = emptyList(),
    val rejectionReason: String = "",
    val createdAt: Long = System.currentTimeMillis(),
    val originRegion: String = "",
    val artisanTechnique: String = "",
    val materialsUsed: String = "",
    val history: String = "",
    val shopifyProductId: String = "",
    val shopifyProductHandle: String = ""
)
