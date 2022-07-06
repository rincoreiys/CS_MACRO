from dataclasses import dataclass
import sys, os
sys.path.insert(0, os.getcwd())
from Gameplay.operation import *
from Helper.Exception import DisconnectException

@dataclass
class Dungeon:
    free_attempt_done:bool = False
    dg2x_attempt_done:bool = False
    dk_attempt_done:bool = False
    is_prepared:bool =False
    current_run:int = 0
    require_dk:bool = False
    is_2x_dungeon:bool = False
    active_index:int = 0
    done:bool = False
    inner_position:int = 1
    dg_name: str = ""
    dg_classify:int = 1 # IN DG TELEPORT CLASSING
    dg_index_number:int = 1 # IN DG TELEPORT DG NUMBERING
    loot_time:int = 7
    backpack_settling_attempt:int = 1
    loot_config:dict = None
    index:set = None
    difficulty:int = 3 #1 normal 2 hard 3 NM (DEFAULT)
    boss_coordinate:dict = None
    seller_link:str = ""
    index:dict = None
    #MAP DETECTION CONFIG
    
    main_city_map_img: str = "Map/sg"
    seller_link: str = "NPC Link/sg_seller"
    bag_already_empty_before: bool = True
    init_pixie:bool = True
    in_main_city:bool = False

    on_enter_triggered:bool = False
    event = {
        "change": None
    }

    def __setattr__(self, __name: str, __value: object) -> None:
        super().__setattr__(__name, __value)
        onChange = self.event["change"]
        print("VARIABLE CHANGED")
        if onChange  is not None : onChange()

        
        
    def imagePath(self, file): return asset_path(f"Dungeon/{self.dg_name}/{file}")

    def prepare(self):
        #HAVE BEEN DYNAMICALLY
        lootMode(**self.loot_config)
        if not self.init_pixie: set_pixie(False)
        self.is_prepared = True
    
    def generate_index(self):
        self.index = {}
        self.index[0] = {
            "title" : "Talk to Entrance NPC",
            "desc" : "Teleport to Dungeon and Talk to DG NPC"
        }

        for i in range(1, len( self.boss_coordinate)+ 1):
            self.index[i] = {
                "title" : f"Killing Boss {i}" ,
                "desc" : "Walk to Boss and Kill"
            }
         
        self.index[ len( self.boss_coordinate)+ 1] = {
            "title" : "Exit",
            "desc" : "Dungeon done"
        }
        return self.index
    
    def init(self):
        self.dg_name = (self.__class__.__name__).replace("D", "")
        self.entrance_map_img  = f"Dungeon/{self.dg_name}/entrance"
        self.dungeon_map_img = f"Dungeon/{self.dg_name}/dungeon"

        #LINK
        self.entrance_npc_link = f"Dungeon/{self.dg_name}/dg_npc_link"
        
        #HAVE BEEN DYNAMICALLY
        try:
            while not self.done:
                get_rid_annoying_error()
                if not self.is_prepared: self.prepare()
                self.detect_location()
        except DisconnectException as de:
            print("character disconnected need Re-login" ,de)


         
    def kill_boss(self):
        afk(False)
        boss_coordinate = self.boss_coordinate[self.inner_position]
        arrive =   walkToMapCoordinat( *boss_coordinate, acknowledge=True)
        if arrive:
            afkIfMobExist(loot_time=self.loot_time)

            self.inner_position += 1
            if self.inner_position == len(self.boss_coordinate) + 1:  
                self.exit()


    def in_one_of_city(self):
        for city in ["sg", "tol", "bloodfang", "bloodsheed" ]:        
            if isInMap(imagePath=asset_path(f"Map/{city}")): 
                return True
        return False
    
  
    def detect_location(self):
        #ENTRANCE DGm
        # print(asset_path(self.entrance_map_img))
        if isInMap(imagePath=asset_path(self.entrance_map_img)):
            self.talk_to_entrance_npc()
        #IN DG
        elif self.in_one_of_city():
            if isInMap(imagePath=asset_path(f"{self.main_city_map_img}")):
                self.get_rid_junk()
                self.teleport()
            else:
                self.go_to_main_city()
           

        elif isInMap(imagePath=asset_path(self.dungeon_map_img)):
            if not self.on_enter_triggered:
                self.on_enter()
                self.on_enter_triggered = True
            self.kill_boss()
    
    def teleport(self):
        #HAVE BEEN DYNAMICALLY
        base_y = 355
        base_x = 685
        while not isInMap(imagePath=self.imagePath("entrance")):
            if isInMap(imagePath=asset_path(self.main_city_map_img)):
                if isImageExist(imagePath=asset_path("Dialog/dg_teleport"), region=(495, 246, 159 ,71  )):
                    click(base_x, base_y + ( 20 * (self.dg_classify - 1) ))
                    time.sleep(0.5)
                    click(base_x, base_y + ( 20 * (self.dg_index_number - 1) ))
                    time.sleep(2)
                else:
                    talkToNPCByMap(imagePath=asset_path("NPC Link/dg_teleport"), scroll_position=2)

    def get_rid_junk(self):
        if "equip" in self.loot_config and not self.bag_already_empty_before:
            setCharacterMode()
            sell_equip(self)
            syntesis_aterfact()
            self.bag_already_empty_before = True
        elif  "item" in self.loot_config: pass

    def go_to_main_city(self): 
        base_y = 355
        base_x = 685
        city_index = 1
        scroll_position = 2
        if isInMap(imagePath=asset_path("Map/tol")):  pass
        elif isInMap(imagePath=asset_path("Map/bloodfang")):  pass
        elif  isInMap(imagePath=asset_path("Map/bloodsheed")): 
            scroll_position = None
            city_index = 2
      
        #TELEPORTING TO MAIN CITY
        while not  isInMap(imagePath=asset_path(f"{self.main_city_map_img}")):
            if isImageExist(imagePath=asset_path("Dialog/teleport"),  region=(495, 246, 159 ,71  ) ) :
                click(base_x, base_y + ( 20 * (city_index - 1) ))
                time.sleep(2)
            else:
                talkToNPCByMap(imagePath=asset_path("NPC Link/teleport"), scroll_position=scroll_position)


    def talk_to_entrance_npc(self):
        base_opt_x, base_opt_y = (540 , 355 )
        party(True)
        mounting(False)
        if isImageExist(imagePath=asset_path("Dialog/entrance_npc") , region=(514, 342, 45 , 30  )):
            self.is_2x_dungeon = check_2x_dungeon()

            #PREFERABLE CHOOSE 2x attempt FIRST
            if not self.dg2x_attempt_done and self.is_2x_dungeon: 
                click(base_opt_x, base_opt_y + 40)
                if not check_attempt_and_enter(self.difficulty, self.dg_name) :  self.dg2x_attempt_done = True
                else: 
                    self.bag_already_empty_before = False
                    self.inner_position = 1 #DEFAULT
                return

            if not self.free_attempt_done: 
                click(base_opt_x, base_opt_y)
                if not check_attempt_and_enter(self.difficulty, self.dg_name) : self.free_attempt_done = True
                else: 
                    self.bag_already_empty_before = False
                    self.inner_position = 1 #DEFAULT
                return

            if not self.dk_attempt_done and self.require_dk: 
                click(base_opt_x, base_opt_y+20)
                if not  check_attempt_and_enter(self.difficulty, self.dg_name) :   self.dk_attempt_done = True
                else: 
                    self.bag_already_empty_before = False
                    self.inner_position = 1 #DEFAULT
                return

            print("Free attempt", self.free_attempt_done , "paid" , self.dk_attempt_done)
            self.done =  (
                 self.free_attempt_done and 
                (self.dg2x_attempt_done == self.is_2x_dungeon) and
                (self.dk_attempt_done == self.require_dk) 
                ) 
            if self.done : self.on_done()
            return
                #BACK TO CITY
           
        else:
            talkToNPCByMap(imagePath=asset_path(self.entrance_npc_link))

    def on_enter(self): pass


    def on_done(self): 
        #WORK ON SAFE PLACE ONLY 30, 55, 75, 85 CORNER, 125, 165, 175, 195, 255, 295
        click(577,615)
        while isInMap(asset_path(self.entrance_map_img)): time.sleep(0.5)
        if self.dg_name != "125" :  self.go_to_main_city() #PREVENT ERROR DG 125 AMBIGOUSITY SAME ENTRANCE AND MAP
        if not self.init_pixie: set_pixie(True) #RESTORE BACK PIXIE
        self.get_rid_junk()
        time.sleep(1.5)

    def default_exit(self):
        self.on_enter_triggered = False
        while not isInMap(imagePath=self.imagePath("entrance")):
            time.sleep(0.5) #WAIT UNTIL REALLY LEAVEDUNGEON
        #self.detect_location()
        
    def exit(self):
        #HAVE BEEN DYNAMICALLY
        party(False)
        self.default_exit()
       
        
     
