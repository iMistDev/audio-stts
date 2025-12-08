import eel
import threading
import vtt_module as vt
import tts_module as tt
import utils
import json
import os
import keyboard
import sys
import audio_engine as au

log_path= "debug.log"
sys.stdout= open(log_path, 'w', encoding='utf-8', buffering=1)
sys.stderr= open(log_path, 'w', encoding='utf-8', buffering=1)

print("--- [DEBUG] Session Started ---")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

eel.init(resource_path('web'))
CONFIG_FILE = "user_config.json"

default_config = {
    "mic": 0,
    "voice" : 0,
    "lang": "en",
    "volume": 50,
    "sensitivity": 20,
    "hotkey": "f9",
    "model_size": "small"
}

app_config = default_config.copy()

def load_config():
    global app_config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
                app_config.update(loaded)
        except: pass
        
def save_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(app_config, f, indent=4)
    except: pass
    
load_config()
active_stream = False

def toggle_stream():
    global active_stream
    if active_stream:
        stop_stream()
        eel.js_trigger_stop()
    else:
        start_stream()
        
def set_hotkey(hotkey_str):
    try:
        keyboard.unhook_all_hotkeys()
    except AttributeError:
        pass
    except Exception as e:
        print(f"--- [WARN] Error while cleaning hotkeys: {e} ---")
        
    try:
        keyboard.add_hotkey(hotkey_str, toggle_stream)
        print(f"--- [HOTKEY] Activated: {hotkey_str} ---")
    except Exception as e:
        print(f"--- [ERROR] Can't asign hotkey: '{hotkey_str}': {e} ---")    
    
set_hotkey(app_config["hotkey"])

@eel.expose
def update_config(key, value):
    print(f"[UI] Config {key}: {value}")
    val = int(value) if str(value).isdigit() else value
    app_config[key] = val
    save_config()
    
@eel.expose
def update_hotkey(hotkey_str):
    try:
        set_hotkey(hotkey_str)
        app_config["hotkey"] = hotkey_str
        save_config()
        return True
    except: return False
    
@eel.expose
def start_stream():
    global active_stream
    if active_stream: return
    
    active_stream = True
    
    t = threading.Thread(
        target=au.run_engine,
        args=(lambda: active_stream, lambda: app_config),
        daemon=True
    )
    t.start()
    
@eel.expose
def stop_stream():
    global active_stream
    active_stream = False
    
@eel.expose
def get_init_data():
    return {
        "mics": vt.select_mic(),
        "voices": tt.list_voices(),
        "languages": utils.INPUT_LANGUAGES,
        "config": app_config
    }
    
if sys.platform in ['win32', 'cygwin']: browser = 'edge'
else: browser = 'chrome'

try:
    eel.start('index.html', size=(680, 980), mode=browser, port=0)
except EnvironmentError:
    eel.start('index.html', size=(680, 980), mode='default', port=0)