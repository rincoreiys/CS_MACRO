import win32gui, win32con
import win32process as wproc
import win32api as wapi
window_name_search = ""
window_find_result = ""

def findWindowByName(window_name):
    global window_name_search 
    global window_find_result
    window_find_result = None
    window_name_search = window_name
    win32gui.EnumWindows( winEnumHandler, None )
    return window_find_result

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        global window_name_search
        global window_find_result
        window_text =  win32gui.GetWindowText( hwnd )
        hex_addr = hex(hwnd)
        print (hwnd, window_text)
        if window_text  == window_name_search and window_find_result is None :
            window_find_result  = hwnd

def focus(hwnd):
    try:
        remote_thread, _ = wproc.GetWindowThreadProcessId(hwnd)
        wproc.AttachThreadInput(wapi.GetCurrentThreadId(), remote_thread, True)
        win32gui.SetFocus(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetWindowPos(hwnd,win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
        win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
        win32gui.SetWindowPos(hwnd,win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
    except Exception as ex:
        print(ex)
   
print("result", findWindowByName("New Tab - Google Chrome"))
# focus(787346)