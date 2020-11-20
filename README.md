# ImageOCR

## Overview

This project is to detect the necessary information in the image using Google Vision API.

## Structure

- src

    The source code to extract the necessary data in the image

- utils
    
    * credential key for Google Vision API
    * The source code to communicate with Google Vision API and manage the folder and files in this project

- app

    The main execution file
    
- requirements

    All the necessary dependencies for this project
    
## Installation

- Environment

    Ubuntu 18.04, Windows 10, Python 3.6

- Dependency Installation

    Please go ahead to this project directory and run the following commands in the terminal
    
    ```
        pip3 install -r requirements.txt
    ```
 
 - Please make the new folder named "credential" into utils folder and copy your Google Vision Api credential key into it.

## Execution

- Please run the following command in the project directory.

    ```
        python3 app.py
    ```
