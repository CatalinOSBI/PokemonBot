import os
import json


def create_log():
    if not os.path.exists("log.txt"):
        with open("log.txt", "w", encoding="utf-8") as file:
            file.write("")


def create_config():
    if not os.path.exists("config.json"):
        default = {
            "settings": {
                "auto_heal": False,
                "auto_move": False,
                "avoid_elites": False,
                "log": False,
                "screenshot_folder": "./TheScreenshots",
                "mode": "left_right"
            },
            "pixels": {
                "heal": {
                    "x": None,
                    "y": None,
                    "R": None,
                    "G": None,
                    "B": None
                },
                "synch(not used yet)": {
                    "x": None,
                    "y": None,
                    "R": None,
                    "G": None,
                    "B": None
                },
                "caught(not used yet)": {
                    "x": None,
                    "y": None,
                    "R": None,
                    "G": None,
                    "B": None
                }
            },
            "images": {
                "poke_name": {
                    "x": None,
                    "y": None,
                    "width": 250,
                    "height": 27
                },
                "confirm": {
                    "x": None,
                    "y": None,
                    "width": None,
                    "height": None
                },
                "fight": {
                    "x": None,
                    "y": None,
                    "width": None,
                    "height": None
                },
                "turn": {
                    "x": None,
                    "y": None,
                    "width": None,
                    "height": None
                },
                "special(not used yet)": {
                    "x": None,
                    "y": None,
                    "width": None,
                    "height": None
                }
            }
        }

        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(default, file, indent=4)

def initial_setup():
  """Creates log and config files"""
  create_log()
  create_config()

# Leave this here for testing
if __name__ == "__main__":
  initial_setup()  