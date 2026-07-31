use std::process::{Child, Command};
use std::sync::Mutex;
use tauri::{Manager, State};

struct BackendProcess(Mutex<Option<Child>>);

/// Spawn the Python backend sidecar on a random-ish fixed port.
fn start_backend() -> Option<Child> {
    // In production, Tauri bundles the Python backend as a sidecar binary.
    // In dev, we start it directly via `python backend/main.py`.
    let port = "54321";
    std::env::set_var("AGDALUS_PORT", port);

    #[cfg(debug_assertions)]
    let child = Command::new("python")
        .args(["backend/main.py"])
        .spawn();

    #[cfg(not(debug_assertions))]
    let child = Command::new("agdalus-backend") // sidecar binary name
        .spawn();

    match child {
        Ok(c) => {
            // Give the server a moment to bind
            std::thread::sleep(std::time::Duration::from_millis(800));
            Some(c)
        }
        Err(e) => {
            eprintln!("Failed to start backend: {e}");
            None
        }
    }
}

#[tauri::command]
fn get_backend_port() -> String {
    std::env::var("AGDALUS_PORT").unwrap_or_else(|_| "54321".to_string())
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_shell::init())
        .manage(BackendProcess(Mutex::new(None)))
        .setup(|app| {
            let state: State<BackendProcess> = app.state();
            let child = start_backend();
            *state.0.lock().unwrap() = child;
            Ok(())
        })
        .on_window_event(|_window, event| {
            // Kill backend when app closes
            if let tauri::WindowEvent::CloseRequested { .. } = event {}
        })
        .invoke_handler(tauri::generate_handler![get_backend_port])
        .run(tauri::generate_context!())
        .expect("error running Agdalus");
}
