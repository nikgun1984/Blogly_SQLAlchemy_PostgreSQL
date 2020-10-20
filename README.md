# Blogly_SQLAlchemy_PostgreSQL

Simple blogging Flask App with SQLAlchemy/PostgreSQL and some Bootstrap for frontend  
Relationships that are used in the app:
* Many-to-Many
* One-to-Many   

Tables:
* users
* posts
* tags
* posts_tags(join table for many-to-many)

Note:
You would probably need to add the following add-ons to your settings in your virtual environment:  
"python.pythonPath": "/Library/Frameworks/Python.framework/Versions/3.9/bin/python3",  
    "python.linting.pylintArgs": ["--load-plugins", "pylint-flask"],  
    "code-runner.executorMap": {  
        "python": "python3 -u",  
    }  
Otherwise, you might encounter some issues to run this.
