import asyncio
from Helper.socket_handler import  listen
def _init():
  asyncio.new_event_loop().run_until_complete(listen())


if __name__ == "__main__": _init()
    

    
    

  