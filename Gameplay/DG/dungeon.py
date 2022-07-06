
from dataclasses import dataclass
import sys, os, json
sys.path.insert(0, os.getcwd())
from Helper.Template import Dungeon
from Gameplay.operation import *
@dataclass
class D30(Dungeon):
    dg_index_number: int = 2
    # dg_name: str = "30"
    def __post_init__(self):
        self.boss_coordinate = {
            1: (475, 405),
            2: (834, 282),
            3: (896, 468)
        }

@dataclass
class D55(Dungeon):
    dg_index_number: int = 7
    def __post_init__(self):
        self.boss_coordinate = {
            1: (872, 417),
            2: (485, 504),
            3:  (877, 500),
        }

    def on_done(self):
        self.bag_already_empty_before = False
        click(577,615)
        waitForImage(imagePath=asset_path(self.main_city_map_img), region=(1243, 70, 115, 34))

@dataclass
class D75(Dungeon):
    dg_index_number: int = 6
    dg_name: str = "75"
    in_chamber: bool = False
    # inner_position: int = 3
    chamber_entrance = {
        1: { 
            "point" : (785,399),
            "npc_position": (784,286),
        },
        2: {
            "point" : (735,362),
            "npc_position": (806,293),
        },
        3:  {
            "point" : (634,385),
            "npc_position": (568,335),
        },
        4: {
            "point" : (598,440),
            "npc_position": (605,339),
        } ,
        5:  {
            "point" :(601,528),
            "npc_position": (573,315),
        },
    }

    def __post_init__(self):
        self.boss_coordinate = {
            1: (850, 357),
            2: (768, 299),
            3: (586, 337),
            4: (522, 437),
            5: (517, 531),
        }
    
    def kill_boss(self):
        afk(False)
        boss_coordinate = self.boss_coordinate[self.inner_position]
        entrance_coordinate = self.chamber_entrance[self.inner_position]
       
        if  self.in_chamber : 
            afkIfMobExist(loot_time=1, timeout=2.5)
            
            while self.in_chamber:
                if  self.inner_position == len(self.boss_coordinate):
                    self.in_chamber = False
                    self.exit()
                    

                if isImageExist(imagePath=self.imagePath("entrance_chamber_dialog"), region=(495, 246, 159 ,71 )):
                    click(569, 353)
                   
                    if isImageExist(imagePath=self.imagePath("entrance_chamber_dialog"), region=(495, 246, 159 ,71 )):
                        click(569, 353)
                        self.in_chamber = False
                        self.inner_position += 1
                        # time.sleep(0.5)
                        #PREVENT OVERLAPPING DIALOG
                        click(569, 373)

                else:
                    
                     #RETURN IF INNER BOSS ALL KILLED
                    press("m")
                    for i in range(260, 245 + (13*11), 13):
                        click(980, i)
                        time.sleep(0.02)
                    press("m")
                    time.sleep(0.5)
            
        else:
            while not self.in_chamber:
                mounting(False)
                arrive_to_chamber_entrance = walkToMapCoordinat( *entrance_coordinate['point'], acknowledge=True)
                if arrive_to_chamber_entrance:
                    click( *entrance_coordinate['npc_position'])
                    waitForImage(imagePath=self.imagePath("entrance_chamber_dialog"), region=(506, 250, 140 ,35 ), timeout=3)

                if isImageExist(imagePath=self.imagePath("entrance_chamber_dialog"), region=(495, 246, 159 ,71 )):
                    click(569, 353)
                    if isImageExist(imagePath=self.imagePath("entrance_chamber_dialog"), region=(495, 246, 159 ,71 )):
                        click(569, 353)
                        time.sleep(1)
                        self.in_chamber = True
                  
                        walkToMapCoordinat(*boss_coordinate)
                        time.sleep(2 + (self.inner_position / 4 ))
              

@dataclass
class D85(Dungeon):
    dg_index_number: int = 7
    # dg_name: str = "85"
    difficulty: int = 1
    def __post_init__(self):
        self.boss_coordinate = {
            1: (898, 376),
            2: (770, 435),
            3:  (635, 505),
            4:  (466, 400),
            5:   (661, 384),
            6:  (689, 290),
            7:   (547, 326)
        }

@dataclass
class D110(Dungeon):
    dg_classify: int = 2
    dg_index_number: int = 1
    dg_name: str = "110"
    index = [
        "Talk To NPC",
        "Kill Boss 1",
        "Kill Boss 2",
        "Kill Boss 3",
        "Kill Boss 4",
        "Exit",
    ]
    def __post_init__(self):
        self.boss_coordinate: set = [
            (464, 478),
            (897, 478),
            (654, 276),
            (686, 425),
        ]

@dataclass
class D165(Dungeon):
    dg_classify: int = 2
    dg_index_number: int = 3
    # dg_name: str = "165"
    buff_taken:bool = False
    def __post_init__(self):
        self.boss_coordinate = {
            1:(785, 310),
            2:(585, 310),
        }

    def on_enter(self):
        #TAKE BUFF
        while not isImageExist(imagePath=self.imagePath("exit_npc_dialog"), region=(495, 246, 159 ,71  )):
            talkToNPCByMap(imagePath=self.imagePath("exit_npc_link"))
            time.sleep(0.5)

        click(600, 355 )
    
    def exit(self):
        while not isImageExist(imagePath=self.imagePath("exit_npc_dialog"), region=(495, 246, 159 ,71  )):
            talkToNPCByMap(imagePath=self.imagePath("exit_npc_link"))
            time.sleep(0.5)
        
        click(600, 395 )
        self.default_exit()

    


@dataclass
class D175(Dungeon):
    dg_name: str = "175"    
    dg_classify:int = 2
    dg_index_number: int = 4
    #MAPPING
  
    def __post_init__(self):
        self.boss_coordinate = {
            1: (500, 400),
            2: (685, 490),
            3: (595, 355),
            4: (780, 445),
            5: (690, 310),
            6: (875, 400),
            7: (860, 310), 
        }     

    def exit(self):    
        if isImageExist(imagePath=self.imagePath("exit_dg_npc_dialog"), region=(495, 246, 159 ,71  )):
            clickOnImage(imagePath=self.imagePath("teleport_to_sg"), region=(500, 363, 326 , 24  ))
            time.sleep(4)
            self.inner_position = 1
            self.bag_already_empty_before = False
            return
        else:
            talkToNPCByMap(imagePath=self.imagePath("exit_dg_npc_link"))
            time.sleep(1)
           #PREVENT LAG WHEN AUTO DISABLE
        self.exit()
     

with open('D175.json', 'w') as f:
    json.dump(D175().generate_index(), f)
