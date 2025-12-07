import speech_recognition as sr
import vtt_module
import tts_module
import asyncio
import eel

def calculate_tresh(percent):
    MIN_AUDIO = 300
    MAX_AUDIO = 4000
    
    return MIN_AUDIO + (percent * (MAX_AUDIO - MIN_AUDIO) / 100)

def run_engine(is_active_func, get_config_func):
    print("--- [THREAD] Starting audio Engine... ---")
    
    r = sr.Recognizer()
    r.pause_threshold = 0.6
    r.non_speaking_duration = 0.4
    r.dynamic_energy_threshold = False
    
    cfg = get_config_func()
    
    try:
        mic_id = cfg["mic"]
        device = mic_id if mic_id is not None else None
        
        with sr.Microphone(device_index=device) as source:
            
            eel.js_log("--- [SYS] Sistem Ready. ---")
            eel.js_log("--- [SYS] Remember to check your Mic Sensitivity ---")
            eel.js_log("--- [SYS] Now start Speaking... ---")
            
            while is_active_func():
                try:
                    cfg = get_config_func()
                    
                    user_percent = cfg.get("sensitivity", 20)
                    real_threshold = calculate_tresh(user_percent)
                    
                    r.energy_threshold = real_threshold
                    
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=8)
                    except sr.WaitTimeoutError:
                        continue
                
                    if not is_active_func():
                        print("--- [THREAD] Stop detected after listening. ---")
                        break
                 
                    eel.js_log("--- [SYSTEM] Processing... ---")
                
                    text = vtt_module.audio_processing(r, audio, cfg["lang"])
                
                    if text:
                        eel.js_log(f" >Your Microphone: {text}")
                        if is_active_func():
                            eel.js_log(f" >Your voice: {text}")
                            asyncio.run(tts_module.speak(text, cfg["voice"], cfg["volume"]))
                            eel.js_log("Listening...")
                except Exception as e:
                    print(f"Error on Engine Loop: {e}")
                    if is_active_func():
                        eel.js_log(f"Error: {e}")
    except Exception as e:
        eel.js_log(f" --- [ERROR] Critical error while opening mic: {e}")
        print(f"--- [SYSTEM] CRITICAL ERROR: {e} ---")
        
    eel.js_log("--- [SYSTEM] SHUTDOWN SYSTEM ---")
    print("--- [THREAD] Thread finished. ---")