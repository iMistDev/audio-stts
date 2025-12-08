// --- VARIABLES GLOBALES ---
let lastStatus = ""; // Para evitar spam en la consola

// --- INICIALIZACIÓN ---
window.onload = async function() {
    let data = await eel.get_init_data()();
    
    if (data) {
        populateSelect("micSelect", data.mics, data.config.mic);
        populateSelect("voiceSelect", data.voices, data.config.voice);
        populateSelect("langSelect", data.languages, data.config.lang);
        
        document.getElementById("sensInput").value = data.config.sensitivity;
        document.getElementById("sensLabel").innerText = data.config.sensitivity + "%";
        
        document.getElementById("volInput").value = data.config.volume;
        document.getElementById("volLabel").innerText = data.config.volume + "%";
        
        document.getElementById("hotkeyInput").value = data.config.hotkey;
        document.getElementById("modelSelect").value = data.config.model_size || "small";
    }
};

function populateSelect(id, items, selectedValue) {
    let select = document.getElementById(id);
    select.innerHTML = "";
    items.forEach(item => {
        let option = document.createElement("option");
        option.value = item.id !== undefined ? item.id : item.code;
        option.text = item.name !== undefined ? item.name : item.lang;
        select.appendChild(option);
    });
    if (selectedValue !== undefined) select.value = selectedValue;
}

// --- COMUNICACIÓN CON PYTHON ---

function updateConfig(key, value) {
    eel.update_config(key, value);
}

function uiUpdateSens(val) {
    document.getElementById("sensLabel").innerText = val + "%";
    updateConfig('sensitivity', val);
}

function uiUpdateVol(val) {
    document.getElementById("volLabel").innerText = val + "%";
    updateConfig('volume', val);
}

async function saveHotkey() {
    let val = document.getElementById("hotkeyInput").value;
    let success = await eel.update_hotkey(val)();
    if(success) logToConsole("✅ Hotkey updated: " + val);
    else logToConsole("❌ Invalid Hotkey", "log-err");
}

function startSystem() {
    eel.start_stream(); 
}

function stopSystem() {
    eel.stop_stream();
}

// --- FUNCIONES EXPUESTAS (Llamadas desde Python) ---

eel.expose(js_log);
function js_log(msg) {
    logToConsole(msg);
}

eel.expose(js_set_status);
function js_set_status(status) {
    let light = document.getElementById('status-light');
    let btnStart = document.getElementById('btnStart');
    let btnStop = document.getElementById('btnStop');

    // 1. Manejo Visual de la Luz
    light.className = ''; // Reset

    if (status === 'loading') {
        light.classList.add('status-loading');
        btnStart.disabled = true;
        btnStart.innerText = "LOADING SYSTEM...";
        btnStart.style.display = "inline-block";
        btnStop.style.display = "none";
    }
    else if (status === 'ready') {
        light.classList.add('status-ready');
    }
    else if (status === 'stopped') {
        btnStart.disabled = false;
        btnStart.innerText = "START STREAMING";
        btnStart.style.display = "inline-block";
        btnStop.style.display = "none";
    }
    else {
        // Estados activos
        btnStart.style.display = "none";
        btnStop.style.display = "inline-block";
        btnStop.disabled = false;

        if (status === 'listening') light.classList.add('status-listening');
        if (status === 'processing') light.classList.add('status-processing');
        if (status === 'speaking') light.classList.add('status-speaking');
    }

    // 2. Manejo de Logs en Consola (Solo si el estado cambió)
    if (status !== lastStatus) {
        lastStatus = status; // Actualizamos el tracker

        switch(status) {
            case 'listening':
                logToConsole("🎤 Listening...", "log-listen");
                break;
            case 'processing':
                logToConsole("⚙️ Processing audio...", "log-process");
                break;
            case 'speaking':
                logToConsole("🔊 Playing audio...", "log-speak");
                break;
            case 'stopped':
                logToConsole("🛑 System Stopped", "log-err");
                break;
            case 'ready':
                logToConsole("⚡ System Ready - Press Start", "log-sys");
                break;
            case 'loading':
                logToConsole("⏳ Initializing models...", "log-sys");
                break;
        }
    }
}

// Triggers de prueba
eel.expose(js_trigger_start);
function js_trigger_start() {
    js_set_status('listening');
    logToConsole(">>> SYSTEM LIVE - MANUAL TRIGGER");
}

eel.expose(js_trigger_stop);
function js_trigger_stop() {
    js_set_status('stopped');
}

// --- UTILIDAD DE LOG ACTUALIZADA ---
// Ahora acepta un segundo parámetro opcional para la clase CSS
function logToConsole(text, cssClass = "") {
    let consoleDiv = document.getElementById("console");
    let p = document.createElement("div");
    
    p.className = "log-line";
    if (cssClass) {
        p.classList.add(cssClass);
    }

    // Agregamos timestamp simple para que se vea más técnico
    let time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: "numeric", minute: "numeric", second: "numeric" });
    p.innerText = `[${time}] ${text}`;
    
    consoleDiv.appendChild(p);
    consoleDiv.scrollTop = consoleDiv.scrollHeight;
}