package com.aylesva.artisan.viewmodel

import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aylesva.artisan.data.model.ArtisanProduct
import com.aylesva.artisan.data.model.ProductStatus
import com.aylesva.artisan.data.repository.ProductRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch

class ProductViewModel(
    private val repository: ProductRepository = ProductRepository()
) : ViewModel() {

    // Simulating a logged-in artisan (can be modified to use real auth)
    private val _artisanName = MutableStateFlow("Artesano Diana")
    val artisanName: StateFlow<String> = _artisanName.asStateFlow()

    // Flow containing the products list
    private val _products = MutableStateFlow<List<ArtisanProduct>>(emptyList())
    val products: StateFlow<List<ArtisanProduct>> = _products.asStateFlow()

    // Loading states
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    // Upload & Save status
    private val _operationStatus = MutableStateFlow<OperationResult?>(null)
    val operationStatus: StateFlow<OperationResult?> = _operationStatus.asStateFlow()

    init {
        loadProducts()
    }

    fun setArtisanName(name: String) {
        _artisanName.value = name
        loadProducts()
    }

    private fun loadProducts() {
        viewModelScope.launch {
            _isLoading.value = true
            repository.getProductsByArtisan(_artisanName.value)
                .catch { e ->
                    _products.value = emptyList()
                    _isLoading.value = false
                }
                .collect { list ->
                    _products.value = list
                    _isLoading.value = false
                }
        }
    }

    fun registerProduct(
        title: String,
        description: String,
        price: Double,
        stock: Int,
        category: String,
        originRegion: String,
        artisanTechnique: String,
        materialsUsed: String,
        history: String,
        selectedImageUris: List<Uri>
    ) {
        viewModelScope.launch {
            _isLoading.value = true
            _operationStatus.value = OperationResult.Progress("Subiendo fotos...")

            val uploadedUrls = mutableListOf<String>()
            var uploadSuccess = true

            // 1. Upload images first
            for (uri in selectedImageUris) {
                repository.uploadProductImage(uri)
                    .onSuccess { url ->
                        uploadedUrls.add(url)
                    }
                    .onFailure { error ->
                        uploadSuccess = false
                        _operationStatus.value = OperationResult.Error("Error al subir imagen: ${error.localizedMessage}")
                    }
                if (!uploadSuccess) break
            }

            if (!uploadSuccess) {
                _isLoading.value = false
                return@launch
            }

            _operationStatus.value = OperationResult.Progress("Registrando producto...")

            // 2. Save product object to Firestore
            val newProduct = ArtisanProduct(
                title = title,
                description = description,
                price = price,
                stock = stock,
                category = category,
                artisanName = _artisanName.value,
                status = ProductStatus.PENDING,
                imageUrls = uploadedUrls,
                originRegion = originRegion,
                artisanTechnique = artisanTechnique,
                materialsUsed = materialsUsed,
                history = history
            )

            repository.saveProduct(newProduct)
                .onSuccess {
                    _operationStatus.value = OperationResult.Success("Producto registrado exitosamente para revisión.")
                }
                .onFailure { error ->
                    _operationStatus.value = OperationResult.Error("Error al guardar producto: ${error.localizedMessage}")
                }
            _isLoading.value = false
        }
    }

    fun clearOperationStatus() {
        _operationStatus.value = null
    }

    sealed interface OperationResult {
        data class Success(val message: String) : OperationResult
        data class Progress(val message: String) : OperationResult
        data class Error(val message: String) : OperationResult
    }
}
