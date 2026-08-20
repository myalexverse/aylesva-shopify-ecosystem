import SwiftUI
import FirebaseCore

@main
struct AdminApp: App {
    
    init() {
        // Configure Firebase SDK on app launch
        // Requires GoogleService-Info.plist to be added to the Xcode target
        FirebaseApp.configure()
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 900, minHeight: 600)
        }
    }
}
