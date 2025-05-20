from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))

admin = Admin(app, name='Admin', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))

@app.route('/')
def index():
    return '<h2>Welcome to Flask Admin!</h2>'

if __name__ == '__main__':
    app.run(debug=True)
