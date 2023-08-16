# Steps to build Docker Image

# Step 1: Define the name of the image we'll be using
## This is the base image that we'll pull from Dockerhub that we'll then 
## build on top of to add the dependencies to for our project

## We use the alpine version here because it is a simple version of the Linux
## That allows for a lightweight and efficient image to use for Docker
FROM python:3.9-alpine3.13
LABEL maintainer="Enrique Alvarado"

## This is reccomended when you are running python in a Docker container
## Makes it so that there is no buffer from our terminal to the screen of our app
ENV PYTHONUNBUFFERED 1

# This block copies everything from our requirements file to our Docker image
COPY ./requirements.txt /tmp/requirements.txt
## Just like with the requirements.txt file, we're copying it to the tmp directory so we have it available during the build phase
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
## We then copy everything from our app directory to /app in our Docker container
COPY ./app /app
## We then set our workdir which is the default directory where we run all our commands from
WORKDIR /app
## This line tells us to expose port 8000 on the Docker container so we can connect to the development server
EXPOSE 8000

## Defines a build argument called DEV and sets the default value to false
### Remember, this is overwritten in docker-compose file by setting args: DEV=true
ARG DEV=false
## We specifically made this a run block instead of putting run on every line so that there aren't any unneccessary layer in our container
## The first line creates a virtual environment so that there aren't any conflicting dependencies
RUN python -m venv /py && \
    ## This next line upgrades the python package manager in our virtual environment
    /py/bin/pip install --upgrade pip && \
    ## This line installs the list of requirements we made in our Docker image
    /py/bin/pip install -r /tmp/requirements.txt && \
    ## This is eesential shellscript that runs an if statement
    ### Makes it so that if DEV=true, then run the code that follows
    ### You also end if statements in shell script by doing if backwards (fi)
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    ## We then remove the tmp directory bc we don't want any extra dependencies on our image
    ### It is best practice to keep Docker images as lightweight as possible
    ### If you ever use any temporary files, insert them, use them, but make sure to delete them before the end
    ### of the Docker file
    rm -rf /tmp && \
    ## Adds a new user inside our image, as it is frowned upon to use the root user
    ## DONT RUN YOUR APPLICATION AS A ROOT USER, BC THEN ATTACKERS WILL HAVE FULL CONTROL OF THE CONTAINER
    ## using a new user mitigates the amount of damage attackers can do
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
## This line updates the PATH env variable to make it so that any command we run will always run from our venv
ENV PATH="/py/bin:$PATH"

## This line specifies the user we are switching to in our Docker file to run these commands
USER django-user