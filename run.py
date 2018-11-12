from app import create_app
from instance.config import Config

app = create_app(config_name="development")


@app.route("/")
def index():
    return "<p>Find the app documentation <a href='https://jemostoremanager.docs.apiary.io/'>here</a></p>"

'''Call the main flask app'''

if __name__ == "__main__":
    app.run()
