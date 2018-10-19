# Store-Manager-v1
This is a simple store management application\
[![Build Status](https://travis-ci.org/codeMarble254/Store-Manager-v1.svg?branch=bg-fix-heroku-deployment-161331066)](https://travis-ci.org/codeMarble254/Store-Manager-v1) [![Coverage Status](https://coveralls.io/repos/github/codeMarble254/Store-Manager-v1/badge.svg?branch=ft-signup-api-161309703)](https://coveralls.io/github/codeMarble254/Store-Manager-v1?branch=ft-signup-api-161309703) [![Maintainability](https://api.codeclimate.com/v1/badges/836fa03585ea46a6136d/maintainability)](https://codeclimate.com/github/codeMarble254/Store-Manager-v1/maintainability)\
To run this project you should follow the following steps:

1. Create a virual enviroment with the command
`$ virtualenv -p python3 env`

2. Activate the venv with the command
`$ source env/bin/activate`

3. Install git

4. clone this repo
`$ git clone https://github.com/codeMarble254/Store-Manager-v1.git`

5. install requirements
`$ pip install -r requirements.txt`

now we are ready to run.

6. for tests run
`$ pytest -v`
7. for the application run \
`$ export SECRET_KEY="<your key>"`\
`$ export FLASK_APP=run.py`\
`$ flask run` \
If you ran the aplication you can test the various api endpoints using postman.

The api endpoints are

| Endpoint | Description |
| --- | --- |
| GET /products | Fetch all products |
| GET /products/<productId> | Fetch a single product record |
| GET /sales | Fetch all sale records |
| GET /sales/<saleId> | Fetch a single sale record |
| POST /products | Create a product |
| POST /sales | Create a sale order |
| POST /auth/signup | Signup a user |
| POST /auth/login | Login a user |
