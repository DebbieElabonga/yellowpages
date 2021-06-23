from flask import render_template,request,redirect,url_for,abort
from flask_wtf import form
from . import main
from flask_login import login_required,current_user,login_user,logout_user
from .forms import UpdateProfile,BusinessForm,ReviewForm, SearchForm
from .. import db,photos
from ..models import User,Business,Review
from app import models

#views
@main.route('/')
def index():
    all_business = Business.query.filter_by().all()
    return render_template('index.html',all_business=all_business)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname)) 


@main.route('/user/<uname>/business',methods= ['POST','GET'])
@login_required
def upload_business(uname):
    user = User.query.filter_by(username = uname).first()
    form = BusinessForm()
    if user is None:
        abort(404)

    if form.validate_on_submit():
        businessname = form.businessname.data
        contact = form.contact.data
        service = form.service.data
        location= form.location.data
        website = form.website.data
        user_id = current_user.id

        
        business = Business(businessname=businessname,contact=contact,service=service,location=location,website=website,user_id=user_id)
        business.save_business()
        return redirect(url_for('main.index'))
    return render_template('upload_business.html',form=form,title='Add Business',legend='Add Business')

# @main.route('/search', methods=['GET', 'POST'])
# def search():
#     cur =db.cursor()
#     if request.method == "POST":
#         Business = BusinessForm.form['business']
#         # search by businessname or name
#         cur.execute("SELECT businessname, service from Business WHERE businessname 
#                         LIKE %s OR service LIKE %s", (business, business))
#         conn.commit()
#         data = cursor.fetchall()
#         # all in the search box will return all the tuples
#         if len(data) == 0 and Business == 'all': 
#             cursor.execute("SELECT businessname, service from Business")
#             conn.commit()
#             data = cursor.fetchall()
#         return render_template('search.html', data=data)
#     return render_template('search.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    searchForm = SearchForm()
    business = models.Business.query

    if searchForm.validate_on_submit():
        businesses = business.filter(models.Business.service.like('%' + searchForm.service.data + '%'))

        business = business.order_by(models.Business.businessname).all()

        return redirect(url_for('main.index'))
    return render_template('search.html', business = business, form= searchForm)
    
    