package com.aylesva.artisan.ui.screens

import android.net.Uri
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import android.content.Intent
import android.speech.RecognizerIntent
import coil.compose.AsyncImage
import com.aylesva.artisan.viewmodel.ProductViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddProductScreen(
    viewModel: ProductViewModel,
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    val isLoading by viewModel.isLoading.collectAsState()
    val operationStatus by viewModel.operationStatus.collectAsState()

    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var priceStr by remember { mutableStateOf("") }
    var stockStr by remember { mutableStateOf("") }
    
    // Heritage fields
    var originRegion by remember { mutableStateOf("") }
    var artisanTechnique by remember { mutableStateOf("") }
    var materialsUsed by remember { mutableStateOf("") }
    var history by remember { mutableStateOf("") }

    // Speech-to-Text launcher
    var speechTargetField by remember { mutableStateOf<String?>(null) }
    val speechRecognizerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            val spokenText = result.data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)?.firstOrNull() ?: ""
            if (spokenText.isNotEmpty()) {
                when (speechTargetField) {
                    "description" -> description = (description + " " + spokenText).trim()
                    "history" -> history = (history + " " + spokenText).trim()
                }
            }
        }
        speechTargetField = null
    }

    val startVoiceDictation: (String) -> Unit = { target ->
        speechTargetField = target
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_PROMPT, "Habla para dictar...")
        }
        try {
            speechRecognizerLauncher.launch(intent)
        } catch (e: Exception) {
            Toast.makeText(context, "El dictado por voz no está disponible.", Toast.LENGTH_SHORT).show()
        }
    }

    // Categories
    val categories = listOf(
        "Calzado", "Ropa Caballero", "Ropa Dama", "Joyería y Accesorios",
        "Bolsas y Carteras", "Velas y Aromaterapia", "Decoración Hogar",
        "Cocina y Comedor", "Organizadores", "Alimentos", "Otros"
    )
    var selectedCategory by remember { mutableStateOf(categories[0]) }
    var showCategoryDropdown by remember { mutableStateOf(false) }

    // Images
    var selectedImageUris by remember { mutableStateOf<List<Uri>>(emptyList()) }
    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetMultipleContents()
    ) { uris ->
        selectedImageUris = selectedImageUris + uris
    }

    // Handle ViewModel Operation Result
    LaunchedEffect(operationStatus) {
        when (operationStatus) {
            is ProductViewModel.OperationResult.Success -> {
                Toast.makeText(context, (operationStatus as ProductViewModel.OperationResult.Success).message, Toast.LENGTH_LONG).show()
                viewModel.clearOperationStatus()
                onNavigateBack()
            }
            is ProductViewModel.OperationResult.Error -> {
                Toast.makeText(context, (operationStatus as ProductViewModel.OperationResult.Error).message, Toast.LENGTH_LONG).show()
                viewModel.clearOperationStatus()
            }
            else -> {}
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("REGISTRAR PRODUCTO", fontWeight = FontWeight.Bold, fontSize = 16.sp, letterSpacing = 1.sp) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack, enabled = !isLoading) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Regresar")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(MaterialTheme.colorScheme.background)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                EducationalCard(
                    title = "Inclusión Digital y Preservación",
                    description = "Registra tus piezas. Al documentar su origen, técnica e historia, contribuyes a la preservación del patrimonio y facilitas un pago justo por tu trabajo."
                )

                // Product Title
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Título del Producto") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isLoading,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.secondary,
                        focusedLabelColor = MaterialTheme.colorScheme.secondary
                    )
                )

                // Category Selection
                Box(modifier = Modifier.fillMaxWidth()) {
                    OutlinedTextField(
                        value = selectedCategory,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Categoría") },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = !isLoading,
                        trailingIcon = {
                            Icon(
                                Icons.Default.ArrowDropDown,
                                "Selector",
                                modifier = Modifier.clickable { if (!isLoading) showCategoryDropdown = true }
                            )
                        },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = MaterialTheme.colorScheme.secondary,
                            focusedLabelColor = MaterialTheme.colorScheme.secondary
                        )
                    )
                    DropdownMenu(
                        expanded = showCategoryDropdown,
                        onDismissRequest = { showCategoryDropdown = false },
                        modifier = Modifier.fillMaxWidth(0.9f)
                    ) {
                        categories.forEach { category ->
                            DropdownMenuItem(
                                text = { Text(category) },
                                onClick = {
                                    selectedCategory = category
                                    showCategoryDropdown = false
                                }
                            )
                        }
                    }
                }

                EducationalCard(
                    title = "Fijar un Precio Justo",
                    description = "Considera: Costo de materiales + horas de trabajo dedicadas + empaque y envío."
                )

                // Price and Stock row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    OutlinedTextField(
                        value = priceStr,
                        onValueChange = { priceStr = it },
                        label = { Text("Precio (MXN)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.weight(1f),
                        enabled = !isLoading,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = MaterialTheme.colorScheme.secondary,
                            focusedLabelColor = MaterialTheme.colorScheme.secondary
                        )
                    )
                    OutlinedTextField(
                        value = stockStr,
                        onValueChange = { stockStr = it },
                        label = { Text("Cantidad / Stock") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.weight(1f),
                        enabled = !isLoading,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = MaterialTheme.colorScheme.secondary,
                            focusedLabelColor = MaterialTheme.colorScheme.secondary
                        )
                    )
                }

                // Description
                OutlinedTextField(
                    value = description,
                    onValueChange = { description = it },
                    label = { Text("Descripción / Detalles") },
                    minLines = 3,
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isLoading,
                    trailingIcon = {
                        IconButton(onClick = { startVoiceDictation("description") }) {
                            Text("🎙", fontSize = 20.sp)
                        }
                    },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.secondary,
                        focusedLabelColor = MaterialTheme.colorScheme.secondary
                    )
                )

                Text(
                    "DATOS DE TRAZABILIDAD Y ORIGEN",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Gray,
                    letterSpacing = 1.sp
                )

                OutlinedTextField(
                    value = originRegion,
                    onValueChange = { originRegion = it },
                    label = { Text("Comunidad / Municipio de Origen") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isLoading,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.secondary,
                        focusedLabelColor = MaterialTheme.colorScheme.secondary
                    )
                )

                OutlinedTextField(
                    value = artisanTechnique,
                    onValueChange = { artisanTechnique = it },
                    label = { Text("Técnica Artesanal Utilizada") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isLoading,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.secondary,
                        focusedLabelColor = MaterialTheme.colorScheme.secondary
                    )
                )

                OutlinedTextField(
                    value = materialsUsed,
                    onValueChange = { materialsUsed = it },
                    label = { Text("Materiales y Materias Primas") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isLoading,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.secondary,
                        focusedLabelColor = MaterialTheme.colorScheme.secondary
                    )
                )

                EducationalCard(
                    title = "La Historia de tu Pieza",
                    description = "Escribe o dicta la inspiración de la pieza, qué significa este diseño para tu comunidad o cómo aprendiste esta técnica tradicional."
                )

                OutlinedTextField(
                    value = history,
                    onValueChange = { history = it },
                    label = { Text("Historia / Significado de la Pieza") },
                    minLines = 3,
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isLoading,
                    trailingIcon = {
                        IconButton(onClick = { startVoiceDictation("history") }) {
                            Text("🎙", fontSize = 20.sp)
                        }
                    },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.secondary,
                        focusedLabelColor = MaterialTheme.colorScheme.secondary
                    )
                )

                // Image Section
                Text(
                    "FOTOS DEL PRODUCTO",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Gray,
                    letterSpacing = 1.sp
                )

                // Horizontal Image List with Add Button
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    item {
                        Box(
                            modifier = Modifier
                                .size(90.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .border(1.dp, Color.Gray, RoundedCornerShape(8.dp))
                                .clickable(enabled = !isLoading) { galleryLauncher.launch("image/*") },
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("+", fontSize = 28.sp, color = Color.Gray)
                                Text("Añadir", fontSize = 11.sp, color = Color.Gray)
                            }
                        }
                    }

                    items(selectedImageUris) { uri ->
                        Box(
                            modifier = Modifier
                                .size(90.dp)
                                .clip(RoundedCornerShape(8.dp))
                        ) {
                            AsyncImage(
                                model = uri,
                                contentDescription = "Seleccionada",
                                modifier = Modifier.fillMaxSize(),
                                contentScale = ContentScale.Crop
                            )
                            Box(
                                modifier = Modifier
                                    .align(Alignment.TopEnd)
                                    .padding(4.dp)
                                    .size(20.dp)
                                    .clip(RoundedCornerShape(10.dp))
                                    .background(Color.Black.copy(alpha = 0.6f))
                                    .clickable { selectedImageUris = selectedImageUris - uri },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    Icons.Default.Close,
                                    "Eliminar",
                                    tint = Color.White,
                                    modifier = Modifier.size(12.dp)
                                )
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(20.dp))

                // Submit Button
                Button(
                    onClick = {
                        val price = priceStr.toDoubleOrNull()
                        val stock = stockStr.toIntOrNull()
                        if (title.isBlank() || price == null || stock == null || selectedImageUris.isEmpty()) {
                            Toast.makeText(context, "Por favor completa todos los campos y añade al menos una foto.", Toast.LENGTH_SHORT).show()
                        } else {
                            viewModel.registerProduct(
                                title = title,
                                description = description,
                                price = price,
                                stock = stock,
                                category = selectedCategory,
                                originRegion = originRegion,
                                artisanTechnique = artisanTechnique,
                                materialsUsed = materialsUsed,
                                history = history,
                                selectedImageUris = selectedImageUris
                            )
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(54.dp),
                    enabled = !isLoading,
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text(
                        "ENVIAR PARA REVISIÓN",
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.sp,
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                }
            }

            // Loading / Operation Progress Screen Overlay
            if (isLoading || operationStatus is ProductViewModel.OperationResult.Progress) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.5f))
                        .clickable(enabled = false) {},
                    contentAlignment = Alignment.Center
                ) {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.padding(32.dp)
                    ) {
                        Column(
                            modifier = Modifier.padding(24.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            CircularProgressIndicator(color = MaterialTheme.colorScheme.secondary)
                            Spacer(modifier = Modifier.height(16.dp))
                            val progressMessage = when (val status = operationStatus) {
                                is ProductViewModel.OperationResult.Progress -> status.message
                                else -> "Cargando..."
                            }
                            Text(progressMessage, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = Color.DarkGray)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun EducationalCard(title: String, description: String) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFFDF9)),
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.secondary.copy(alpha = 0.5f)),
        shape = RoundedCornerShape(8.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("💡", fontSize = 16.sp)
                Spacer(modifier = Modifier.width(8.dp))
                Text(title, fontWeight = FontWeight.Bold, fontSize = 13.sp, color = MaterialTheme.colorScheme.primary)
            }
            Spacer(modifier = Modifier.height(4.dp))
            Text(description, fontSize = 12.sp, color = Color.DarkGray)
        }
    }
}
