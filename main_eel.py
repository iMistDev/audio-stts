import eel
import threading
import vtt_module
import tts_module
import utils
import json
import os
import keyboard
import sys
import audio_engine as en

eel.init('web')

CONFIG_FILE = "user_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r')as f:
                return json.load(f)
        except Exception as e:
            print(f"Error while loading config: {e}")
    return None

def save_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(app_config, f, indent=4)
        print("--- [SYS] Saved Config. ---")
    except Exception as e:
        print(f"--- Error saving config: {e} ---")

default_config = {
    "mic": 0,
    "lang": "es-419",
    "voice": 0,
    "volume": 50,
    "sensitivity": 20,
    "hotkey": "f9"
}

saved_config = load_config()

if saved_config:
    app_config = saved_config
    print(f"--- [SYS] Config. Loaded: {app_config} ---")
else:
    app_config = default_config
    print("--- [SYS] Defatult configuration selected. ---")

active_stream = False

def toggle_stream():
    global active_stream
    if active_stream:
        print("--- [HOTKEY] Stopping stream... ---")
        stop_stream()
        eel.js_trigger_stop()
    else:
        print("--- [HOTKEY] Startig stream... ")
        start_stream()
        eel.js_trigger_start()

@eel.expose
def update_hotkey(hotkey_str):
    print(f"[HOTKEY] Setting Global Hotkey to: {hotkey_str}")
    
    keyboard.unhook_all_hotkeys()
    
    try:
        keyboard.add_hotkey(hotkey_str, toggle_stream)
        
        app_config["hotkey"] = hotkey_str
        save_config()
        return True
    except Exception as e:
        print(f"Error setting hotkey: {e}")
        return False
    
current_hotkey = app_config.get("hotkey", "f9")
try:
    keyboard.add_hotkey(current_hotkey, toggle_stream)
    print(f"--- [SYS] Initial Hotkey loaded as: {current_hotkey}")
except:
    print(" --- [WARN] Can't load the initial hotkey ---")


@eel.expose
def stop_stream():
    global active_stream
    print("--- [PY] STOP signal Recived. ---")
    active_stream = False

@eel.expose
def update_config(key, value):
    print(f"[UI] Changin {key} to {value}")
    if str(value).isdigit():
        app_config[key] = int(value)
    else:
        app_config[key] = value
    save_config()

@eel.expose
def start_stream():
    global active_stream
    
    if active_stream:
        return
    print("--- [PY] Start button pressed, Attempting Thread... ---")
    eel.js_log(">>> STARTING UP...")
    
    active_stream = True
    
    t = threading.Thread(
        target=en.run_engine,
        args=(
            lambda: active_stream, lambda: app_config
        ),
        daemon= True
    )

    t.start()

    print("--- [PY] Thread started succesfully. ---")
    
@eel.expose
def get_lists():
    print("Sending devices lists...")
    try:
        
        print(" -> Searching Microphones...")
        mics = vtt_module.select_mic()
        print(f" -> Microphones found!: {len(mics)}")
        print(" -> Searching Voices...")
        voices = tts_module.list_voices()
        print(f" -> Voices found!: {len(voices)}")
        
        input_langs = utils.INPUT_LANGUAGES
    
        return{
        "mics":mics,
        "voices":voices,
        "languages": input_langs,
        "config": app_config
        }
    
    except Exception as e:
        print(f"Critical Error on method get_lists(): {e}")
        return {"mics": [], "voices": []}
    
                
import sys
if sys.platform in ['win32', 'cygwin']:
    browser = 'edge'
else:
    browser = 'chrome'
    
print(f"--- [SYS] Initializing in mode: {browser} ---")

try:
    eel.start('index.html', size=(680, 980), mode=browser, port= 0)
except EnvironmentError:
    print("--- [WARN/SYS] Browser not found, using users default. ---")
    eel.start('index.html', size=(680, 980), mode='default', port= 0)
