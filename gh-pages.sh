#!/bin/bash
git checkout master
git branch -D gh-pages
git checkout -b gh-pages
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