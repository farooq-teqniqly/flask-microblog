from app import app, db
import uuid
from app.models import User, Post

if __name__ == "__main__":
    app.run()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post, uuid=uuid)
