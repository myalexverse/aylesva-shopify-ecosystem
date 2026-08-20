package com.aylesva.artisan.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Premium Aylesva Color Palette
val DarkGray = Color(0xFF1A1A1A)
val GoldBeige = Color(0xFFC5A47E)
val LightGray = Color(0xFFF9F9F9)
val BorderGray = Color(0xFFEEEEEE)

val GreenSuccess = Color(0xFF2D6B2D)
val RedAlert = Color(0xFFB00020)

private val LightColorScheme = lightColorScheme(
    primary = DarkGray,
    secondary = GoldBeige,
    background = LightGray,
    surface = Color.White,
    onPrimary = Color.White,
    onSecondary = DarkGray,
    onBackground = DarkGray,
    onSurface = DarkGray
)

private val DarkColorScheme = darkColorScheme(
    primary = Color.White,
    secondary = GoldBeige,
    background = DarkGray,
    surface = Color(0xFF2D2D2D),
    onPrimary = DarkGray,
    onSecondary = DarkGray,
    onBackground = Color.White,
    onSurface = Color.White
)

@Composable
fun ArtisanAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}
