# MNIST Number Reader

This is a project that uses Pygame to draw numbers which are read by a tensorflow machine learning model trained on the MNIST number data set.

This is made up of a static site hosted on Github Pages which makes API calls to a fastapi hosted on Cloud Run which handles running the machine learning model.

Github Pages Url - https://jtorbett23.github.io/ML-Number-Reader

# Tech Stack

- Python (3.11)
    - [Pygame](https://www.pygame.org/news) - For the UI.
    - [Pyscript](https://pyscript.com) To run pygame on a webpage.
    - [Tensorflow](https://www.tensorflow.org) - For creating the machine learning model.
    - [fastapi](https://fastapi.tiangolo.com) - For handling requests to the machine learning model.
- HTML/CSS/Javascript
    - For the webpage, styling, and background effect.
- [Docker](https://www.docker.com) - To containerise the application for deployment on Google Cloud's Cloud Run.

# Hosting

- [Google Cloud](https://cloud.google.com/?hl=en) - To host the api running the machine learning model.
    - For this I use a docker container via [Cloud Run](https://cloud.google.com/run?hl=en).
- [Github Pages](https://docs.github.com/en/pages) - To host the UI that will communicate with Google Cloud.

# Project Commands

## Installation

`pipenv install --dev`

## Local Development

- Create and train model on MNIST dataset (with random noise added) - `pipenv run create`
- Run pygame locally with model - `pipenv run local-game`
- Run an api that hosts both the ui and tensorflow to read numbers for development - `pipenv run api`
- Run an api that only hosts tensorflow return the guessed number for development - `pipenv run api-reader`
- Run an api hosting only the ui - `pipenv run api-ui`
- Run two apis where one hosts tensorflow and the other the ui - `pipenv run api-split`

## Deployment and Production

- Prepare code for Github Pages and push to branch (which is setup to deploy) - `pipenv run gh-pages`
- Run api that will read images and return the guessed number for development - `pipenv run api-prod`
