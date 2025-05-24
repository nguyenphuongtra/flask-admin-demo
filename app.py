from flask import Flask, render_template_string, request, redirect, url_for
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

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    is_done = db.Column(db.Boolean, default=False)

class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email')
    column_searchable_list = ('username', 'email')
    column_filters = ('username',)
    can_view_details = True
    page_size = 10

admin = Admin(app, name='Admin', template_mode='bootstrap4')
admin.add_view(UserAdmin(User, db.session))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            new_todo = Todo(task=task)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for('index'))
    todos = Todo.query.all()
    return render_template_string('''
        <h2>Todo List - Nguyen Phuong Tra</h2>
        <form method="post">
            <input type="text" name="task" placeholder="New task" required>
            <button type="submit">Add</button>
        </form>
        <ul>
        {% for todo in todos %}
            <li>
                {% if todo.is_done %}<s>{{ todo.task }}</s>{% else %}{{ todo.task }}{% endif %}
                <a href="{{ url_for('toggle_todo', todo_id=todo.id) }}">[Toggle]</a>
                <a href="{{ url_for('delete_todo', todo_id=todo.id) }}" onclick="return confirm('Delete this task?')">[Delete]</a>
            </li>
        {% endfor %}
        </ul>
        <a href="/admin">Go to Admin</a>
    ''', todos=todos)

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.is_done = not todo.is_done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/test')
def test():
    return "This is a test page!"

if __name__ == '__main__':
    app.run(debug=True)