# xtcards
An AI integrated poker capstone project written with Python, using [pygame](https://www.pygame.org/) and [pygame_gui](https://github.com/MyreMylar/pygame_gui)

Created by Jacob Penman, Jonah Brawley, Dylan Lau, and Jeremiah Oh
for CSC412 at California Baptist University

# Overview
xtcards (aka Kingdom Cards) is a digital Texas Hold 'Em style poker game that integrates 
a custom trained poker AI as well as image recognition in order to demonstrate the capabilities and viability
of a digital poker game that is playable with real cards

The goal of the Christian integration is to provide a more positive impact and have healthier implications
than traditional poker. Additionally, **in order to play the game you must use a deck of standard Bicycle playing cards**,
as this is what our image recognition model was trained off of in order to achieve a high 99.9% accuracy.

## Setup instructions
1. Clone project
2. Run `pip install -r requirements.txt` to install dependencies needed
3. Play by running `main.py`

## Debug options
Disable image detection by running `python main.py --debug-tf=true`. This is only useful if you are making modifications
to the game and would like faster loading times.  

## Updating requirements
1. If new dependencies are added or removed, use `pipreqs --force [PATH TO XTCARDS HERE]` to automatically update `requirements.txt`
2. Tip: if you are located inside your xtcards folder, use `pipreqs --force .` (period means current directory)
