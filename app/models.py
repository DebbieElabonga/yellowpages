from . import db
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True,index=True)
    bio = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    pass_secure  = db.Column(db.String(255))
    business = db.relationship("Business",backref="user",lazy="dynamic")
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
       return f'User {self.username}'

class Business(db.Model):
    __tablename__="business"
    id = db.Column(db.Integer,primary_key=True)
    businessname = db.Column(db.String(255))
    contact = db.Column(db.Integer)
    service = db.Column(db.String(255))
    location = db.Column(db.String(255))
    website = db.Column(db.String(255))
    review = db.relationship("Review",backref="business",lazy="dynamic")
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


    def save_business(self):
        db.session.add(self)
        db.session.commit()
    def delete_business(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_business(cls,user_id):
        businesses = Business.query.filter_by(user_id=user_id).all()
        return Business

    def __repr__(self):
       return f'Business {self.businessname}'



class Review(db.Model):
    __tablename__="review"
    id = db.Column(db.Integer,primary_key=True)
    review = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    business_id = db.Column(db.Integer,db.ForeignKey("business.id"))


    def save_review(self):
        db.session.add(self)
        db.session.commit()
    def delete_review(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,business_id):
        reviews = Review.query.filter_by(business_id=business_id).all()
        return reviews




