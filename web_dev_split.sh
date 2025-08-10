#!/bin/bash
cp pygame_core.py ./ui/pygame_core.py
cp pygame_ui.py ./ui/pygame_ui.py
python -m fastapi dev number_reader.py --port 8080 &
python -m fastapi dev number_reader_ui_only.py --port 8084