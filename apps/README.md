# Plataforma de Artesanos Aylesva MX — Guía de Configuración

Este directorio contiene los códigos base de la aplicación de **Android para Artesanos** y la aplicación de **macOS para el Administrador**. Ambas aplicaciones se comunican en tiempo real mediante **Firebase (Firestore + Storage)**.

---

## 1. Configuración de Firebase (Consola de Firebase)

Para que las aplicaciones puedan comunicarse y subir fotos, debes crear y configurar un proyecto en la consola de Firebase:

1. Ve a [Firebase Console](https://console.firebase.google.com/) y haz clic en **Agregar proyecto**. Nómbralo `Aylesva Artesanos`.
2. Una vez creado, ve al menú izquierdo y activa los siguientes servicios:
   
   *   **Cloud Firestore**:
       *   Haz clic en **Crear base de datos**.
       *   Selecciona **Comenzar en modo de prueba** (para permitir lecturas/escrituras durante el desarrollo) y haz clic en siguiente.
       *   Elige una ubicación cercana (ej. `us-central1` o `nam5`) y actívala.
   *   **Cloud Storage**:
       *   Haz clic en **Comenzar** y sigue el asistente en modo de prueba.

### Reglas de Seguridad (Recomendadas para desarrollo):

#### Firestore Rules:
En la pestaña **Reglas (Rules)** de Firestore, asegúrate de tener configurado lo siguiente para permitir leer y escribir libremente:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

#### Storage Rules:
En la pestaña **Reglas (Rules)** de Storage, configura:
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if true;
    }
  }
}
```

---

## 2. Configuración de la App Android (Artesanos)

La aplicación de Android está configurada con el paquete `com.aylesva.artisan` y utiliza Kotlin + Jetpack Compose con arquitectura MVVM.

1. En la consola de Firebase, haz clic en el icono de **Android** para agregar una app al proyecto.
2. Registra el nombre de paquete: **`com.aylesva.artisan`**.
3. Descarga el archivo **`google-services.json`**.
4. Copia el archivo y pégalo dentro de la carpeta del proyecto en:
   `apps/artisan-app-android/app/google-services.json`
5. Abre **Android Studio**.
6. Selecciona **Open** (Abrir) y elige la carpeta: `/apps/artisan-app-android`.
7. Deja que Gradle descargue las dependencias y sincronice el proyecto.
8. Ejecuta la app en un emulador o dispositivo Android físico.

---

## 3. Configuración de la App macOS (Administrador)

La app de macOS se ejecuta de forma nativa. Sigue estos pasos para configurarla en Xcode:

### Paso A: Crear el Proyecto en Xcode
1. Abre **Xcode** en tu Mac.
2. Haz clic en **File > New > Project...**
3. Selecciona la pestaña **macOS** y elige **App**.
4. Configura el proyecto con:
   *   **Product Name**: `AdminApp`
   *   **Organization Identifier**: `com.aylesva` (generará el Bundle ID: `com.aylesva.AdminApp`)
   *   **Interface**: `SwiftUI`
   *   **Language**: `Swift`
5. Guarda el proyecto dentro de la carpeta: `apps/admin-app-macos/`

### Paso B: Agregar Firebase SDK (Swift Package Manager)
1. En Xcode, ve a **File > Add Package Dependencies...**
2. En la barra de búsqueda superior derecha, pega la URL de Firebase:
   `https://github.com/firebase/firebase-ios-sdk`
3. En la sección de Dependency Rule, selecciona "Up to Next Major Version".
4. Haz clic en **Add Package**.
5. En la lista de paquetes que se muestra, selecciona:
   *   `FirebaseFirestore`
   *   `FirebaseFirestoreSwift`
6. Haz clic en **Add Package** para finalizar la descarga de dependencias.

### Paso C: Registrar la App en Firebase
1. En la consola de Firebase, haz clic en **Agregar app** y selecciona el icono de **iOS/Apple**.
2. Registra el Bundle ID exacto de tu proyecto de Xcode (ej. `com.aylesva.AdminApp`).
3. Descarga el archivo **`GoogleService-Info.plist`**.
4. Arrastra y suelta el archivo `GoogleService-Info.plist` dentro de la barra lateral de Xcode, asegurándote de que la casilla **"Copy items if needed"** esté marcada y esté seleccionado el Target `AdminApp`.

### Paso D: Reemplazar los Archivos de Código
Reemplaza o arrastra los archivos de la carpeta `apps/admin-app-macos/Source/` al panel de navegación de tu proyecto Xcode para sobreescribir la plantilla base:
*   [AdminApp.swift](file:///Users/alexdoven/Desktop/PROYECTOS%20VARAL/aylesva_respaldo_desarrollo/apps/admin-app-macos/Source/AdminApp.swift) (Reemplaza el archivo principal de tu app)
*   [ContentView.swift](file:///Users/alexdoven/Desktop/PROYECTOS%20VARAL/aylesva_respaldo_desarrollo/apps/admin-app-macos/Source/ContentView.swift) (Reemplaza la vista por defecto)
*   [Models.swift](file:///Users/alexdoven/Desktop/PROYECTOS%20VARAL/aylesva_respaldo_desarrollo/apps/admin-app-macos/Source/Models.swift) (Añádelo al proyecto)
*   [FirebaseService.swift](file:///Users/alexdoven/Desktop/PROYECTOS%20VARAL/aylesva_respaldo_desarrollo/apps/admin-app-macos/Source/FirebaseService.swift) (Añádelo al proyecto)
*   [ProductViewModel.swift](file:///Users/alexdoven/Desktop/PROYECTOS%20VARAL/aylesva_respaldo_desarrollo/apps/admin-app-macos/Source/ProductViewModel.swift) (Añádelo al proyecto)
*   [ShopifyClient.swift](file:///Users/alexdoven/Desktop/PROYECTOS%20VARAL/aylesva_respaldo_desarrollo/apps/admin-app-macos/Source/ShopifyClient.swift) (Añádelo al proyecto)

5. Compila y ejecuta la aplicación de macOS haciendo clic en el botón de **Play** (Run) en Xcode.
