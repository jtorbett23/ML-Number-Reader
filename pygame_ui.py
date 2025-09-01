from pyscript import window
from pygame_ui_async import start as start_async
from pygame_ui_sync import start as start_sync


agent = window.navigator.userAgent.lower()

if("iphone" in agent or "android" in agent):
    print("MOBILE")
    start_sync()
else:
    print("WEB")
    start_async()