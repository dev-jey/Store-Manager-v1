from app import create_app
from instance.config import Config

app = create_app(config_name="development")

'''Call the main flask app'''

if __name__ == "__main__":
    app.run()
