#!/bin/bash
source .env || echo "no .env file"
cp index.html ./ui/index.html
cp pygame_core.py ./ui/pygame_core.py
cp pygame_ui.py ./ui/pygame_ui.py
sed -i "s|!URL|$URL|g" ./ui/pygame_ui.py
sed -i "s|!URL|$URL|g" ./ui/index.html
python -m fastapi dev number_reader_with_ui.py --port 8080