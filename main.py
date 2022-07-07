import asyncio
def _init():
  try:
    from Helper.socket_handler import  listen
    asyncio.new_event_loop().run_until_complete(listen())
  except KeyboardInterrupt as ki:
    print("Program Closed by user")

if __name__ == "__main__": _init()
    

    
    

  