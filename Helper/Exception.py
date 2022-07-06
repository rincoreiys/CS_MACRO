
import os, sys
sys.path.insert(0, os.getcwd())
# from  Gameplay.operation  import *
HWND = 395664
# def handle_require_party( pool, instance):
#     click(685,405)
#     party(True)

# def handle_relogin(account, pool:Pool, instance:Instance):
#     pool.add(Login(character_name=))

class DisconnectException(Exception): pass
class LoginStuckException(Exception): pass
class BrowserUpdateException(Exception):pass
class DieException(Exception): pass
class LoginException(Exception): pass
      
EXCEPTIONS_DIR_PATH = "Assets/img/Exception"
EXCEPTIONS = [
    {
        "type" : "DICONNECTED_1",
        "recognition" : "disconnected_1",
        "termination":  DisconnectException
    },
    {
        "type" : "CHARACTER LOGIN STUCK",
        "recognition" : "character_login_stuck",
        "termination":  LoginStuckException
    },
    {
        "type" : "DICONNECTED_2",
        "recognition" : "disconnected_2",
         "termination":  DisconnectException
    },
    {
        "type" : "DICONNECTED_3",
        "recognition" : "disconnected_3",
        "termination":  DisconnectException
    },
    {
        "type": "REQUIRE_PARTY",
        "recognition" : "require_party",
        "termination" : None
    }
]


# class MacroException(Exception):
#    pass 
 
# def asset_path(path):
#     return os.path.join(os.getcwd(), EXCEPTIONS_DIR_PATH, path)



# def trycatch(proc, pool = None, instance = None, custom_handling=None):
#     try:
#         detect()
        
#     except Exception as me:
#         for arg in me.args:
#             if arg["handling"] is not None : arg["handling"]( pool, instance)
#     finally:
#         proc() 
     


# focus(HWND)
# print(isImageExist(asset_path(EXCEPTIONS[3]['recognition'])))
