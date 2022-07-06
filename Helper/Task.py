from dataclasses import dataclass
import sys, os, win32gui
sys.path.insert(0, os.getcwd())
from Instance.Manager import Instance

@dataclass
class ObjectEvent(object):
    id:int = 1
    pool  = None
    in_execution: bool = False
    callback:dict = None
    instance:Instance  = None
    retry_attempt = 0
    done_condition:object  = None
    next_task:object = None

    def __post_init__(self):
        self.callback = {}
        self.in_execution = False
        self.retry_attempt = 0

    def on(self, event_name, callback):
        if self.callback is None : self.callback = {}
        if event_name not in self.callback:
            self.callback[event_name] = callback
            print(self.callback)
    
    
    def trigger(self, event_name, *arg):
        
        # print(arg)
        if  event_name in self.callback:
            # for callback in self.callbacks[event_name]:
            self.callback[event_name](*arg)

    def run(self):
        pass

    
    def retry(self):
        if self.retry_attempt < 3:
            self.retry_attempt += 1
            self.trigger("retry", 5, self)
           

        if self.retry_attempt == 3 :
            self.retry_attempt += 1
            self.trigger("failed", self)
    