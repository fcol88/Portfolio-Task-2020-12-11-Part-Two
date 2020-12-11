import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/task_list.db'
db = SQLAlchemy(app)

app.debug = True

# define user class - heavily stripped back from in app memory version
class User(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    firstName=db.Column(db.String(100), nullable=False)
    lastName=db.Column(db.String(100), nullable=False)
    pin=db.Column(db.String(4), nullable=True)
    created=db.Column(db.DateTime, nullable=False)

    # returns user as a string
    def __str__(self):
        return "User: {0} {1}".format(self.firstName, self.lastName)

    # returns code used to instantiate object
    def __repr__(self):
        obj_repr = f'id: {self.id},' \
                   f'firstName: {self.firstName},' \
                   f'lastName: {self.lastName},' \
                   f'pin: [PROTECTED],' \
                   f'created: {self.created}'    
        return obj_repr

# define Task class - heavily stripped back from in app memory version
class Task(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    status=db.Column(db.String(20), nullable=False)
    created=db.Column(db.DateTime, nullable=False)
    completed=db.Column(db.DateTime, nullable=True)
    description=db.Column(db.String(500), nullable=False)
    # implements foreign key constraint
    userid=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # allows task.user and user.tasks to be queried
    user=db.relationship('User',backref=db.backref('tasks',lazy=True))

    # returns code used to instantiate object
    def __repr__(self):

        obj_repr = f'id: {self.id},' \
                   f'status: {self.status},' \
                   f'created: {self.created},' \
                   f'userid: {self.userid},' \
                   f'description: {self.description}'
        
        if self.completed is None:
            obj_repr = obj_repr + f'completed: N/A'
        else:
            obj_repr = obj_repr + f'completed: {self.completed}'

        return obj_repr

@app.route("/tasklist")
@app.route("/")
def task_list():

    showAll = False

    if not request.args.get("showAll") == None:
        showAll = True

    if showAll == True:
        # get all tasks
        tasks = Task.query.all()
    else:
        # get all tasks that aren't done
        tasks = Task.query.filter(Task.status != 'Done')

    return render_template('task_list.html', title="Task List", tasks=tasks, showAll = showAll)

@app.route("/addtask", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":

        req = request.form

        #validate task and return error list
        feedback = validate_task(req)

        #if there are any errors...
        if len(feedback) != 0:
            # get the list of users again (whoops, would normally be cached I guess...)
            users = User.query.all()
            # and send back to the page
            return render_template('add_task.html', title="Save task",
                description=req["description"], feedback=feedback, users=users)
        #otherwise add a task and redirect
        addTask(req["user"], req["description"])

        return redirect('/tasklist')

    # add a list of users to the page to be for-looped so you can pick
    # who something is assigned to.
    users = User.query.all()

    return render_template('add_task.html', title="Add task", users=users)

#I DID end up putting adduser in after all.
@app.route("/adduser", methods=["GET", "POST"])
def add_user():

    if request.method == "POST":

        req = request.form

        feedback = validate_user(req)

        if len(feedback) != 0:
            return render_template('add_user.html', title="Save user",
                firstName=req["firstName"], lastName=["lastName"],
                feedback=feedback)
        
        addUser(req["firstName"], req["lastName"], req["pin"])

        return redirect('/tasklist')

    return render_template('add_user.html', title="Add user")

@app.route("/completetask")
def complete_task():

    id = int(request.args.get('id'))

    completeTask(id)
    
    return redirect('/tasklist')

def validate_task(req):

    feedback = list()

    # would've looped through these but they all needed slightly different validation
    if req["description"] == "":
        feedback.append("Enter a description")

    # added this as now we're talking about a database...
    if len(req["description"]) > 500:
        feedback.append("Very clever, you got past the JavaScript")

    # like this cheeky chap, it seems if select boxes are left unselected, it just doesn't send on the form!
    if not "user" in req:
        feedback.append("Pick a user")
        return feedback

    user = None

    if req["user"] == "" or not req["user"].isdecimal():
        feedback.append("Choose a user and enter the corresponding PIN")
    else:
        user = User.query.get(req["user"])
    
    if user is None: 
        feedback.append("Stop mucking about with the DOM")
        return feedback

    if req["pin"] != user.pin:
        feedback.append("PIN is incorrect")    

    return feedback

def validate_user(req):

    feedback = list()

    if req["firstName"] == "" or len(req["firstName"]) > 100:
        feedback.append("Enter a first name between 1-100 characters")

    if req["lastName"] == "" or len(req["lastName"]) > 100:
        feedback.append("Enter a last name between 1-100 characters")

    if len(req["pin"]) != 4 or not req["pin"].isdecimal():
        feedback.append("Enter a 4-digit pin (0-9 only)")

    return feedback

def addUser(firstName, lastName, pin):

    newUser = User(firstName=firstName, lastName=lastName,
        pin=pin, created=datetime.now())

    db.session.add(newUser)
    db.session.commit()

def addTask(userid, description):

    newTask = Task(status="To Do", created=datetime.now(), 
        completed=None, userid = userid, description=description)

    db.session.add(newTask)
    db.session.commit()

def completeTask(id):

    task = Task.query.get(id)

    # if the task hasn't already been marked as completed...
    if task.status != "Done":
        # ...mark it as completed...
        task.status = "Done"
        # ...and set the completed time to now...
        task.completed = datetime.now()
        db.session.commit()

# if the schema hasn't been created, create it
db.create_all()

# get the user count on startup
users = User.query.all()

# if there are no users in the system, put the usual couple in
if len(users) == 0:
    regularUser = User(firstName = "Regular", lastName = "User", pin = 1234, created = datetime.now())
    adminUser = User(firstName = "Admin", lastName = "User", pin = 4246, created = datetime.now())

    db.session.add(regularUser)
    db.session.add(adminUser)
    db.session.commit()

app.run()