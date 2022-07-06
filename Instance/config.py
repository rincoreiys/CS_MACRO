from selenium.webdriver.chrome.options import Options
import os
def getConfig(node_number) -> Options:
    
    options = Options()

    options.add_argument("disable-features=NetworkService")
    options.add_argument("disable-infobars")
    options.add_argument("mute-audio")
    options.add_argument("disable-web-security")
    options.add_argument("start-maximized")
    options.add_argument("mute-audio")
    options.add_argument(f'load-extension={os.getcwd()}\Instance\Extension\CS')
    # options.add_argument("force-device-scale-factor=0.8")
    
    options.add_argument(f"user-data-dir=C:\Program Files (x86)\Google\Chrome\Application\Profile\{node_number}")
    options.add_argument("disable-session-crashed-bubble")
    
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    return options
  
    
   
 
    
