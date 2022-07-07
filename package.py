import importlib.util
import subprocess, sys

dependecies = [
    { "package" : "asyncio", "alias" : "asyncio",  "module": "asyncio"},
    { "package" : "python-socketio[asyncio_client]", "alias":"python-socketio", "module" : "socketio" },
    { "package" : "pyautogui", "alias" : "pyautogui" ,"module" : "pyautogui"},
    { "package" : "opencv-python-headless" , "alias": "opencv-python", "module" : "cv2"},
    { "package" : "aiohttp",  "alias": "aiohttp", "module" : "aiohttp"},
    { "package" : "selenium",  "alias": "selenium", "module" : "selenium"},
    { "package" : "pymongo",  "alias": "pymongo", "module" : "pymongo"},
    { "package" : "dnspython",  "alias": "dnspython", "module" : "dns"},
    { "package" : "pywin32",   "alias" : "pywin32", "module" : "win32gui"},
    { "package" : "pillow",  "alias" : "pillow", "module" : "PIL"},
    { "package" : "keyboard",  "alias" : "keyboard", "module" : "keyboard"},
    { "package" : "argparse",   "alias" : "argparse", "module" : "argparse"},
]

def install_package(name:str, silent:bool):
    try: 
       
        subprocess.check_call([sys.executable, "-m", "pip", "install", name])
    except Exception as ex:
        print("Fail: ", ex)
        

def checking_package(silent:bool = False):
    subprocess.check_call([sys.executable, "-m", "pip", "install","--upgrade", "pip"])
    for item in dependecies:
        package, alias , module = item.values()
        if importlib.util.find_spec(module, alias): 
            if not silent : print(f'Package {module} found')
        else:  
            if not silent : print("Package ", alias, "isnt found, Installing..")
            install_package(package, silent)
    
    print("Installation Done")


checking_package()
