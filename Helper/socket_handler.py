#BETA 1
import argparse, socketio, json
from cgitb import handler
from threading import Thread
from Helper.Exception import LoginException, LoginStuckException, DisconnectException
from Instance.Manager import Instance
from selenium.common.exceptions import WebDriverException, TimeoutException
from Gameplay.operation import detect_error, login

  
# Opening JSON CONFIG  file
f = open('config.json')
config = json.load(f)

sio = socketio.AsyncClient(reconnection_attempts=10)

def only(obj:object, keys = [] ):
    obj = obj.__dict__ #FOR CLASS COMPATIBILITY
    print("obj", obj)
    ret = { k: v for k, v in  obj.items()  if k in keys } 
    print("ret", ret)
    return  ret

class Handler(socketio.AsyncClientNamespace):
    node_number:int = 0
    def __init__(self, namespace=None, node_number=0):
        super().__init__(namespace)
        try:
            self.node_number = node_number
            self.instance:Instance = Instance(node_number=node_number, sio=sio)    
        except WebDriverException as ex:
            print("Browser exception : ", ex)
             
    async def on_connect(self):
        self.instance.setHwnd()
        await sio.emit("sync", data=only(self.instance, ["hwnd", "character"]) , namespace="/node" )

    async def on_handle_character(self, character):
        # print(character)
        try:
            if login(instance=self.instance, character=character):
                self.instance.character = character
                await sio.emit('on_logged_in', data={"response" : f"Character ${character['character']} is online", "character": character},  namespace="/node" )
                await self.instance.run(character["routines"])
                Thread(target=detect_error, daemon=True).start()

        except TimeoutException as te:
            await sio.emit('on_load_failed', data={"response" : f"Character ${character['character']} failed to loaded, posibility your internet too slow"},  namespace="/node" )

        except LoginStuckException as le: 
            await sio.emit('on_character_stuck', data={"response" : f"Character ${character['character']} stuck online, wait for 15 min or so"},  namespace="/node" )

        except DisconnectException as de:
            await sio.emit('on_character_disconnected', data={"response" : f"Character ${character['character']} disconnected, retrying login"},  namespace="/node" )

        finally: 
            # WILL RUN IF TRY / EXCEPT DONE
            self.instance.character = None
            await sio.emit('on_character_done', data={"response" : f"Character ${character['character']} done all routine for today"},  namespace="/node" )
            
    # async def on_off_character(self):
    #     self.instance.character = None
    #     await sio.emit("sync", data=only(self.instance, ["hwnd", "character"]) , namespace="/node" )
handler = Handler('/node', node_number=config["NODE_NUMBER"])
sio.register_namespace(handler)

async def listen():
    await sio.connect(f"{config['SERVER']}/node?number={config['NODE_NUMBER']}" )
    await sio.wait()