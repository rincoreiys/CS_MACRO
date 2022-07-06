# BETA 2

from dataclasses import dataclass
import sys, os
sys.path.insert(0, os.getcwd())
from Gameplay.operation import *
from Helper.Exception import  DieException

def imagePath(file):  return os.path.join(os.getcwd(), "Assets/img/Dungeon/Corruption", f"{file}.PNG")

@dataclass
class Corruption:
    routine_position:int = 0
    current_run:int = 0
    is_prepared:bool = False
    idle_clearing_crypt:bool = False
    floor_limit:int = 0
    max_floor:int = 21
    current_floor:int = 0
    first_time_claim:bool = True
    done:bool = False
    in_afk:bool = False
    routine_list =  [
        {"routine" :  "Talk To SG Battlemaster"},
        {"routine" :  "Talk To Corruption Master"},
        {"routine" :  "Enter Gate"},
        {"routine" :  "Killing Mob"},
        {"routine" :  "Claim Reward"},
        {"routine" :  "Upstair"},
        {"routine" :  "Exit"},
    ]


    def detect_location(self):
        get_rid_annoying_error()
        if isInMap(imagePath=imagePath('city')):    self.talk_to_sg_battlemaster()
        elif isInMap(imagePath=imagePath('hall')):   self.talk_to_corruption_npc()
        else:
          
            if is_in_end():
                self.killing_mob() 
                self.claim()
            elif is_in_middle(): 
                self.killing_mob() 
            else : self.enter_gate()

    def talk_to_sg_battlemaster(self):
        party(False)
        if(isImageExist(imagePath=imagePath("sg_battlemaster"))): 
            clickOnImage(imagePath=imagePath("sg_battlemaster"))
            time.sleep(0.1)
            click(550, 353)
            waitForImage(imagePath=imagePath('hall'))
        else:
            talkToNPCByMap(imagePath=imagePath("sg_battlemaster_link"), confidence=0.95, scroll_position=0)
    
    def talk_to_corruption_npc(self):
        if isImageExist(imagePath=imagePath("corrupted_guard_dialog")):
            is_free_entry_done = isImageExist(imagePath=imagePath("free_entry_done"), region=(517,339,342,32))
            is_mob_entry_done = isImageExist(imagePath=imagePath("mob_entry_done"), region=(517,364,342,32))
            # print(is_free_entry_done, is_mob_entry_done )
            
            if not is_free_entry_done: #FREE ENTRY NOT DONE  
                click(620 , 350) 
                self.current_floor = 1
                #RELEASE ATTACKED STATE
                return 
            elif not is_mob_entry_done: #MOB ENTRY NOT DONE
                click(620 , 370) 
                time.sleep(0.5)
                if  isImageExist(imagePath=imagePath("require_defeat"), region=(532,334,115,71)):
                    click(684, 409)
                    time.sleep(0.5)
                    click(846,265 ) #CLOSE CORRUPTION NPC DIALOG
                    walkToMapCoordinat(679, 444, acknowledge=True) 
                    afk(True)
                    time.sleep(180)
                    afk(False)
                else: self.current_floor = 1

            if is_free_entry_done and is_mob_entry_done: #CORRUPTION DONE
                self.done = True
                click(620 , 410) 
                
            return
        else:
            talkToNPCByMap(imagePath=imagePath("corrupted_guard_link"))

    def enter_gate(self):
       
        if isImageExist(imagePath=imagePath("rock_guard_dialog")):
            click(588,355)
            time.sleep(0.5)
            click(1317, 182, 4)
        else:
            talkToNPCByMap(imagePath=imagePath("rock_guard_link"))
            time.sleep(1.5)

    def killing_mob(self):
        
        if self.first_time_claim :      self.read_floor()
        if not self.in_afk : self.in_afk =  afk(True)
        afkIfMobExistInCorruption() 
      

    def read_floor(self):
        param =  self.current_floor if self.current_floor >  0 else  1
        for i in range(param, 22, 1):
            # print(i)
            res = isInMap(imagePath=imagePath(f"floor/{i}"))
            if res:
                print("character at floor", i)
                print("rf res", res, i)
                self.current_floor = i
                break
        
    def claim(self):
        #DONE CONDITION
      
        if self.first_time_claim == True:   
            afk(False)
            self.in_afk = False
            self.first_time_claim = False

        claimed = False
        while not claimed:
            if isImageExist(imagePath=imagePath("claim_reward"), region=(509, 340, 209 , 44)):
                clickOnImage(imagePath=imagePath("claim_reward"),  region=(509, 340, 209 , 44))
                time.sleep(0.5)
                click(558,353)
                time.sleep(0.8)

                if isImageExist(imagePath=asset_path("Exception/require_kill_all"), region=(583, 318, 199, 131)): #ABNORMALLY HAPPENED
                    click(682,411)
                    time.sleep(0.2)
                    return self.detect_location() 
              
                claimed = True
            else:
                if isImageExist(imagePath=asset_path("Common/character_on_map") ,region=(1265,153,5, 6)):
                    click(383, 442)
                else:
                    if isImageExist(imagePath=asset_path("Common/character_on_map"), region=(1247, 100, 65, 80)):
                        
                        walkToMapCoordinat(559, 314)
                        time.sleep(1)
                    else: return self.detect_location() #ABNORAMMLY CONNECTION RESOLVER
        
        if not  self.in_afk :  self.in_afk = afk(True)
        print("CLAIMMED")
        self.upstair()
               

    def upstair(self):
        while  isImageExist(imagePath=asset_path("Common/character_on_map"), region=(1247, 100, 65, 80)):
            #TRY UPSTAIR WHEN POINTER AT END OF MAP
                
            if isImageExist(imagePath=imagePath("corrupted_envoy_dialog")):
                if self.current_floor == self.max_floor or self.current_floor  == self.floor_limit:
                    afk(False)
                    self.in_afk = False
                    time.sleep(1)
                    clickOnImage(imagePath=imagePath("return_to_sg"))
                    time.sleep(0.2)
                    click(558,353)
                    self.first_time_claim = True
                    self.current_floor = 0#RESET FLOOR
                    waitForImage(imagePath=imagePath('city'))
                    return
                else:
                    click(586, 354)
                    time.sleep(0.2)
                    click(558,353)
                
            else:
                print("click to NPC")
                #clickOnImage(imagePath=imagePath("corrupted_envoy"), region=(252, 208, 364 ,310  ))
                click(383, 442)
     
        
        if  self.current_floor < self.max_floor: self.current_floor += 1
        time.sleep(3)

    def init(self):
        get_rid_annoying_error()
        try:
            if not self.is_prepared: self.prepare()
            while not self.done:  
                #REMOVE ANNOYING DIALOG
                if isImageExist(imagePath=imagePath("center_dialog"), region=(512, 432, 154,59)):
                    click(554, 458)
                    click(554, 458)
            
                self.detect_location()
            print("CORRUPTION DONE")
        except DieException as de:
            print("DIE")     


    def prepare(self):
        lootMode(item=True, radius=3)
        frost(True)
        click(1342, 197)
        self.is_prepared = True
        time.sleep(1)




