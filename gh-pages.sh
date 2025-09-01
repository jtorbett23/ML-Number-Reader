#!/bin/bash
source .env || echo "no .env file"
# git checkout master
git branch -D gh-pages
git checkout -b gh-pages
cp index.html ./ui/index.html
cp pygame_core.py ./ui/pygame_core.py
cp pygame_ui.py ./ui/pygame_ui.py
cp pygame_ui_sync.py ./ui/pygame_ui_sync.py
cp pygame_ui_async.py ./ui/pygame_ui_async.py
sed -i "s|!URL|$GHPAGES_URL|g" ./ui/pygame_ui_sync.py
sed -i "s|!URL|$GHPAGES_URL|g" ./ui/pygame_ui_async.py
sed -i "s|!URL|$GHPAGES_URL|g" ./ui/index.html
rm -r ./*.py
rm -r ./*.h5
rm -r ./*.md
rm -r ./*.lock
rm -r ./Pipfile
rm -r ./Dockerfile
mv ui/* ./
rm -r ./ui
rm -r ./*.sh
git add .
git commit -m "pages"
git push --set-upstream origin gh-pages -f 