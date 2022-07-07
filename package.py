import importlib.util
from threading import Thread
import subprocess, sys

dependecies = [
    { "package" : "asyncio", "module": "asyncio"},
    { "package" : "python-socketio[asyncio_client]", "module" : "socketio" },
    { "package" : "pyautogui", "module" : "pyautogui"},
    { "package" : "opencv-python-headless" , "module" : "cv2"},
    { "package" : "aiohttp", "module" : "aiohttp"},
    { "package" : "selenium", "module" : "selenium"},
    { "package" : "pymongo", "module" : "pymongo"},
    { "package" : "dnspython", "module" : "dnspython"},
    { "package" : "pywin32", "module" : "win32gui"},
    { "package" : "pillow", "module" : "pillow"},
    { "package" : "keyboard", "module" : "keyboard"},
    { "package" : "argparse", "module" : "argparse"},
]

def install_package(name:str, silent:bool):
    try: 
        if not silent : print("Package ", name, "isnt found, Installing..")
        subprocess.check_call([sys.executable, "-m", "pip", "install", name])
    except Exception as ex:
        print("Fail: ", ex)
        

def checking_package(silent:bool = False):
    for item in dependecies:
        package, module = item.values()
        if importlib.util.find_spec(module, package): 
            if not silent : print(f'Package {module} found')
        else:  
            install_package(package,silent)
    
checking_package()