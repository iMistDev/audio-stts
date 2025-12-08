import speech_recognition as sr
import vtt_module as vt
import tts_module as tt
import asyncio
import eel
import keyboard as k
import sanitizer as sa

def run_engine(is_active_func, get_config_func):
    print("---- [AUDIO ENGINE V2.0] Starting... ---")
    
    eel.js_set_status("loading")
    cfg = get_config_func()
    model_size = cfg.get("model_size", "small")
    
    if not vt.init_whisper(model_size=model_size):
        eel.js_log("--- [FATAL ERROR] Can't load the AI. ---")
        eel.js_set_status("stopped")
        eel.js_trigger_stop()
        return
    
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.pause_threshold = 0.6
    r.non_speaking_duration = 0.2
    r.phrase_threshold = 0.3
    
    eel.js_set_status("ready")
    eel.js_trigger_start()
    
    try:
        mic_id = cfg["mic"]
        device = mic_id if mic_id is not None else None
        
        with sr.Microphone(device_index=device) as source:
            
            eel.js_log(f"--- [SYSTEM ALIVE] Mode: {model_size.upper()} ---")
            
            while is_active_func():
                cfg = get_config_func()
                
                sens = cfg.get("sensitivity", 20)
                r.energy_threshold = 300 + (sens * 37)
                
                try:
                    #Pending some adjustments on the third argument
                    audio = r.listen(source, timeout=1, phrase_time_limit=None)
                except sr.WaitTimeoutError:
                    continue
                
                if not is_active_func(): break
                
                eel.js_set_status("processing")
                
                text_raw = vt.transcript(audio, prompt=sa.VOCABULARY)
                
                if text_raw:
                    
                    text = sa.sanitize_text(text_raw)
                    
                    if len(text) < 3 and text.lower() not in sa.VALID_SHORT_WORDS:
                        eel.js_set_status("listening")
                        continue
                    
                    eel.js_log(f">>> Your Microphone: {text}")
                    
                    if is_active_func():
                        eel.js_set_status("Speaking")
                        asyncio.run(tt.speak(text, cfg["voice"], cfg["volume"]))
                
                eel.js_set_status("listening")
    except Exception as e:
        eel.js_log(f"--- [CRASH ERROR]: {e} ---")
        print(f"--- [CRASH ERROR]: {e} ---")
        
    eel.js_set_status("stopped")
    eel.js_trigger_stop()
    print("--- [AUDIO ENGINE V2.0] Shutdown ---")