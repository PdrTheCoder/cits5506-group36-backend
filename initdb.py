from main import app
from model import db


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
