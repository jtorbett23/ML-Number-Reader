from pyscript import window

if (window.navigator.maxTouchPoints <= 1):
    from pygame_ui_async import start as start_async
    print("ASYNC")
    start_async()
else:
    from pygame_ui_sync import start as start_sync
    print("SYNC")
    start_sync()
