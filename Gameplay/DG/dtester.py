
import sys, os, time


sys.path.insert(0, os.getcwd())
import keyboard
from threading import Thread
from Helper.Exception import LoginStuckException
from Gameplay.DG.dungeon import *
from Gameplay.DG.corruption import Corruption
from Instance.Window import focus
# from Gameplay.operation import *
HWND = 395664

focus(HWND)
d175_loot = {
    "equip" : True,
}

def run_routine():
   
    try:
        print("aa")
        time.sleep(1)
    except LoginStuckException as lse:
        print("stuck")

    # prev:object
    # import importlib
    # module = importlib.import_module("Gameplay.DG.dungeon")
    # class_ = getattr(module, "D175")
    # instance = class_(require_dk=True, loot_config=d175_loot, loot_time=14)
    # instance.bag_already_empty_before = False
    # instance.init()
    

    # g = getattr() D175(require_dk=True, loot_config=d175_loot, loot_time=14)
    # g.bag_already_empty_before = False
    # g.init()

    # e = D165(loot_config=d175_loot, loot_time=4)
    # e.init()
    
    # a = D30(require_dk=False, loot_config=d175_loot, loot_time=3, difficulty=3)
    # prev = a
    # a.init()

    # #WORK WELL
    # b = D55(loot_config=d175_loot, loot_time=3)
    # prev = b
    # b.init()

    # #WORK WELL
    # d = D85(loot_config=d175_loot, loot_time=4)
    # d.init()
    
    # #WORK WELL
    # c = D75(loot_config=d175_loot, loot_time=4, init_pixie=False, require_dk=True)

    # c.init()
    
    # #WORK WELL
  
    #WORK WELL 
    # c = Corruption(floor_limit=21)
   
    # c.init()
   
def activate_listener():
    while True:
        if(keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl")):
            print("EXIT")
            raise KeyboardInterrupt
        time.sleep(0.05)



focus(HWND)   
t = Thread(target=run_routine, daemon=True)
t.start()
e = Thread(target=detect_error, daemon=True, kwargs={'thread': t}).start()
l = Thread(target=activate_listener).start()
