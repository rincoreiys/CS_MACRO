from dataclasses import dataclass
from selenium import webdriver

import os, time
import socketio
import win32gui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Instance.config import getConfig
from Instance.Window import focus
import importlib
window_find_result = None
window_name_search = ""


def findWindowByName(window_name):
    global window_name_search 
    global window_find_result
    window_find_result = None
    window_name_search = window_name
    win32gui.EnumWindows( winEnumHandler, None )
    return window_find_result

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        global window_name_search
        global window_find_result
        window_text =  win32gui.GetWindowText( hwnd )
        hex_addr = hex(hwnd)
        print (hex_addr, window_text)
        if window_text  == window_name_search and window_find_result is None :
            window_find_result  = hwnd

@dataclass
class Instance:    
    node_number: int = 0
    driver =  webdriver.Chrome("chromedriver.exe", options=getConfig(node_number))  
    hwnd: int = 0
    character: dict = None
    routines: list = None
    sio: socketio.AsyncClient = None

    def __post_init__(self): self.setHwnd()

    def go(self, url):
        self.driver.get(url)
        
        return True

    def setHwnd(self):
        self.driver.execute_script(f"document.title = 'Profile {self.node_number}'")
        time.sleep(0.1)
        self.hwnd =  findWindowByName(f"Profile {self.node_number} - Google Chrome")
        return self.hwnd

    def focus(self):
        self.setHwnd()
        focus(self.hwnd)
        
    async def run(self, routines):
        self.routines = routines
       
        module = importlib.import_module("Gameplay.DG.dungeon")
        async def on_routine_done(): pass
           
        for index, routine in  enumerate(routines, start=1):
            class_ = getattr(module, routine['name'])
            instance = class_(require_dk=routine['require_dk'], loot_config=routine['loot_config'])
            if index == 1 : instance.bag_already_empty_before = False
            instance.init()

    
                
            

