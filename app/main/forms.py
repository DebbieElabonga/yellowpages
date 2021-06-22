from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import Required,Email,EqualTo,DataRequired

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class BusinessForm(FlaskForm):
    businessname = TextAreaField('Enter Business Name',validators = [Required()])
    contact = TextAreaField('Enter Number',validators = [Required()])
    service = TextAreaField('Tell us about your business',validators = [Required()])
    location = SelectField('Select Location',validators=[DataRequired()],choices=[('Nairobi','Nairobi'),('Kiambu','Kiambu'),('Mombasa','Mombasa'),('Makueni','Makueni'),('Nyandarua','Nyandarua'),('Vihiga','Vihiga')])
    website = TextAreaField('Enter your business Website')
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    review = TextAreaField('Enter your review here..',validators = [Required()])
    submit = SubmitField('Submit')

    

