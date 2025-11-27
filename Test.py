import pyautogui
import pytesseract
from datetime import datetime
import os
from PIL import Image
import time
import keyboard
from random import uniform
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

##################################################
# Log Pokemon
def log_pokemon(pokemon_name, log_file='log.txt'):
  timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
  log_entry = f"~{pokemon_name}~ - {timestamp}\n"
    
  with open(log_file, 'a', encoding='utf-8') as file:
    file.write(log_entry)

##################################################
# Special encounter logic
def special_encounter():
    try:
        if pyautogui.locateOnScreen('SpecialEncounter.PNG', confidence=0.7):
            print('Special Encounter!')
            return True
    except:
        pass
    return False
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
    # preprocessed_image = Image.open(filepath).convert('L')  # Convert to grayscale                    
    preprocessed_image = Image.open(filepath).point(lambda x: 0 if x < 128 else 255)                    
                                                                                                      
    # Use pytesseract to perform OCR and extract text                                                 
    extracted_text = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 7')
                                                                                                      
    # Print the extracted text                                                                        
    print("Extracted Text:")                                                                          
    print(extracted_text)                                                      
                                                                                                      
    # Debugging Image                                                                                   
    # print("Image Size:", preprocessed_image.size)                                                   
    # print("Thresholded Image:")                                                                     
    # preprocessed_image.show()                                                                       
                                                                                                      
    # Delete the Image
    os.remove(filepath)   

    return extracted_text                                                                                                     
                                                                                                      
# Screen Settings 
# This is for 2560x1440                             
left = 1430  # X-coordinate of the top-left corner of the region                                     
top = 512   # Y-coordinate of the top-left corner of the region                                       
width = 250 # Width of the region        
height = 25 # Height of the region  

# This is for 1920x1080 
# left = 1123  # X-coordinate of the top-left corner of the region                                     
# top = 358   # Y-coordinate of the top-left corner of the region                                       
# width = 250 # Width of the region
# height = 29 # Height of the region                                      

#####################################################

#####################################################
# Key Hold Function

def hold_key_down(key, duration):
    
    #Vars
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

#####################################################

#####################################################
# Main Loop 

#Settings
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
  try:
    if pyautogui.locateOnScreen('FightButton.PNG', confidence=0.7) :

      # While Fighting

      print('Button Visible!')

      #Take Screenshot and store pokemon name
      pokemon_name = take_screenshot(screenshot_folder, left, top, width, height) 
      is_elite="[E]" in pokemon_name  
      viable_pokemon = {"[S]",
                        "Rhyhorn",
                        "horn",
                        "yho",
                       }
      #Log Pokemon
      if log:
        log_pokemon(pokemon_name)     
      
      if any(poke in pokemon_name for poke in viable_pokemon) or special_encounter():
        #Stop
        running = False  
        
      elif is_elite and avoid_elites:
        #Run
        hold_key_down('4',0)  

      else:
        #Fight
        hold_key_down('1',0) 
        time.sleep(0.5)
        hold_key_down('1',0)

  except pyautogui.ImageNotFoundException:

    # While Not Fighting
    random_float = uniform(0, 1)

    print('Image not found on the screen')
    hold_key_down('a', random_float)    
    hold_key_down('d', random_float) 

print("Script stopped.")    

#####################################################