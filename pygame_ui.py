from pyscript import window
from pygame_ui_async import start as start_async
from pygame_ui_sync import start as start_sync


agent = window.navigator.userAgent.lower()

if("iphone" in agent or "android" in agent):
    start_sync()
else:
    start_async()