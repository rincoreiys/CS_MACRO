import queue
from threading import Thread
import asyncio
import sys, os
import time
import socketio
from Instance.Manager import Instance, InstanceManager
from Helper.Connection import db
import importlib
from Helper.Bucket import Bucket
from Helper.Pool import Pool

im:InstanceManager =  InstanceManager()
sio = socketio.AsyncClient()
im.restore()
pool = Pool()

class MacroNamespace(socketio.AsyncClientNamespace):
    def on_receive_task(self, data):
        try:
            print(data)
            module_name = f"Gameplay.{data['module']}"
            module = importlib.import_module(module_name)
            func = getattr(module, 'run')
            func(im.instance_collection[data['profile_number']])
            
        except Exception as ex:
            print(ex)


sio.register_namespace(MacroNamespace('/macro'))
async def listen():
    await sio.connect("http://localhost:3000/macro")
    await sio.wait()

