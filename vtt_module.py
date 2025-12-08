import io
import os
import pyaudio

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("--- [ERROR] faster-whisper library not installed. ---")
    
model = None
current_model_size = None

def init_whisper(model_size="small", device="cpu", compute_type="int8"):
    global model, current_model_size
    
    if not WHISPER_AVAILABLE: return False
    
    if model and current_model_size == model_size:
        return True
    
    print(f"--- [WHISPER] Loading Model: '{model_size}' on {device}... ---")
    
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type, cpu_threads=4)
        current_model_size = model_size
        print("--- [WHISPER] Model Loaded and ready. ---")
        return True
    except Exception as e:
        print(f"--- [WHISPER ERROR] Fail loading Whisper: {e} ---")
        
def transcript(audio_data, prompt="", lang_code="en"):
    global model
    if not model: return None
    
    try:
        wav_bytes = audio_data.get_wav_data()
        wav_stream = io.BytesIO(wav_bytes)
        
        lang_target = lang_code if lang_code else "en"
        clean_lang = lang_target.split('-')[0]
        
        if isinstance(prompt, (list, tuple)):
            prompt = " ".join(prompt)
        
        segments, _ = model.transcribe(
            wav_stream,
            beam_size=1,
            best_of=1,
            temperature=0.0,
            language=clean_lang,
            initial_prompt=prompt,
            vad_filter=True,
            condition_on_previous_text=False   
        )
        
        text = "".join([segment.text for segment in segments]).strip()
        return text if len(text) > 0 else None
    
    except Exception as e:
        print(f"Error on Transcription: {e}")
        return None
    
def select_mic():
    p = pyaudio.PyAudio()
    info_devices = []
    
    seen_core_names = set()
    
    print("\n----- [ Scanning Audio Devices ] -----")
    
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        name = dev.get('name')
        input_channels = dev.get('maxInputChannels')
        
        ignore_words = ["Microphone", "Micrófono", "Input", "Entrada", "Dispositivo de High Definition Audio"]
        
        clean_name = name
        for word in ignore_words:
            clean_name = clean_name.replace(word, "").strip()
        
        if (input_channels > 0 and
            clean_name not in seen_core_names and
            "Asignador" not in name and
            "Controlador primario" not in name and
            "Stereo Mix" not in name):
            
            seen_core_names.add(clean_name)
            info_devices.append({"id": i, "name": f"{clean_name} (ID: {i}) "})
            
    p.terminate()
    return info_devices