# Store-Manager-v1
This is a simple store management application\
[![Build Status](https://travis-ci.org/codeMarble254/Store-Manager-v1.svg?branch=bg-fix-heroku-deployment-161331066)](https://travis-ci.org/codeMarble254/Store-Manager-v1)
[![Coverage Status](https://coveralls.io/repos/github/codeMarble254/Store-Manager-v1/badge.svg?branch=develop)](https://coveralls.io/github/codeMarble254/Store-Manager-v1?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/66cf3a604295b849139d/maintainability)](https://codeclimate.com/github/codeMarble254/Store-Manager-v1/maintainability)\
To run this project you should follow the following steps: \
**Find the web UI here**https://codemarble254.github.io/Store-Manager/UI/ 

**Find the app on heroku** https://jemo-store-manager.herokuapp.com/ 

1. Create a virual enviroment with the command
`$ virtualenv -p python3 env`

2. Activate the venv with the command
`$ source env/bin/activate`

3. Install git

4. clone this repo
`$ git clone https://github.com/codeMarble254/Store-Manager-v1.git`
5. cd into the folder \
`Store-Manager-v1`

5. export environment variables \
`$ export APP_SETTINGS="development"`
`$ export DB_NAME="development"`

6. create the dev database \
`createdb test_db`

6. create the testing database \
`$ createdb test_db`

5. Switch to `develop` branch \
`$ git checkout develop`

6. install requirements
`$ pip install -r requirements.txt`

now we are ready to run.

7. for tests on v1 run
`$ pytest -v`
8. for tests on v2 change to run \
Switch to the latest branch \
`bg-heroku-deployment-v2-161493704 `
Run \
`export APP_SETTINGS="testing"`
`pytest app/test/v2 -v --cov=app/test/v2`

8. for the application run \
`$ export SECRET_KEY="<your key>"`\
`export APP_SETTINGS="development"`
`$ export FLASK_APP=run.py`\
`$ flask run` \
If you ran the aplication you can test the various api endpoints using postman.

The api endpoints are

| Endpoint | Description |
| --- | --- |
| GET /products | Fetch all products |
| GET /products/productId | Fetch a single product record |
| GET /sales | Fetch all sale records |
| GET /sales/saleId | Fetch a single sale record |
| POST /products | Create a product |
| POST /sales | Create a sale order |
| POST /auth/signup | Signup a user |
| POST /auth/login | Login a user |

**Resources used** \
https://travis-ci.org/ \
https://apiary.io/ \
https://codeclimate.com/ \
https://coveralls.io/ 

**Acknowledgements** \
I acknowledge Andela Kenya for giving the platform to develop this product \
I also acknowledge my teammates for their collaboration



