# from Helper.Task import ObjectEvent
from threading import Thread
import asyncio
import socketio
import time
import socketio , importlib
from  Helper.Task import ObjectEvent
from Helper.Exception import  trycatch
class Pool():
    task:dict = {}
    failed_task = {}
    finised_task = {}
    sio:socketio.AsyncClient = None
    pid = 1
    def serialize_task(self):
        def format(value):
            task:ObjectEvent = value[1]
            ret = {
                "pid" : task.id,
                "profile_number": task.instance.profile_number,
                "class" : task.__class__.__name__,
            }
            return (value[0], ret)

        return dict(map(lambda v : format(v), list(self.task.items() )))

        
    async def add(self, *task):
        for t in task:
            if t is not None:
                t.id = self.pid
                # print(t.id)

                #set default event
                if "done" not in t.callback : t.on("done", self.done )
                if "future" not in t.callback : t.on("future", self.future)
                if "failed" not in t.callback :t.on("failed", self.failed)
                if "retry" not in t.callback :t.on("retry", self.retry)

                self.task[self.pid]  = t
                self.pid += 1
        await self.sio.emit("forward", data=("web:sync_job", self.serialize_task()), namespace='/browser')

    def remove(self, pid):
        try:
            self.task.pop(pid)
        except KeyError as ke:
            print(ke)

    def done(self, current_task, next_task=None):
        # print("left" , self.task)
        # print(current_task, "done")
        print(current_task, "done generic")

        self.remove(current_task.id)
        if next_task is not None:  self.add(next_task)
        # await sio.emit("forward", ("web:sync_task", self.task), namespace="/pool")
        # print(pid, next_task)

    def retry(self, trigger_in:int, task):
        time.sleep(trigger_in)
        task.in_execution = False

        
        # task.run()

    def future(self, trigger_in:int,  task=None):
        # def background_task():
        time.sleep(trigger_in)
         #PULL TRUE CONDITION TO BE ABLE EXECUTED
        self.add(task)

    def failed(self, task):
        # list(self.task).pop(task.id)
        print(task, "failed")
        self.remove(task.id)


    def execute(self):
        while True:
            # print(self.task)
            for index, task in list(self.task.items()):
                if task is not None:
                    if not task.in_execution :
                        task.in_execution = True
                        trycatch(task.run)
                        # time.sleep(10)
                        # task.in_execution - True
            time.sleep(1)
