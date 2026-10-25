from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visit_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Visit {self.id} {self.ip_address} {self.visit_time}>"