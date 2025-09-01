from pyscript import window
agent = window.navigator.userAgent.lower()

if("iphone" in agent or "android" in agent):
    from pygame_ui_sync import start as start_sync
    start_sync()
else:
    from pygame_ui_async import start as start_async
    start_async()