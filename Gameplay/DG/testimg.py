import sys, os
from threading import Thread
from xmlrpc.client import Boolean
sys.path.insert(0, os.getcwd())
from Gameplay.operation import *
def imagePath(file):  return os.path.join(os.getcwd(), "Assets/img/Dungeon/175", f"{file}.PNG")
HWND = 131844
# print(isInMap(imagePath=imagePath("outer")))
def fight_mob(): return isImageExist(imagePath=asset_path("Dungeon/Corruption/corr_mob"), region=(624, 74, 134, 39 ))
print(isImageExist(imagePath=asset_path("Exception/disconnected_2")))
