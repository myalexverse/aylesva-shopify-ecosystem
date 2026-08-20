package com.aylesva.artisan.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.aylesva.artisan.data.model.ArtisanProduct
import com.aylesva.artisan.data.model.ProductStatus
import com.aylesva.artisan.viewmodel.ProductViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: ProductViewModel,
    onNavigateToAddProduct: () -> Unit
) {
    val products by viewModel.products.collectAsState()
    val artisanName by viewModel.artisanName.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    var showProfileDialog by remember { mutableStateOf(false) }
    var tempProfileName by remember { mutableStateOf(artisanName) }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Text(
                        "MIS PRODUCTOS",
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 2.sp,
                        fontSize = 18.sp
                    )
                },
                actions = {
                    IconButton(onClick = { showProfileDialog = true }) {
                        Icon(Icons.Default.Edit, contentDescription = "Editar artesano")
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    actionIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = onNavigateToAddProduct,
                containerColor = MaterialTheme.colorScheme.secondary,
                contentColor = MaterialTheme.colorScheme.primary,
                shape = CircleShape
            ) {
                Icon(Icons.Default.Add, contentDescription = "Agregar producto", modifier = Modifier.size(30.dp))
            }
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(MaterialTheme.colorScheme.background)
        ) {
            if (products.isEmpty() && !isLoading) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Text(
                        text = "No tienes productos registrados",
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp,
                        color = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Registra tus piezas de arte haciendo clic en el botón + de abajo.",
                        color = Color.Gray,
                        modifier = Modifier.fillMaxWidth(),
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center
                    )
                }
            } else {
                Column(modifier = Modifier.fillMaxSize()) {
                    // Artisan Profile Bar
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        shape = RoundedCornerShape(8.dp),
                        elevation = CardDefaults.cardElevation(2.dp)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(
                                    text = "Artesano",
                                    fontSize = 12.sp,
                                    color = Color.Gray,
                                    fontWeight = FontWeight.SemiBold
                                )
                                Text(
                                    text = artisanName,
                                    fontSize = 20.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.secondary
                                )
                            }
                        }
                    }

                    // Products List
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(bottom = 88.dp)
                    ) {
                        items(products) { product ->
                            ProductItemCard(product)
                        }
                    }
                }
            }

            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.align(Alignment.Center),
                    color = MaterialTheme.colorScheme.secondary
                )
            }
        }
    }

    // Simple profile name changing dialog
    if (showProfileDialog) {
        AlertDialog(
            onDismissRequest = { showProfileDialog = false },
            title = { Text("Configurar Nombre de Artesano", fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text("Ingresa tu nombre o marca para organizar tus productos:", fontSize = 14.sp)
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = tempProfileName,
                        onValueChange = { tempProfileName = it },
                        singleLine = true,
                        label = { Text("Nombre del Artesano") }
                    )
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        if (tempProfileName.isNotBlank()) {
                            viewModel.setArtisanName(tempProfileName)
                        }
                        showProfileDialog = false
                    }
                ) {
                    Text("Guardar", color = MaterialTheme.colorScheme.secondary)
                }
            },
            dismissButton = {
                TextButton(onClick = { showProfileDialog = false }) {
                    Text("Cancelar", color = Color.Gray)
                }
            }
        )
    }
}

@Composable
fun ProductItemCard(product: ArtisanProduct) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        shape = RoundedCornerShape(10.dp),
        elevation = CardDefaults.cardElevation(2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp)
        ) {
            // Thumbnail Image
            Box(
                modifier = Modifier
                    .size(90.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(Color(0xFFF0F0F0))
            ) {
                if (product.imageUrls.isNotEmpty()) {
                    AsyncImage(
                        model = product.imageUrls.first(),
                        contentDescription = product.title,
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                }
            }

            Spacer(modifier = Modifier.width(16.dp))

            // Details
            Column(
                modifier = Modifier
                    .weight(1f)
                    .align(Alignment.CenterVertically)
            ) {
                Text(
                    text = product.category.uppercase(),
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.secondary,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.sp
                )
                Text(
                    text = product.title,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                    maxLines = 1
                )
                Spacer(modifier = Modifier.height(4.dp))
                Row(
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = "$${String.format("%.2f", product.price)} MXN",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color(0xFF2D6B2D)
                    )
                    Text(
                        text = "Stock: ${product.stock}",
                        fontSize = 12.sp,
                        color = Color.Gray
                    )
                }

                Spacer(modifier = Modifier.height(8.dp))

                // Status Badge
                StatusBadge(product.status, product.rejectionReason)
            }
        }
    }
}

@Composable
fun StatusBadge(status: ProductStatus, rejectionReason: String) {
    val (backgroundColor, textColor, label) = when (status) {
        ProductStatus.PENDING -> Triple(Color(0xFFFFF9E6), Color(0xFFB27D00), "PENDIENTE DE REVISIÓN")
        ProductStatus.APPROVED -> Triple(Color(0xFFEBF7EB), Color(0xFF2D6B2D), "APROBADO")
        ProductStatus.REJECTED -> Triple(Color(0xFFFCEBEC), Color(0xFFB00020), "RECHAZADO")
    }

    Column {
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(4.dp))
                .background(backgroundColor)
                .padding(horizontal = 8.dp, vertical = 4.dp)
        ) {
            Text(
                text = label,
                fontSize = 10.sp,
                fontWeight = FontWeight.ExtraBold,
                color = textColor,
                letterSpacing = 0.5.sp
            )
        }

        if (status == ProductStatus.REJECTED && rejectionReason.isNotEmpty()) {
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Motivo: $rejectionReason",
                fontSize = 11.sp,
                color = Color(0xFFB00020),
                fontWeight = FontWeight.Medium
            )
        }
    }
}
