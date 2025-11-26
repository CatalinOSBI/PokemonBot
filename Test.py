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
    preprocessed_image = preprocessed_image.point(lambda x: 0 if x < 128 else 255)                    
                                                                                                      
    # Use pytesseract to perform OCR and extract text                                                 
    extracted_text = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 6')
                                                                                                      
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
                                                                           
screenshot_folder = r'D:\Visual Studio Code\Projects\Pokemon\TheScreenshots'                          
                                                                                                      
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
    
    # Vars
    
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

#####################################################

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
  try:
    if pyautogui.locateOnScreen('FightButton.PNG') :

      # While Fighting

      print('Button Visible!')
      buttonPosition = pyautogui.locateCenterOnScreen('FightButton.PNG')

      #Take Screenshot and store pokemon name
      pokemon_name = take_screenshot(screenshot_folder, left, top, width, height)  
      viable_pokemon = {"Snorlax",
                        "Rotom",
                        "Noibat",
                        "Spiritomb",
                        "Yveltal",
                       }
      
      if any(poke in pokemon_name for poke in viable_pokemon):
        #Stop
        running = False 
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