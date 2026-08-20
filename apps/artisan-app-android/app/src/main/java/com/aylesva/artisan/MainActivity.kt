package com.aylesva.artisan

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.aylesva.artisan.ui.screens.AddProductScreen
import com.aylesva.artisan.ui.screens.HomeScreen
import com.aylesva.artisan.ui.theme.ArtisanAppTheme
import com.aylesva.artisan.viewmodel.ProductViewModel

class MainActivity : ComponentActivity() {
    
    private val viewModel: ProductViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ArtisanAppTheme {
                AppNavigation(viewModel)
            }
        }
    }
}

@Composable
fun AppNavigation(viewModel: ProductViewModel) {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
                viewModel = viewModel,
                onNavigateToAddProduct = { navController.navigate("add_product") }
            )
        }
        composable("add_product") {
            AddProductScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
