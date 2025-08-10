#!/bin/bash
git checkout master
git branch -D gh-pages
git checkout -b gh-pages
cp pygame_core.py ./ui/pygame_core.py
cp pygame_ui.py ./ui/pygame_ui.py
rm -r ./*.py
rm -r ./*.h5
rm -r ./*.md
rm -r ./*.lock
rm -r ./Pipfile
rm -r ./Dockerfile
mv ui/* ./
rm -r ./ui
rm -r ./gh-pages.sh
git add .
git commit -m "pages"
git push --set-upstream origin gh-pages -f 