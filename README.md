# Python Image Recognition

This project was created as a demo for an interview. It allows you to upload an image from your local machine or a valid URL, and it will return a set of tags given the image provided. The image will be stored in a database with the metadata.

## Technology Stack

The project was built with the following technologies using a MacOS (Intel), version 11.6.2:

- MongoDB
- Flask
- Pillow
- Requests
- Imagga

## Getting Started

In order to get it setup within a local instance, the following steps needs to be followed.

### Prerequisites

- Docker
- Docker Compose
- Python 3
- Poetry
- MongoDB

### Running the Project

Within the root folder, the following command is used to create and build the containers

```
docker-compose build --no-cache
```

After the containers are built, it is time to run the containers

```
docker-compose up -d
```

After running the containers, you can check the application by going into the browser and checking `localhost:8080/images`

## Running Tests

To run the tests locally, you will need `poetry` installed. Then you can run

```
poetry install
```

This will create a virtual environment and install all the dependencies.

```
poetry shell
```

This will open a shell within the virtual environment. Then, you need to export the enviroment variables by running `export ENV_FILE_LOCATION=./.env.test`.

Finally, you can run the tests by running the following command

```
coverage run -m unittest --buffer
```

This will run all the tests provided in the `tests` folder and create a coverage report.
