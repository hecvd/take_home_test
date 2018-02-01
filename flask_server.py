from flask import Flask
from blueprints.celebration_blueprint import guest_list_page


app = Flask(__name__)
app.register_blueprint(guest_list_page)

if __name__ == '__main__':
    app.run()
