import pyautogui
import pytesseract
from datetime import datetime
import os
import json
from PIL import Image
import time
import keyboard
import random
from notification import phone_alert, phone_alert_encounter
from setup import initial_setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

########################SETUP#####################
initial_setup()
config = json.load(open("config.json", "r", encoding="utf-8"))
#VARS
fight_region =(config["images"]["fight"]["x"],
               config["images"]["fight"]["y"],
               config["images"]["fight"]["width"],
               config["images"]["fight"]["height"]
               )
confirm_region=(config["images"]["confirm"]["x"],
                config["images"]["confirm"]["y"],
                config["images"]["confirm"]["width"],
                config["images"]["confirm"]["height"]
                )
turn_region=(config["images"]["turn"]["x"],
             config["images"]["turn"]["y"],
             config["images"]["turn"]["width"],
             config["images"]["turn"]["height"]
            )
poke_region=(config["images"]["poke_name"]["x"],
             config["images"]["poke_name"]["y"],
             config["images"]["poke_name"]["width"],
             config["images"]["poke_name"]["height"]
            )
heal_region=(config["pixels"]["heal"]["x"],
             config["pixels"]["heal"]["y"],
            )
heal_rgb=(config["pixels"]["heal"]["R"],
          config["pixels"]["heal"]["G"],
          config["pixels"]["heal"]["B"],          
         )

#Settings
auto_heal = config["settings"]["auto_heal"]
auto_move = config["settings"]["auto_move"]
avoid_elites = config["settings"]["avoid_elites"]
log = config["settings"]["log"]
screenshot_folder = config["settings"]["screenshot_folder"] 

##################################################
# Log Pokemon
def log_pokemon(pokemon_name, log_file='log.txt'):
  timestamp = datetime.now().strftime('%Hh-%Mm-%Ssec')
  pokemon_name= pokemon_name.strip()
  log_entry = f"~{pokemon_name}~ - {timestamp}\n"
    
  with open(log_file, 'a', encoding='utf-8') as file:
    file.write(log_entry)
##################################################
# Image Recognition logic
def image_recognition(image_path: str, log_msg: str, region=None):
    try:
        if pyautogui.locateOnScreen(image_path, confidence=0.7, region=region):
            print(log_msg)
            return True
    except:
        pass
    return False
##################################################
# Alert
def send_alert():
  global running
    
  if image_recognition('Images/confirm.png', "ALERT", region=confirm_region):
    phone_alert()
    hold_key_down('i',0)
    running = False
##################################################
# Choosing effective move logic
def choose_move():
  # Wait time for moves to appear
  time.sleep(0.2)
  if auto_move:
      
    #4x
    try:
        move_position = pyautogui.locateCenterOnScreen('Moves/VEffective.png', confidence=0.8)
        if move_position:
            print('4x Move Found!')
            pyautogui.click(move_position)
            time.sleep(0.1)
            pyautogui.click(move_position)
            return #Stop
    except:
      pass
    
    #2x
    try:
        move_position = pyautogui.locateCenterOnScreen('Moves/Effective.png', confidence=0.8)
        if move_position:
            print('2x Move Found!')
            pyautogui.click(move_position)
            time.sleep(0.1)
            pyautogui.click(move_position)
            return #Stop
    except:
      pass
    
    #1x
    try:
        move_position = pyautogui.locateCenterOnScreen('Moves/Normal.png', confidence=0.8)
        if move_position:
            print('1x Move Found!')
            pyautogui.click(move_position)
            time.sleep(0.1)
            pyautogui.click(move_position)
            return #Stop
    except:
      pass
  else:
    #Use first move
    hold_key_down('1',0)  
##################################################
def heal():
  if auto_heal:
    #Healthy
    if pyautogui.pixel(heal_region[0],heal_region[1]) == heal_rgb:
      pass
    else:
      try:
        #Not Healthy
        while pyautogui.pixel(heal_region[0],heal_region[1]) != heal_rgb and not image_recognition('Images/Turn.png','Fight In Progress - not healing!',region=turn_region):
          potion_position = pyautogui.locateCenterOnScreen('Images/Potion.png', confidence=0.8)
          if potion_position:
            print('Healing Pokemon!')
            print('Potion Found!')
            offset_x = 30
            pyautogui.moveTo(potion_position.x + offset_x, potion_position.y)
            time.sleep(0.2)
            pyautogui.click(potion_position.x + offset_x, potion_position.y)
            pyautogui.moveTo(heal_region[0],heal_region[1])
            time.sleep(0.2)
            pyautogui.click(heal_region[0],heal_region[1])
      except:
        print('Potion Not Found!')
        pass
##################################################
# Pokemon recognition system                                                                          
def take_screenshot(screenshot_folder, left, top, width, height):                                     
                                                                                                      
    screenshot = pyautogui.screenshot(region=(left, top, width, height))                              
    timestamp = datetime.now().strftime('%H-%M-%S')                                                   
    filename = f"PPO {timestamp}.png"                                                                 
    filepath = os.path.join(screenshot_folder, filename)                                              
                                                                                                      
    # Save the screenshot to the specified filepath                                                   
    screenshot.save(filepath)                                                                         
                                                                                                      
    # Preprocess image (convert to grayscale and apply thresholding)                                  
    preprocessed_image = Image.open(filepath).convert('L')  # Convert to grayscale                    
    # preprocessed_image = Image.open(filepath).point(lambda x: 0 if x < 128 else 255)                    
                                                                                                      
    # Use pytesseract to perform OCR and extract text                                                 
    extracted_text = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz[]')
                                                                                                                                                                          
    print("Extracted Text:")                                                                
    print(f"~{extracted_text.strip()}~")                                                      
                                                                                                      
    # Debugging Image                                                                                                                                                     
    # preprocessed_image.show()                                                                       
                                                                                                      
    # Delete the Image
    os.remove(filepath)   

    return extracted_text
##################################################
# Key Hold Function

#Special
def wander(duration, mode="left_right" ,check_interval=0.1):
  
#Wandering mode
  if mode == "left_right":
    button1 = 'a'
    button2 = 'd'
  else:
    button1 = "w"
    button2 = "s"  
  
#First Button
  keyboard.press(button1)
  start_time = time.time()
    
  while time.time() - start_time < duration:
      # Check if fightbutton is there while moving
      if image_recognition('Images/FightButton.PNG',"", region=fight_region):
          keyboard.release(button1)
          return True
        
      # Throttle
      time.sleep(check_interval)
    
  keyboard.release(button1)
    
#Second Button
  keyboard.press(button2)
  start_time = time.time()
    
  while time.time() - start_time < duration:
      # Check if fightbutton is there while moving
      if image_recognition('Images/FightButton.PNG',"", region=fight_region):
          keyboard.release(button2)
          return True
        
      # Throttle
      time.sleep(check_interval)
    
  keyboard.release(button2)    
  return False

#Normal  
def hold_key_down(key, duration):
    
  #Vars
  keyboard.press(key)
  time.sleep(duration)
  keyboard.release(key)
#####################################################
# Main Loop 
 
running = True
def on_key_release(event):
    global running
    if event.name == 'q':
        running = False

# Set up a keyboard event listener
keyboard.on_release(on_key_release)

while running:
  if image_recognition('Images/FightButton.PNG', 'Button Visible!', fight_region) :

    # While Fighting
    pyautogui.moveTo(1100,500)

    #Take Screenshot and store pokemon names
    pokemon_name = take_screenshot(screenshot_folder, poke_region[0], poke_region[1], poke_region[2], poke_region[3]) 
    is_elite="[E]" in pokemon_name or "[" in pokemon_name or "]" in pokemon_name
    avoidable_pokemon = {
                        }
    viable_pokemon = {"[S]",
                      "Xerneas",
                      "ern",
                     }
    #Log Pokemon
    if log:
      log_pokemon(pokemon_name)     
      
    if any(poke in pokemon_name for poke in viable_pokemon) or image_recognition('Images/SpecialEncounter.png', 'Special Encounter!'):
      #Stop
      running = False
      phone_alert_encounter()  
        
    elif (is_elite and avoid_elites) or any(poke in pokemon_name for poke in avoidable_pokemon):
      #Run
      hold_key_down('4',0)

    else:
      #Fight
      hold_key_down('1',0)
      choose_move()

  else:
    #Alertd
    send_alert()
    
    #Heal
    heal()

    #Wander around 0.2682(2) 0.1341(1)
    random_int = random.randint(1,6)
    duration = 0.1341*random_int

    # print('Image not found on the screen')
    if wander(duration, config["settings"]["mode"]):
      continue #Reset main loop

print("Script stopped.")    

#####################################################