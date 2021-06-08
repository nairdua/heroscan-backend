# HeroScan

Backend for the HeroScan service, capstone project
for Bangkit 2021 program. Handles prediction requests
and responses.

## Running

**Note**:  
* This project mainly uses **Python 3.7.x**. Other versions can cause unexpected behavior.  
* It's recommended to use [`pyenv`](https://github.com/pyenv/pyenv) to manage multiple Python versions in one machine.  
* To keep your Python install clean, it's also recommended to use [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv). Create a virtualenv specifically for this project.  

1. Clone this repository.
2. Install requirements
  * Run `pip install -r requirements.txt` in the terminal.
3. Run application
  * Run `export FLASK_APP=main.py ; flask run` in the terminal.
4. Make prediction requests
  * It's recommended to use [Postman](https://www.postman.com) to mock API requests
  * The request's body must contain a `file` variable which is the image to be scanned.
