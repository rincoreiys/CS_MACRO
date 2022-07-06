
import pyautogui, time, os, threading
import sys, os

# from Instance.Manager import Instance
sys.path.insert(0, os.getcwd())
# CONTROL SHORTCUT
from Helper.Exception import DieException,  EXCEPTIONS, LoginStuckException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Thread
import ctypes
from typing import Type

HWND = 197206
# DEPENDENCIES
def asset_path(path):
    return os.path.join(os.getcwd(), f"Assets/img/{path}.png")

def click( x=0, y=0, clicks=1):
    pyautogui.click(x=x, y=y, clicks=clicks)
    
def clickOnImage(imagePath, region = None, clicks = 1,  
    confidence=0.99, scroll_area=None, scroll_direction="Down",
     scroll_position=None, timeout=None) :

    if scroll_position is not None:
        pyautogui.moveTo(*scroll_area)
        #RESET POSITION FIRST
        pyautogui.scroll(400 * 10)
        #RESPOSITIONING
        pyautogui.scroll(-400 * (1 if scroll_direction == "Down" else -1) * scroll_position)
        time.sleep(0.5)

    #NPC
    result = None

    if timeout:
        for i in range(timeout):
            time.sleep(1)
            result = findImage(imagePath, region=region, confidence=confidence)  
            if result : break
    else:  
        result = findImage(imagePath, region=region, confidence=confidence)  

    if result:
        MPx, MPy = result
        click(MPx, MPy, clicks=clicks)

    return result is not None

def afkIfMobExist(loot_time=0, timeout=6):
    afk(True)
    verify = 0
    while verify < timeout * 2:
        
        time.sleep(0.5)
        if  checkMobExistance() :
            verify = 0
            
        else:
            pyautogui.press("`")
            verify += 1

    time.sleep(loot_time)
    afk(False)

def is_in_middle(): return  isImageExist(imagePath=asset_path("Common/character_on_map"), region=(1304, 174, 30, 20))
def is_in_end(): return isImageExist(imagePath=asset_path("Common/character_on_map"), region=(1247, 100, 65, 80))

def afkIfMobExistInCorruption():
    def fight_boss(): return isImageExist(imagePath=asset_path("Dungeon/Corruption/corr_boss"), region=(624, 74, 134, 39 ))
    # def fight_mob(): return isImageExist(imagePath=asset_path("Dungeon/Corruption/corr_mob"), region=(624, 74, 134, 39 ))
    #print("fight_mob", fight_mob)
    while not fight_boss() and is_in_middle():
        pyautogui.press("`")
        time.sleep(0.2)
        print("STILL IN MOB")
    
    #WAIT UNTIL BOSS FOUND

    #KILL THE    
    pyautogui.press("`")
    time.sleep(1)
    while fight_boss() and is_in_end()  :  
        pyautogui.press("`")
        time.sleep(0.2)
        print("AT BOSS")    
    
    while fight_boss() and is_in_middle() :   #ABNORMALL
        return afkIfMobExistInCorruption()

    return True #MEAN DONE

def press(key):
    pyautogui.press(key)

def moveOnImage(imagePath, region = None, timeout=10) :
    result = findImage(imagePath, timeout, region=region)  
    if result :  pyautogui.moveTo(*result)

def moveTo(x=1, y=1):
    pyautogui.moveTo(x,y)


def batchTryClick(imagePath, region=None,   confidence=0.99):
    for pos in pyautogui.locateAllOnScreen(imagePath, confidence=confidence, region=region):
        x, y, w, h = pos
        click(x,y)
        time.sleep(0.2)
    

def findImage(imagePath, region=None,  confidence=0.99) -> pyautogui.Point :

    result = pyautogui.locateCenterOnScreen(imagePath, confidence=confidence, region=region)
    return result
    # except Exception as ex:
    #     print(ex)
    #     return None
    # 
def checkPixelColorInRegion(rgb, region):
    x ,y , w, h = region
    for i in range(x, w+1):
        for ii in range(y, h+1):

            if  pyautogui.pixelMatchesColor(i, ii, rgb, tolerance=10): return True

    return False

def isImageExist(imagePath, region=None, confidence=0.99) :
    return findImage(imagePath, region, confidence) is not None

def isInMap(imagePath) :
    return findImage(imagePath, region=(1243, 70, 115, 34)) is not None

def check_2x_dungeon():
    return isImageExist(imagePath=asset_path("Options/x2dung"), region=(520, 382, 148, 28)) 

def waitForImage(imagePath, region=None, timeout=5):

    while not isImageExist(imagePath=imagePath, region=region):
        time.sleep(0.5)
        timeout -= 0.5
        if(timeout == 0): return False
    print("wait for image found")
    return True


def get_rid_annoying_error(loop:bool = False):
    print("OPERATION", threading.current_thread(), threading.main_thread())
    return
    #MOUNT DIALOG
    if isImageExist(imagePath=asset_path("Exception/close_chrome_warning"), region=(1160, 59, 205, 40)):
        clickOnImage(imagePath=asset_path("Exception/close_chrome_warning"), region=(1160, 59, 205, 40))
        time.sleep(1)

    if isImageExist(imagePath=asset_path("Exception/require_unmounted"), region=(615, 328, 138, 115)):
        click(682,411)
        time.sleep(0.2)
    if isImageExist(imagePath=asset_path("Exception/require_kill_all"), region=(583, 318, 199, 131)):
        click(682,411)
        time.sleep(0.2)
    

    print(threading.current_thread(), threading.main_thread())
    if loop:
        time.sleep(1)
        get_rid_annoying_error(loop)
    
    


# GAME APPROACH
def walkToMapCoordinat(x ,y, acknowledge=False):
    if not isImageExist(imagePath=asset_path("State/map_opened"), region=(837, 180, 316,  130))  : pyautogui.press("m")
    time.sleep(0.5)
    result = False
    pointer_region  = (x-15, y-15, 30, 30)
    if acknowledge:
        moveTo(680,220)
        result = isImageExist(imagePath=asset_path("Common/character_pointer"), region=pointer_region)
    click(x, y)
    pyautogui.press("m")  
    return result
    

def setCharacterMode(number=0):
    base_x = 120
    base_y = 95
    click(85,85)
    time.sleep(0.2)
    click(base_x + (20*number), base_y + (20*number))
    
def talkToNPCByMap(imagePath, scroll_position=None, direction="Down", confidence=0.99):
    pyautogui.press("m")
    time.sleep(0.5)
    #DONT BLOCK IMAGE BY MOUSE
    moveTo(680,220)
    if(scroll_position is not None):
        pyautogui.moveTo(1070,330)
        #RESET POSITION FIRST
        pyautogui.scroll(400 * 10)
        #RESPOSITIONING
        pyautogui.scroll(-400 * (1 if direction == "Down" else -1) * scroll_position)
        time.sleep(0.5)

    #NPC
    res = clickOnImage(imagePath, region=(831, 214,288, 259), confidence=confidence)
    print("res From TalktoNPC By Map", res, imagePath)
    time.sleep(0.5)
    pyautogui.press("m")

def mounting(state = True):
    result = isImageExist(imagePath=asset_path('State/mounted'), region=(22,132,20,20)) is not  state 
    if result :  pyautogui.press("z")

    return result


def afk(state = True, pressed = False, recursion=0 ):
    while not (isImageExist(imagePath=asset_path('State/afkON'), region=(192,63,776,61)) ==  state ):
        if pressed == False or recursion == 119 : 
            pyautogui.press(".")
            pressed = True
            time.sleep(0.5)
            if recursion == 120 : 
                print("NOT FOUND AFK")
                return False
            recursion += 1 
            
    print("FOUND AFK", state)
    return True

#STABLE

def checkMobExistance():
    return isImageExist(imagePath=asset_path('State/mob_existances'), region=(656,76,86,41))

def isMobDie():
    return not isImageExist(imagePath=asset_path('State/mob_existances'), region=(656,76,86,41))

#STABLE 

              
def party(state):
    result = isImageExist(imagePath=asset_path('State/party'), region=(0, 69, 28,28 )) is not  state 
    if result :
        pyautogui.press("p")
        time.sleep(0.5)
        x,y = (460, 495) if state else (460,515)
        pyautogui.click( x,y)
        pyautogui.press("p")

    return result

def frost(state):
    result = isImageExist(imagePath=asset_path('State/frost_on'), region=(196, 61, 660,120 )) is not  state 
    if result : pyautogui.press("s")

    return result

def set_pixie(state:bool):
    press("x")
    waitForImage(imagePath=asset_path("Dialog/pixie_tab"), region=(204,215,185,42))
    click(266, 232)
    time.sleep(0.5)
    click(162, 262)
    time.sleep(0.2)
    click((175 if state else 225), 384, clicks=2)
    press("x")

def lootMode(item = True, item_quality=2, equip=False, equip_quality=0, radius=1):
    if equip is item : item = not equip #PREVENT BOTH TRUE NEED TOGGLER
    if not  isImageExist(imagePath=asset_path('Dialog/AFKDialog')):
        click(828, 679)
        time.sleep(0.5)
        lootMode(item, item_quality, equip, equip_quality, radius)
    else:
        #CHECKLIST FIRST WORKING WITH TOGGLE CASE FOR EFFICIENCY
        #EQUIP
        if  isImageExist(imagePath=asset_path('State/checked'), region=(481, 531, 22, 22 )) is not equip:
            click(481 + (22/ 2), 531+(22/2))
        #ITEM
        if  isImageExist(imagePath=asset_path('State/checked'), region=(481, 548, 22, 22 )) is not item:
            click(481 + (22/ 2), 548+(22/2))

        #DETERMINE QUALITY
        #EQUIP
        if equip:
            click(660, 540)
            time.sleep(0.1)
            click(660, 555 + (17*equip_quality))

        if item:
            click(660, 560)
            time.sleep(0.1)
            click(660, 575 + (17*item_quality))

        #SET RADIUS
        #RESET FIRST
        for i  in range(3) : 
            click( 611 , 350) #DECRESE RADIUS
            time.sleep(0.1)
        #INCREASING RADIUS
        if radius > 1 :
            for i  in range(radius) :
                # print(i, range(radius) )
                click( 661 , 350) 
                time.sleep(0.1)
    

        click(828, 679)
        time.sleep(0.5)


def syntesis_aterfact():
    if isImageExist(imagePath=asset_path("State/inventory_indicator"), region=(322,186, 589,240)) : click(493, 682 )
    time.sleep(2)
    if clickOnImage(imagePath=asset_path("Common/item_syntesis_button"), region=(620, 255, 225,310 )):
        time.sleep(0.3)
        click(700,205)
        clickOnImage(imagePath=asset_path("Options/artefact_menu"),  scroll_area=(700,225), scroll_position=10)
        time.sleep(0.3)
        def synt():
            if clickOnImage(imagePath=asset_path("Props/artefact_essence"), region=(560, 230, 35,35 )):
                click(622,603, 5)
                time.sleep(0.5)
                click(676,606)
                time.sleep(5)

                #REFRESH
                click(700,222)
                time.sleep(0.2)
                click(700,260)
                time.sleep(0.2)
                click(700,222)
                time.sleep(0.2)
                click(700,240)
                time.sleep(0.3)
                synt()
            else:
                print("Nothing to synthetized")
                click(110,110)
                pyautogui.press("esc")

                return
        synt()

def check_attempt_and_enter(difficulty, dungeon_name):
    #BETA 1
    difficulty_x,  difficulty_y = (650, 355 + ( 20 * (difficulty - 1)))
    moveTo(620, 310)
    time.sleep(0.2)
    
    theres_attempt =  isImageExist(imagePath=asset_path(f"Dungeon/{dungeon_name}/zero_attempt"), region=(620, 340, 200, 70)) == False
    if theres_attempt:
        click(difficulty_x , difficulty_y)
        time.sleep(2.5)
    else: click(590, 415) #CLICK BACK    
    # time.sleep(0.5)
    return theres_attempt 


def sell_equip(dungeonClass):
    #FROM BOTTOM TO LEFT TO TOP
    #CLICK PAGE 6 FIRST
    last_x = 625
    last_y = 470
    last_page_coordinate = [615, 495]
    
    if isImageExist(imagePath=asset_path("Dialog/sg_seller"), region=(496, 238, 183 ,57   )):
        time.sleep(0.5)
        click(545,355)
        
        if dungeonClass.backpack_settling_attempt == 2:
            for sell in range(2): #NEED IT FOR 2x CHECKING
                for page in range(6, 2, -1):
                    time.sleep(0.5)
                    page_x, page_y = last_page_coordinate[0] - (30 * ( 6 - page  )), last_page_coordinate[1] 
                    moveTo(page_x, page_y)
                    time.sleep(0.1)
                    click(page_x, page_y,2 )
                    time.sleep(0.5)
                    
                    moveTo(page_x, page_y+35)
                    for i in range(6):
                        for ii in range(6):
                            bag_slot_x = last_x - (30*i)
                            bag_slot_y =  last_y - (30*ii)
                        
                            if not isImageExist(imagePath=asset_path("State/empty_bag_slot"), region=(bag_slot_x-15, bag_slot_y-15, 30,30)):
                                    #CLICK SELL BUTTON
                                click(330, 542)
                                time.sleep(0.1)
                                click( bag_slot_x , bag_slot_y)
                                time.sleep(0.3)
                                # print(f"({page},{last_x - (30*i)}, {last_y - (30*ii)})")
                                if clickOnImage(imagePath=asset_path("Common/confirm"), region=(584,441,93,29)):
                                    time.sleep(0.1)
                                    #REPEAT
                                    click(330, 542)
            click(110,110)
            pyautogui.press("esc")
            pyautogui.press("esc")
            return
        else:
            talkToNPCByMap(imagePath=asset_path("NPC Link/sg_seller"), scroll_position=3)
            dungeonClass.backpack_settling_attempt += 1 
    else:
        talkToNPCByMap(imagePath=asset_path("NPC Link/sg_seller"), scroll_position=3)
        time.sleep(1)
        
    
    sell_equip(dungeonClass)
 

def login(instance, character, retry=0):
    instance.focus()
    magic_link = f"https://www.r2games.com/play/?game=10&server={character['server_id']}&account={character['account']}&password={character['password']}"
    try:
        instance.go(magic_link)
        myElem = WebDriverWait(instance.driver, 60).until(EC.presence_of_element_located((By.ID, 'flashcontent')))
        print(myElem, "is ready!")
        get_rid_annoying_error()
        if waitForImage(imagePath=asset_path(f"Character/{character['character']}"), timeout=60) is False: raise TimeoutException
        clickOnImage(imagePath=asset_path(f"Character/{character['character']}"), clicks=2)
        if  waitForImage(imagePath=asset_path(f"State/online_indicator"), timeout=60) is False : raise TimeoutException
        else: return True

    except TimeoutException as te:
        print("Loading took too much time!")
        login(instance, character, retry = +1) #RECURSION FOR TIMEOUT LOGIN

 
    
    # return False
    #PHASE 1

# check_attempt_and_enter(3)
def raise_exception_in_thread(t:Thread, e: Type[BaseException]):
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(t.ident), ctypes.py_object(e))

def detect_error(thread=threading.main_thread()): 
    # raise_exception_in_thread(thread, Exception )
    # raise Exception("failed")
    while True:
        for ex in EXCEPTIONS:
            res = isImageExist(asset_path(f"Exception/{ex['recognition']}"))
            if res and ex["termination"] is not None :  
                print("RAISED", ex["type"])
                raise_exception_in_thread(thread, ex["termination"] )
                return 
            time.sleep(0.5)
            # print("detect error still running")

