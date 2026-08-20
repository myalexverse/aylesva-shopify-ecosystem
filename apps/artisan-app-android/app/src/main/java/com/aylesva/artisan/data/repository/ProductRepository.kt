package com.aylesva.artisan.data.repository

import android.net.Uri
import com.aylesva.artisan.data.model.ArtisanProduct
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.tasks.await
import java.util.UUID

class ProductRepository {

    private val firestore = FirebaseFirestore.getInstance()
    private val storage = FirebaseStorage.getInstance()
    private val productsCollection = firestore.collection("products")

    /**
     * Streams the real-time list of products registered by a specific artisan.
     */
    fun getProductsByArtisan(artisanName: String): Flow<List<ArtisanProduct>> = callbackFlow {
        val listener = productsCollection
            .whereEqualTo("artisanName", artisanName)
            .orderBy("createdAt", Query.Direction.DESCENDING)
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    close(error)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val products = snapshot.toObjects(ArtisanProduct::class.java)
                    trySend(products)
                }
            }
        awaitClose { listener.remove() }
    }

    /**
     * Registers a new product in Firestore.
     */
    suspend fun saveProduct(product: ArtisanProduct): Result<Unit> = runCatching {
        val docRef = if (product.id.isEmpty()) {
            productsCollection.document()
        } else {
            productsCollection.document(product.id)
        }
        val finalProduct = product.copy(id = docRef.id)
        docRef.set(finalProduct).await()
    }

    /**
     * Uploads a local image file to Firebase Storage and returns its public download URL.
     */
    suspend fun uploadProductImage(imageUri: Uri): Result<String> = runCatching {
        val storageRef = storage.reference.child("product_images/${UUID.randomUUID()}.jpg")
        storageRef.putFile(imageUri).await()
        val downloadUrl = storageRef.downloadUrl.await()
        downloadUrl.toString()
    }
}
