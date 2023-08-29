from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    project_title = db.Column(db.String(255), unique=True, nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_category = db.Column(db.String(255), nullable=False)
    project_target = db.Column(db.Float, nullable=False)
    minimum_buy_in = db.Column(db.Float, nullable=False)
    roi = db.Column(db.Float, nullable=False)
    stake_amount = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    total_contributors = db.Column(db.Integer, default=0)
    total_contribution = db.Column(db.Float, default=0.0)
    # Add constraints to enforce non-nullability and uniqueness

class Contributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contributor_address = db.Column(db.String(255), nullable=False)
    project_title = db.Column(db.String(255), nullable=False)
    contribution = db.Column(db.Float, nullable=False)
    project = db.relationship('Project', backref=db.backref('contributors', lazy=True))

    def __init__(self, contributor_address, project_title, contribution):
        self.contributor_address = contributor_address
        self.project_title = project_title
        self.contribution = contribution

    def save(self):
        db.session.add(self)
        db.session.commit()