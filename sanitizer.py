import re

VOCABULARY = (
    "Vtuber, Virtual YouTuber, gankear, farmear, lootear, noob, lag, "
    "streamear, raidear, tryhard, banear, buffear, nerfear, counter, "
    "mainear, rushear, kitear, ultea, GG, WP, F, stunear, carry, "
    "build, ranked, smurf, troll, afk, "
    "Zentreya, Ironmouse, chibidoki, Korone, "
    "Inugami, Ookami Mio, Hololive, Nijisanji, Japan Culture"
)

VALID_SHORT_WORDS = [
    #esp
    "si", "no", "ok", "y", "o", "ir", "va", "ya",
     #eng
    "hi", "yo", "go", "wp", "ez", "ty", "gg", "id", "k", "up",
    #1 letter stuff
    "f", "x","d"
]

def sanitize_text(text):
    
    if not text:
        return ""
    
    text = re.sub(r'\b[Bb][e]?[-\s]?[tT]uber\b', 'Vtuber', text, flags=re.IGNORECASE)
    
    text = re.sub(r'\bfarm\s?ear\b', 'farmear', text, flags=re.IGNORECASE)

    text = re.sub(r'\bloot\s?ear\b', 'lootear', text, flags=re.IGNORECASE)
    
    text = re.sub(r'\bmain\s?ear\b', 'mainear', text, flags=re.IGNORECASE)
    text = re.sub(r'\brush\s?ear\b', 'rushear', text, flags=re.IGNORECASE)
    text = re.sub(r'\bban\s?ear\b', 'banear', text, flags=re.IGNORECASE)
    
    text = text.strip()
    if text:
        text = text[0].upper()+ text[1:]
        
    return text