#!/bin/bash
source .env || echo "no .env file"
cp index.html ./ui/index.html
cp pygame_core.py ./ui/pygame_core.py
cp pygame_ui.py ./ui/pygame_ui.py
cp pygame_ui_sync.py ./ui/pygame_ui_sync.py
cp pygame_ui_async.py ./ui/pygame_ui_async.py
sed -i '' -e "s|!URL|$URL|g" ./ui/pygame_ui_sync.py
sed -i '' -e "s|!URL|$URL|g" ./ui/pygame_ui_async.py
sed -i '' -e "s|!URL|$URL|g" ./ui/index.html
python -m fastapi dev number_reader_ui_only.py --port $PORT_UI