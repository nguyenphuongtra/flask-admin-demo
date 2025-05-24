from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email')
    column_searchable_list = ('username', 'email')
    column_filters = ('username',)
    can_view_details = True
    page_size = 10

admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(UserAdmin(User, db.session))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template_string('''
        <h2>Chào mừng đến với ứng dụng Flask</h2>
        <p>Đây là trang chính.</p>
        <a href="{{ url_for('test') }}">Đi đến trang kiểm thử</a>||
        <a href="/admin">Đi đến Admin Panel</a>
    ''')

@app.route('/test')
def test():
    return "Trang kiểm thử!"

if __name__ == '__main__':
    app.run(debug=True)