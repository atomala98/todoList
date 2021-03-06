from app import app, db
from app.models import User, Task, Message, Group

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, "Task": Task, "Message": Message, "Group": Group}