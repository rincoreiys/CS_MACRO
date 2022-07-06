from asyncio import futures
import asyncio
from dataclasses import dataclass
from select import select
import sys, os, win32gui
from time import sleep
from numpy import character, choose
sys.path.insert(0, os.getcwd())
from Instance.Manager import Instance
from Helper.Task import ObjectEvent
from Gameplay.operation import *
from Helper.Pool import Pool
from Helper.Exception import trycatch , detect
from Instance.Window import *


def imagePath(file):
    return os.path.join(os.getcwd(), "Assets/img", f"{file}.PNG")


class BaseDungeon(ObjectEvent): 
    character_movement_speed:int  = 13 # The slowst toon will walk to destination in 13 second
    killing_speed:int = 30 # the slowest toon
    current_run: int = 0
    require_DK: bool = True
    normal_run_done: bool = False
    dk_run_done: bool = True
    event_2xrun_done: bool = True
    is_2x_event: bool = True
    dificulty:str = "Nightmare"
  

    @property
    def is_done(self):
        return   (  
            (   self.normal_run_done ) and 
            (   self.require_DK == self.dk_run_done ) and 
            (   self.event_2xrun_done == self.is_2x_event ) 
        )

    def enter_dg(self):
        if not self.normal_run_done: 
            click()
        elif (  not self.event_2xrun_done and  self.is_2x_event ): 
            click()
        elif (  not self.dk_run_done and  self.require_DK ) : 
            click()

        if not self.is_done :
            match self.dificulty:
                case "Normal": pass
                case "Scary": pass
                case "Nightmare": pass

@dataclass
class Walk(ObjectEvent):
    character_movement_speed:int = 0 
    coordinate:list() = None
    next_task:object = None
    def run(self):
        focus(self.instance.hwnd)
        afk(False)
        if self.done_condition():
            self.trigger("done", self, self.next_task)
        else:
            time.sleep(0.5)
            walkToMapCoordinat(self.coordinate)
            self.trigger("retry", 5, self)

@dataclass
class Talk(ObjectEvent):
    character_movement_speed:int = 0 
    npc:object = None
    next_task:object = None
    def run(self):
        focus(self.hwnd)
        afk(False)
        if self.done_condition():
            
            self.trigger("done", self, self.next_task)
          
        else:
            time.sleep(0.5)
            print(*self.npc, self.npc)
            talkToNPCByMap(*self.npc)
            self.trigger("retry", 5, self)

@dataclass      
class Kill(ObjectEvent):
    next_task:object = None
    looting_time:int = 10
    def run(self):
        focus(self.hwnd)
        afk(True)
        time.sleep(2)
        if self.done_condition():
            time.sleep(self.looting_time)
            afk(False)
            self.trigger("done", self, self.next_task)
        else:
            self.trigger("retry", 5, self)

@dataclass      
class Login(ObjectEvent):
    next_task:object = None
    character:object = None
    loading_state = False
    def __post_init__(self):
        self.loading_state = False
        
    def run(self):
        try:
            character_name = self.character["character"]
            if self.loading_state is False:
                link = f'https://www.r2games.com/play/?game=10&server={self.character["server_id"]}&account={self.character["account"]}&password={self.character["password"]}'
                self.instance.go(link)    
                self.loading_state = True

            focus(self.instance.hwnd)
            detect()
            
            character_avatar = findImage(imagePath=asset_path(f'Environment/online_indicator.png'))
            
            if character_avatar is not None : # DONE CONDITION
              
                self.trigger("done", self, self.next_task)
                
            else:  #NOT DONE / RETYRING
                findName = findImage(imagePath=asset_path(f'Character/name/{character_name}.png'))
                if(findName is not None):
                   
                    x , y = findName
                    click(x, y, 2)
                    self.trigger("retry", 30, self)
                else:
                    if(self.retry_attempt > 2):
                        self.trigger("failed" ,self)
                    else:
                        self.retry_attempt += 1
                        self.trigger("retry", 30, self)
        except Exception as ex:
            pass
            # if(self.done_condition()){

            # }

      
        
@dataclass   
class DungeonEnter(ObjectEvent):
    character_movement_speed:int = 5
    dificulty:int = 3
    account:object = None
    npc:object = None
    npc_dialog:object = None
    enter_method:int = 1 #1 Normal #2 2x event #3 DK key
    dificulty:int = 3 #1 Normal #2 Hard #3 NM
    dungeon:BaseDungeon = None
    def choose_dificulty(self, current_task, next_task):
        match self.enter_method:
            case 1:
                click(545, 355)
            case 2: 
                click(545, 375)
            case 3: 
                if self.read_2x_event() : click(545, 395)  
                else:  click(545, 375)

        time.sleep(0.5)
        match self.dificulty:
            case 1:   click(545, 355)
            case 2:   click(545, 375)
            case 2:   click(545, 395)
    
        self.trigger("retry", 5, self)

        
    def read_2x_event(self): 
        return  isImageExist(imagePath=asset_path('img/Environment/2xdung.png'))
            
    def run(self):
        if self.done_condition():
            self.trigger("done", self, self.next_task)
            
        else:
            def talk_done_condition():
                return  isImageExist(*self.npc_dialog)
                # print(result)

            t = Talk(
                done_condition=talk_done_condition,
                npc=self.npc,
                hwnd=self.hwnd
            )
            
            t.on("done", self.choose_dificulty)
            self.pool.add(t)
            # self.trigger("retry",  self.character_movement_speed,  self)