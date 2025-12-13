import pyautogui
import pytesseract
from datetime import datetime
import os
from PIL import Image
import time
import keyboard
from random import uniform
from notifcation import phone_alert
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

##################################################
# Log Pokemon
def log_pokemon(pokemon_name, log_file='log.txt'):
  timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
  log_entry = f"~{pokemon_name}~ - {timestamp}\n"
    
  with open(log_file, 'a', encoding='utf-8') as file:
    file.write(log_entry)
################################################## 'Images/SpecialEncounter.png 'Special Encounter!'
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
    
  if image_recognition('Images/confirm.png', "ALERT"):
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
    x = 897
    y = 152
    #Healthy
    if pyautogui.pixel(x,y) == (165, 65, 66):
      pass
    else:
      try:
        #Not Healthy
        while pyautogui.pixel(x,y) != (165, 65, 66) and not image_recognition('Images/FightButton.PNG','Fight In Progress, not healing!'):
          potion_position = pyautogui.locateCenterOnScreen('Images/Potion.png', confidence=0.8)
          if potion_position:
            print('Healing Pokemon!')
            print('Potion Found!')
            offset_x = 30
            pyautogui.moveTo(potion_position.x + offset_x, potion_position.y)
            time.sleep(0.2)
            pyautogui.click(potion_position.x + offset_x, potion_position.y)
            pyautogui.moveTo(x,y)
            time.sleep(0.2)
            pyautogui.click(x,y)
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
                                                                                                      
    # Print the extracted text                                                                        
    print("Extracted Text:")                                                                
    print(f"~{extracted_text}~")                                                      
                                                                                                      
    # Debugging Image                                                                                                                                                     
    # preprocessed_image.show()                                                                       
                                                                                                      
    # Delete the Image
    os.remove(filepath)   

    return extracted_text
##################################################                                                                                                       
                                                                                                      
# Screen Settings 
# This is for 2560x1440                             
left = 1430  # X-coordinate of the top-left corner of the region                                     
top = 512   # Y-coordinate of the top-left corner of the region                                       
width = 250 # Width of the region        
height = 25 # Height of the region  

# This is for 1920x1080 
# left = 1116  # X-coordinate of the top-left corner of the region                                     
# top = 319   # Y-coordinate of the top-left corner of the region                                       
# width = 250 # Width of the region
# height = 29 # Height of the region                                      

#####################################################
# Key Hold Function
def hold_key_down(key, duration):
    
    #Vars
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)
#####################################################
# Main Loop 

#Settings
auto_heal = False
auto_move = True
avoid_elites = True
log = True
screenshot_folder = './TheScreenshots' 
 
running = True
def on_key_release(event):
    global running
    if event.name == 'q':
        running = False

# Set up a keyboard event listener
keyboard.on_release(on_key_release)

while running:
  if image_recognition('Images/FightButton.PNG', 'Button Visible!', region=(1088, 856, 250 ,90)) :

    # While Fighting
    pyautogui.moveTo(1100,500)

    #Take Screenshot and store pokemon namesw
    pokemon_name = take_screenshot(screenshot_folder, left, top, width, height) 
    is_elite="[E]" in pokemon_name or "[" in pokemon_name or "]" in pokemon_name
    avoidable_pokemon = {
                        }
    viable_pokemon = {"[S]",
                      "Zapdos",
                      "dos",
                      "d",
                     }
    #Log Pokemon
    if log:
      log_pokemon(pokemon_name)     
      
    if any(poke in pokemon_name for poke in viable_pokemon) or image_recognition('Images/SpecialEncounter.png', 'Special Encounter!'):
      #Stop
      running = False  
        
    elif (is_elite and avoid_elites) or any(poke in pokemon_name for poke in avoidable_pokemon):
      #Run
      hold_key_down('4',0)

    else:
      #Fight
      hold_key_down('1',0)
      choose_move()

  else:
    #Alert
    send_alert()
    
    #Heal
    heal()

    #Wander around
    random_float = uniform(0, 1)

    # print('Image not found on the screen')
    hold_key_down('a', random_float)    
    hold_key_down('d', random_float) 

print("Script stopped.")    

#####################################################