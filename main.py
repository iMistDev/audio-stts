import utils
import vtt_module
import tts_module
import time

def run():
    config = {
        "mic": 0,
        "lang": "es-419",
        "voice": 0
    }
    
    opts = [
        "Configure Microphone",
        "Configure Language",
        "Configure Voice (TTS)",
        "RUN STREAM MODE (Echo)"
    ]
    
    while True:
        choice = utils.menu(opts, config)
        
        if choice is None:
            utils.cleaning()
            print("\nGoodbye! See you next time!")
            time.sleep(1)
            break
        
        elif choice == 0:
            config["mic"] = vtt_module.select_mic()
        elif choice == 1:
            config["lang"] = vtt_module.select_language()
        elif choice == 2:
            config["voice"] = tts_module.select_voice()
        elif choice == 3:
            utils.cleaning()
            print("--- [NOW RUNING STREAMER MODE (CTRL+C BREAKS)] ---")
            try:
                while True:
                    
                    text = vtt_module.hear_function(config["mic"], config["lang"])
                    
                    if text:
                        tts_module.speak(text, config["voice"])
                        
            except KeyboardInterrupt:
                pass
            
if __name__ == "__main__":
    run()