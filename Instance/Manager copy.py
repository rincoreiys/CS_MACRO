
from threading import Thread
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from  Helper.Connection import db
import os, json, time
import win32gui,  win32con
from selenium.common.exceptions import WebDriverException
window_find_result = None
window_name_search = ""
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
options = Options()
options.add_argument("disable-features=NetworkService")
options.add_argument("disable-infobars")
options.add_argument("mute-audio")
options.add_argument("disable-web-security")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_experimental_option("detach", True)

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
        # print (hex_addr, window_text)
        if window_text  == window_name_search and window_find_result is None :
            window_find_result  = hwnd

class Instance:    
    driver : webdriver.Chrome
    profile_number: int
    account_binding: object
    hwnd: int
    def __init__(self, profile_number: int = 1, session_id = None, command_executor=None, hwnd = None):
        self.profile_number = profile_number
        if session_id is  not None and command_executor is not None: 
          
            self.hwnd = hwnd
            self.attach_to_session(command_executor, session_id)
        else:
            self.load_browser()

    def go(self, url: str = ""):
        (Thread(target=self.driver.get, daemon=True, args=[url])).start()

    def focus(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetWindowPos(self.hwnd,win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
        win32gui.SetWindowPos(self.hwnd,win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
        win32gui.SetWindowPos(self.hwnd,win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        # win32gui.SetForegroundWindow(self.hwnd)
        
             
    def load_browser(self):
            #THIS WILL EXECUTED IF RETURN EKYWORD REMOVED   =
            options.add_argument(f"user-data-dir={os.getcwd()}\Profile\profile-{self.profile_number}")
            options.add_argument(f'load-extension={os.getcwd()}\Instance\Extension\CS')
            # options.add_argument(f'remote-debugging-port=700{self.profile_number}')
            driver = webdriver.Chrome( "chromedriver.exe", options=options)  
            self.driver = driver
            # print(f"Profile {self.profile_number}")
            self.driver.execute_script(f"document.title = 'Profile {self.profile_number}'")
            time.sleep(0.2)
            self.hwnd =  findWindowByName(f"Profile {self.profile_number} - Google Chrome")
            self.account_binding = {}
            
     
    def attach_to_session(self, command_executor, session_id)  :
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
        options.add_argument(f"user-data-dir={os.getcwd()}\Profile\profile-{self.profile_number}")
        options.add_argument(f'load-extension={os.getcwd()}\Instance\Extension\CS')

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute
        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(command_executor=command_executor, desired_capabilities=options.to_capabilities())
        new_driver.session_id = session_id
        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute
        self.driver = new_driver
        return new_driver
        
    def new_tab(self):
        self.driver.execute_script("window.open('')")

    def is_closed(self, callback):
        while True:
            try:
                self.driver.current_url
            except WebDriverException as driver_exception:
                print("driver error", driver_exception)
               
                callback("closed by user")
                break
            time.sleep(1)
    
    
            
class InstanceManager:

    def init_instance(self, profile_number:int) -> Instance :  
        if self.busy_state[profile_number] is not True: #prevent unpatient behaviour when open browser
            self.busy_state[profile_number] = True
            instance :Instance = self.instance_collection[profile_number] or Instance(profile_number)
            self.instance_collection[profile_number] = instance
            
        elif self.instance_collection[profile_number] is not None : 
            print("Please wait until process done")
            instance :Instance = self.instance_collection[profile_number]
        return instance

    def serialize(self) -> dict:
        def format_item(val):
            v:Instance = val[1]
            res = {
                'command_executor' : v.driver.command_executor._url if v is not None else None,
                'hwnd' : v.hwnd if v is not None else None,
                'profile_number' : val[0],
                'account_binding': v.account_binding if v is not None else None, 
                'handles': v.driver.window_handles if v is not None else None,
                'session_id': v.driver.session_id if v is not None else None,  
            } 
            return (val[0], res)
        
        
        # FILTER NONE DICTIONARY
        return dict(map(lambda v : format_item(v),self.instance_collection.items()))
        #return  dict(filter(lambda item: item[1] is not None, map(lambda v : format_item(v),self.instance_collection.items())))

    def restore(self):
        instance_request = requests.get('http://127.0.0.1:3000/instance')
        for instance in instance_request.json():
            if instance['session_id'] is  not None and instance['command_executor'] is not None: 
                self.instance_collection[instance['profile_number']] = Instance(
                    instance['profile_number'], 
                    instance["session_id"] , 
                    instance['command_executor'], 
                    instance['hwnd']
                )

    def save_state(self):
        json_form = json.dumps(list(self.serialize().values()))
        print(json_form)
        requests.post('http://127.0.0.1:3000/instance' ,  data=json_form, headers=headers)

            
                
            

