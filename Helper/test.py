import os
from threading import Thread
from selenium import webdriver
command_executor='http://localhost:4444'
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_experimental_option("detach", True)

def create_driver_session(executor_url, session_id):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    execute_temp =  RemoteWebDriver.execute
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    try:
        new_driver.get("http://google.com")
    except Exception as e:
        
        # print(e)
        # RemoteWebDriver.execute = execute_temp
        

        new_driver.get("http://google.com")
        
    return new_driver

#driver_chrome_reuse = create_driver_session("81846d19788eee49e80981ac97dfec8a")
try:
    driver = webdriver.Chrome(options=options)
   
    driver.get("http://google.com")
    with open("selenium_session.txt", "w") as f:
        f.write(driver.session_id+"#"+driver.command_executor._url)
        f.close()
except KeyboardInterrupt:
    pass

# second_driver =  create_driver_session(driver.command_executor._url, driver.session_id)
# def run_driver():
#     second_driver =  create_driver_session("http://localhost:50860", "223a9455c9eb8deafc57802af3542243")
#     second_driver.get("http://animesave.com")


# Thread(target=run_driver).run()


# try:
#     driver = webdriver.Remote(command_executor=command_executor, options=options )
# #     # prevent annoying empty chrome windows
# #     print(driver)

# #     existing_session_id = open("selenium_session.txt").read()
# #     if(existing_session_id != ""):
# #         driver.session_id = existing_session_id
# #         driver.close()
# #         driver.quit() 

    
#     with open("selenium_session.txt", "w") as f:
#         f.write(driver.session_id)
#         f.close()
    
    
# #     # attach to existing session
   
   
# #     # self.browser_listener = Thread(target=self.browser_existances_listener)
# #     # self.browser_listener.run()
# except:
#     pass
# #     driver = webdriver.Remote(command_executor=command_executor, options=options )
# #     with open("selenium_session.txt", "w") as f:
# #         f.write(driver.session_id)
# #         f.close()
        
# #     #print(f"Error on browser call {self.instance_number} Initialization, posibility: browser has been closed") 

# # # driver = webdriver.Remote(
# # #     command_executor='http://localhost:4444',
# # #     options=chrome_options
# # # )
# # driver.get("http://www.google.com")