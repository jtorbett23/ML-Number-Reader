#!/bin/bash
cp pygame_core.py ./ui/pygame_core.py
cp pygame_ui.py ./ui/pygame_ui.py
python -m fastapi dev number_reader.py --port 8080