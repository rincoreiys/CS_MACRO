from Helper.Pool import Pool
from threading import Thread
import socketio
from Instance.Manager import Instance, InstanceManager
import asyncio
from selenium.common.exceptions import WebDriverException
from Helper.DataClass import Login
sio = socketio.AsyncClient()
im = InstanceManager()
p = Pool()

class BrowserNamespace(socketio.AsyncClientNamespace):
    async def on_get_session(self):
        sid = self.client.__dict__['namespaces'][self.namespace]
        await sio.emit('forward', data=('web:sync_browser_session', sid), namespace="/browser")
        return sid

    async def on_connect(self): 
        
        await sio.emit('forward' ,  data=("web:sync_status", { "state" : True, "instances": im.serialize()}) , namespace="/browser") 



    async def on_open(self, data):
        print(data)
        try:
            profile_number = data['profile_number']
            instance = im.init_instance(profile_number)
            
            def on_closed(arg):
                # print(arg)
                im.instance_collection[profile_number] = None
                im.busy_state[profile_number] = False
                # ra    ise Exception("closed")
                asyncio.new_event_loop().run_until_complete(sio.emit("off", instance.profile_number, namespace="/browser"))
                asyncio.new_event_loop().run_until_complete(sio.emit("forward", data=( "web:sync_instances", im.busy_state), namespace="/browser"))
               
            # asyncio.new_event_loop().run_until_complete(sio.emit("forward", data=( "pool:get_job", im.busy_state), namespace="/browser"))
            def job_received(arg):
                print(arg, "form ehe")
            # await sio.emit("request_job", namespace="/pool", callback=job_received)
            (Thread(target=instance.is_closed, args=[on_closed], daemon=True)).start()
          
        except Exception as ex:
            print("get wrror here", ex)
            im.busy_state[profile_number] = False 
        finally:
            await self.on_get_instances()
            print("check", im.instance_collection)
            im.save_state()
            return True

    async def on_load_character(self, data=None):
        global p
        if im.instance_collection[data['profile_number']] is not None:
            print(data)
            character = data['character']
            instance:Instance= im.instance_collection[data['profile_number']]
            # print(character)
           
            def sync_status(current_task):
                instance.account_binding = character
                print(instance)
                p.done(current_task)
            login_task= Login(instance=instance, character=character)
            login_task.on("done", sync_status) 
            await p.add(login_task)
        
    async def on_get_instances(self):
        await sio.emit('forward' ,  data=("web:sync_instances", im.serialize()) , namespace="/browser") 
        
    def on_new_tab(self,data):
        instance:Instance = im.instance_collection[data['profile_number']]
        if instance is not None:
            instance.new_tab()
            print("Succesfully open new tab")

    def on_get_tabs(self, data):
        instance:Instance = im.instance_collection[data['profile_number']]
        if instance is not None:
            print(instance.driver.window_handles, len(instance.driver.window_handles))

    def on_focus(self, data):
        # print(data)
        instance:Instance = im.instance_collection[data['profile_number']]
        if instance is not None: instance.focus()

    def on_go(self,data):
        instance:Instance = im.instance_collection[data['profile_number']]
        print("open_url", instance)
        if instance is not None:
            instance.go(data['url'])
            
sio.register_namespace(BrowserNamespace('/browser'))
async def listen():
    await sio.connect("http://localhost:3000/browser")
    p.sio = sio
    await sio.wait()

Thread(target=p.execute, daemon=True).start()