from app import create_app
from instance.config import Config

app = create_app(Config.APP_SETTINGS)

'''Call the main flask app'''

if __name__ == "__main__":
    app.run()
