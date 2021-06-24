from flask import render_template,request,redirect,url_for,abort
from flask_wtf import form
from . import main
from flask_login import login_required,current_user,login_user,logout_user
from .forms import UpdateProfile,BusinessForm,ReviewForm, SearchForm,LocationSearchForm
from .. import db,photos
from ..models import User,Business,Review
from app import models

#views
@main.route('/')
def index():
    search_bs = request.args.get("location")
    search_service = request.args.get("service")
    businessOnLocation = Business.query.filter_by(location=search_bs).all()
    businessByService = Business.query.filter_by(service=search_service).all()


    return render_template('index.html',businessOnLocation=businessOnLocation,businessByService=businessByService)

@main.route('/all')
def all():
    all_business = Business.query.filter_by().all()
    return render_template('all.html',all_business=all_business)


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
        return redirect(url_for('main.all'))
    return render_template('upload_business.html',form=form,title='Add Business',legend='Add Business')
    
    
@main.route('/search', methods=['GET', 'POST'])
def search():
    searchform = SearchForm()
    if searchform.validate_on_submit():
        selectedservice = searchform.service.data
        businessByService = Business.query.filter_by(service=selectedservice).all()
        return render_template('results.html',businessByService=businessByService)
    return render_template('search.html',searchform=searchform,title='Search',legend='Add Business')



@main.route('/location',methods=['GET', 'POST'])
def location():
    search_bs = request.args.get("location") 
    businessOnLocation = Business.query.filter_by(location=search_bs).all()
    return render_template('results.html',businessOnLocation=businessOnLocation)


# @main.route('/location',methods=['GET', 'POST'])
# def location():
#     locationform = LocationSearchForm()
#     if locationform.validate_on_submit():
#         selectedlocation = locationform.location.data
#         businessOnLocation = Business.query.filter_by(location=selectedlocation).all()
#         return render_template('results.html',businessOnLocation=businessOnLocation)
#     return render_template('location.html',locationform=locationform,title='Search',legend='Add Business')


# locationform = LocationSearchForm()
#     if locationform.validate_on_submit():
#         businesses = Business.query.filter_by().all()
#         for business in businesses:
#             if business.location == locationform.location.data:
#                 return redirect(url_for('main.index',business=business))
#     return render_template('search.html',locationform=locationform,title='Search',legend='Add Business')

@main.route("/review/<int:business_id>",methods=["POST","GET"])
@login_required
def reviews(business_id):
    form = ReviewForm()
    business = Business.query.get(business_id)
    all_reviews = Review.get_reviews(business_id)
    if form.validate_on_submit():
        new_review = form.review.data
        business_id = business_id
        user_id = current_user._get_current_object().id
        review_object = Review(review=new_review,user_id=user_id,business_id=business_id)
        review_object.save_review()
    return render_template("reviews.html",review_form = form,all_reviews = all_reviews,business = business)