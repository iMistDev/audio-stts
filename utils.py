import os

AVAILABLE_LANGUAGES = {
    "1": {"name": "Español (España)", "code": "es-ES"},
    "2": {"name": "Español (LatAm)", "code": "es-419"},
    "3": {"name": "English (US)", "code": "en-US"},
    "4": {"name": "Japanese", "code": "ja-JP"}
}

def cleaning():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def welcome():
    art = r"""
                                                                                                                                                                
    ,---,        ,'  , `.                       ___                  ,---,                         
    ,`--.' |     ,-+-,.' _ |  ,--,               ,--.'|_              .'  .' `\                       
    |   :  :  ,-+-. ;   , ||,--.'|               |  | :,'     ,---,.,---.'     \                      
    :   |  ' ,--.'|'   |  ;||  |,      .--.--.   :  : ' :   ,'  .' ||   |  .`\  |               .---. 
    |   :  ||   |  ,', |  ':`--'_     /  /    '.;__,'  /  ,---.'   ,:   : |  '  |   ,---.     /.  ./| 
    '   '  ;|   | /  | |  ||,' ,'|   |  :  /`./|  |   |   |   |    ||   ' '  ;  :  /     \  .-' . ' | 
    |   |  |'   | :  | :  |,'  | |   |  :  ;_  :__,'| :   :   :  .' '   | ;  .  | /    /  |/___/ \: | 
    '   :  ;;   . |  ; |--' |  | :    \  \    `. '  : |__ :   |.'   |   | :  |  '.    ' / |.   \  ' . 
    |   |  '|   : |  | ,    '  : |__   `----.   \|  | '.'|`---'     '   : | /  ; '   ;   /| \   \   ' 
    '   :  ||   : '  |/     |  | '.'| /  /`--'  /;  :    ;          |   | '` ,/  '   |  / |  \   \    
    ;   |.' ;   | |`-'      ;  :    ;'--'.     / |  ,   /           ;   :  .'    |   :    |   \   \ | 
    '---'   |   ;/          |  ,   /   `--'---'   ---`-'            |   ,.'       \   \  /     '---"  
            '---'            ---`-'                                 '---'          `----'             
    "Shy Solutions from a shy dev."                                                                                                
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