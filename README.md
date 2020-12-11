# Portfolio Task 2020-11-27 (Week 8)

Learning exercise for CETM65

## Task List V1.3

### Description

Learning exercise for CETM65

### Usage

Install requirements using:

` pip install -r requirements.txt `

If you like, you can have the application create a fresh database - just delete the existing DB and it'll be recreated when you run the application (along with the customary test users)

Run the flask application using:

` python app.py `

Visit http://127.0.0.1:5000/ (or your similarly configured localhost address)

This works very much like the previous task list, but now with a front end!

From the home screen, you can:

- Add a task: click Add task
- Add a user: click Add user
- Flip between views: click Show All to show all tasks, and Show Active to show active tasks
- Complete a task: click Mark as done

When you're on the add task page:

Enter:

- A description
- Which user is making the task
- Enter the pin (1234 for regular, 4246 for admin, or one you've defined)
- Click Save task

When you're on the add user page:

Enter:

- A first name
- A last name
- A memorable pin (this is the last time you'll see it short of querying directly through SQLite!)

Or click Cancel on either form to go back to the home screen.

If there's an issue, the app will tell you what to do to fix it.