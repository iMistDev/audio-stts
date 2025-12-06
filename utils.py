import os
    
INPUT_LANGUAGES = [
    {"code": "es-419", "name": "Español (Latinoamérica)"},
    {"code": "es-ES", "name": "Español (España)"},
    {"code": "en-US", "name": "English (USA)"},
    {"code": "en-GB", "name": "English (UK)"},
    {"code": "pt-BR", "name": "Português (Brasil)"},
    {"code": "fr-FR", "name": "Français"},
    {"code": "de-DE", "name": "Deutsch"},
    {"code": "it-IT", "name": "Italiano"},
    {"code": "ja-JP", "name": "Japanese (日本語)"},
    {"code": "ko-KR", "name": "Korean (한국어)"},
    {"code": "ru-RU", "name": "Russian (Pусский)"},
]

TTS_VOICES = {
    0: {"name": "Español (Latam) - Lorenzo", "code": "es-CL-LorenzoNeural"},
    1: {"name": "Español (Latam) - Dalia",   "code": "es-MX-DaliaNeural"},
    2: {"name": "Español (España) - Elvira", "code": "es-ES-ElviraNeural"},
    3: {"name": "English (US) - Jenny",       "code": "en-US-JennyNeural"},
    4: {"name": "English (US) - Guy",         "code": "en-US-GuyNeural"},
    5: {"name": "English (UK) - Sonia",       "code": "en-GB-SoniaNeural"},
    6: {"name": "Português (BR) - Francisca", "code": "pt-BR-FranciscaNeural"},
    7: {"name": "Français - Denise",          "code": "fr-FR-DeniseNeural"},
    8: {"name": "Deutsch - Katja",            "code": "de-DE-KatjaNeural"},
    9: {"name": "Italiano - Elsa",            "code": "it-IT-ElsaNeural"},
    10:{"name": "Japanese - Nanami",          "code": "ja-JP-NanamiNeural"},
    11:{"name": "Korean - SunHi",             "code": "ko-KR-SunHiNeural"},
    12:{"name": "Russian - Svetlana",         "code": "ru-RU-SvetlanaNeural"},
}

#Deprecated, loved the ASCII on CMD :(
    
"""
def cleaning():
    os.system('cls' if os.name == 'nt' else 'clear')
   
def welcome():
    art = r"""
                                                                                                                                                                
#    ,---,        ,'  , `.                       ___                  ,---,                         
#    ,`--.' |     ,-+-,.' _ |  ,--,               ,--.'|_              .'  .' `\                       
#    |   :  :  ,-+-. ;   , ||,--.'|               |  | :,'     ,---,.,---.'     \                      
#    :   |  ' ,--.'|'   |  ;||  |,      .--.--.   :  : ' :   ,'  .' ||   |  .`\  |               .---. 
#    |   :  ||   |  ,', |  ':`--'_     /  /    '.;__,'  /  ,---.'   ,:   : |  '  |   ,---.     /.  ./| 
#    '   '  ;|   | /  | |  ||,' ,'|   |  :  /`./|  |   |   |   |    ||   ' '  ;  :  /     \  .-' . ' | 
#    |   |  |'   | :  | :  |,'  | |   |  :  ;_  :__,'| :   :   :  .' '   | ;  .  | /    /  |/___/ \: | 
#    '   :  ;;   . |  ; |--' |  | :    \  \    `. '  : |__ :   |.'   |   | :  |  '.    ' / |.   \  ' . 
#    |   |  '|   : |  | ,    '  : |__   `----.   \|  | '.'|`---'     '   : | /  ; '   ;   /| \   \   ' 
#    '   :  ||   : '  |/     |  | '.'| /  /`--'  /;  :    ;          |   | '` ,/  '   |  / |  \   \    
#    ;   |.' ;   | |`-'      ;  :    ;'--'.     / |  ,   /           ;   :  .'    |   :    |   \   \ | 
#    '---'   |   ;/          |  ,   /   `--'---'   ---`-'            |   ,.'       \   \  /     '---"  
#            '---'            ---`-'                                 '---'          `----'             
#    "Shy Solutions from a shy dev."                                                                                                
""" 
    print(art)

def menu(option_list, current_config):
    while True:
        cleaning()
        welcome()
        
        print("\n----- [MAIN CONFIG.] -----")
        print(f"Microphone ID: {current_config.get('mic', 'Default')}")
        print(f"Language: {current_config.get('lang', 'Undefined')}")
        
        print("\n----- [MAIN MENU] -----")
        print("-"*22)
        
        for i, option in enumerate(option_list, 1):
            print(f"[{i}] {option}")

        print(f"[{len(option_list) + 1}] Exit")
        print("-"*22)
        
        raw_selection = input("\n>>> Choose an option: ")
        
        try:
            
            selection = int(raw_selection)

            if 1 <= selection <= len(option_list):
                return selection - 1
            elif selection == len(option_list) + 1:
                return None
            else:
                input("Invalid Option. Press Enter...")
                
        except ValueError:
            input("Please select your option. Press Enter...")
"""