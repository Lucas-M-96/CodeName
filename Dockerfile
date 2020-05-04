# Use the Python3.8.2 image based on alpine
FROM python:3.8.2-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# install c compiler and build tools
# https://github.com/gliderlabs/docker-alpine/issues/158
RUN apk add build-base linux-headers pcre-dev

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to use flask dev server (VERY BAD)
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
CMD ["flask", "run", "--host=0.0.0.0"]

