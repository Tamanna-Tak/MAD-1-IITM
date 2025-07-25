from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.sqlite3"


db=SQLAlchemy(app)
app.app_context().push()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addlogin')
def addlogin():
    return render_template('admin_login.html')

@app.route('/userlogin')
def userlogin():
    return render_template('user_login.html')

@app.route('/register')
def register():
    return render_template('user_register.html')

@app.route('/admindash')
def admindash():
    return render_template('admin_dashboard.html')
@app.route('/userdash')
def userdash():
    return render_template('user_dashboard.html')

@app.route('/searching')
def searching():
    return render_template('searching_page.html')

@app.route('/logout')
def logout():
    return render_template('admin_login.html')

@app.route('/showsearch')
def showsearch():
    return render_template('search_a_show.html')

@app.route('/venuesearch')
def venuesearch():
    return render_template('search_a_venue.html')

@app.route('/venueplace')
def venueplace():
    return render_template('search_a_venue_place.html')

@app.route('/showrating')
def showratingsearch():
    return render_template('search_show_rating.html')

@app.route('/showtag')
def showtagsearch():
    return render_template('search_show_tag.html')


##################################################
#create venue database

class Venue(db.Model):
    venue_id=db.Column(db.Integer,primary_key=True)
    venue_name=db.Column(db.String,nullable=False)
    venue_place=db.Column(db.String)
    venue_capacity=db.Column(db.Integer)
    members=db.relationship("Show",backref="venue",secondary="association")
    

class Show(db.Model):
  show_id=db.Column(db.Integer,primary_key=True)
  show_name=db.Column(db.String,nullable=False)
  show_rating=db.Column(db.Integer)
  show_tag=db.Column(db.String)
  show_price=db.Column(db.Integer)


class Association(db.Model):
  #both the column act as (compound)primary key
  venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"),primary_key=True)
  show_id=db.Column(db.Integer,db.ForeignKey("show.show_id"),primary_key=True)
class User(db.Model):
   user_id=db.Column(db.Integer,primary_key=True)
   user_name=db.Column(db.String,nullable=False)
   user_password=db.Column(db.String,nullable=False)
 
class Admin(db.Model):
   admin_id=db.Column(db.Integer,primary_key=True)
   admin_name=db.Column(db.String,nullable=False)
   admin_password=db.Column(db.String,nullable=False)

class Booking(db.Model):
  user_name=db.Column(db.String,primary_key=True)
  venue_id=db.Column(db.Integer,nullable=False)
  show_id=db.Column(db.Integer,nullable=False)
  no_of_tickets=db.Column(db.Integer,nullable=False)

  

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method=='POST':
       a_name=request.form['a_name']
       a_pass=request.form['a_pass']
       a=Admin.query.filter_by(admin_name=a_name,admin_password=a_pass).first()
       if not a :
            error="invalid username/password"
            return render_template('admin_login.html',error=error)
    #    new=Admin(admin_name=a_name,admin_password=a_pass)
    #    db.session.add(new)
    #    db.session.commit()
    return render_template('admin_dashboard.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
       u_name=request.form['u_name']
       u_pass=request.form['u_pass']
       u=User.query.filter_by(user_name=u_name,user_password=u_pass).first()
       if not u :
            error="invalid username/password"
            return render_template('user_login.html',error=error)
    #    new=User(user_name=u_name,user_password=u_pass)
    #    db.session.add(new)
    #    db.session.commit()
    return render_template('user_dashboard.html')
    
@app.route("/user_register",methods=['POST','GET'])
def user_register():
   if request.method=='POST':
       u_name=request.form['u_name']
       u_pass=request.form['u_pass']
       new=User(user_name=u_name,user_password=u_pass)
       db.session.add(new)
       db.session.commit()
   return render_template('user_login.html')   

@app.route("/venue/create",methods=['POST','GET'])
def create_venue():
  if request.method=='POST':
   # v_id=request.form['v_id']#we can also use .get method but here we use .form as we are sure that user must enter c_name(as it is a required field)
    v_name=request.form['v_name']
    v_place=request.form['v_place']
    v_capacity=request.form['v_capacity']

##creating instance
    ven=Venue(
    
      venue_name=v_name,
      venue_place=v_place,
      venue_capacity=v_capacity
    )
##adding instance to session
    db.session.add(ven)
    db.session.commit()
    
    return redirect('/admindash')
  return render_template("create_venue.html")


@app.route("/show/create",methods=['POST','GET'])
def create_show():
  if request.method=='POST':
      s_name=request.form['s_name']#we can also use .get method but here we use .form as we are sure that user must enter c_name(as it is a required field)
      s_rating=request.form['s_rating']
      s_tag=request.form['s_tag']
      s_price=request.form['s_price'] 
      v_id=request.form['v_id']

      #creating instance
      emp=Show(
        show_name=s_name,
        show_rating=s_rating,
        show_tag=s_tag,
        show_price=s_price


      )
      vie=Venue.query.get(v_id)
      #adding instance to session
    
      db.session.add(emp)
      emp.venue.append(vie)
      db.session.commit()
      
      return redirect('/admindash')
  coms=Venue.query.all()#give list of available companies
  return render_template("create_show.html",coms=coms)


@app.route('/venue/list')
def view_list():
  all=Venue.query.all() #fetch all records from the company table
  return render_template('view_venue.html',all=all)

@app.route('/user_venue/list')
def user_view_list():
  all=Venue.query.all() #fetch all records from the company table
  return render_template('user_venue_list.html',all=all)


@app.route('/show/list')
def show_list():
  all=Show.query.all() #fetch all records from the company table
  return render_template('view_show.html',all=all)

@app.route('/user_venue/<int:venue_id>')#expecting a variable company_id of type int # type: ignore
def view_user_venue(venue_id):
    ven=Venue.query.get(venue_id)
    show_list=ven.members
    return render_template('user_venue_detail.html',ven=ven,show_list=show_list)

@app.route('/venue/<int:venue_id>')#expecting a variable company_id of type int # type: ignore
def view_venue(venue_id):
    ven=Venue.query.get(venue_id)
    show_list=ven.members
    return render_template('venue_details.html',ven=ven,show_list=show_list)

@app.route('/show/<int:show_id>')#expecting a variable company_id of type int # type: ignore
def view_show(show_id):
    sh=Show.query.get(show_id)
    venue_list=sh.venue
    return render_template('show_details.html',sh=sh,venue_list=venue_list)

@app.route("/show/<int:show_id>/update",methods=['POST','GET'])
def update_show(show_id):
  if request.method=='POST':
      s_name=request.form['s_name']#we can also use .get method but here we use .form as we are sure that user must enter c_name(as it is a required field)
      s_rating=request.form['s_rating']
      s_tag=request.form['s_tag']
      s_price=request.form['s_price']

      v_id=request.form['v_id'] #from select tag

      #update instance
      show=Show.query.get(show_id)
      show.show_name=s_name
      show.show_rating=s_rating
      show.show_tag=s_tag
      show.show_price=s_price

      ven=Venue.query.get(v_id)
    
      show.venue.append(ven)
      db.session.commit()
      
      return redirect('/admindash')
  venu=Venue.query.all()#give list of available companies
  shows=Show.query.get(show_id)#pass employee object
  return render_template("update_show.html",venu=venu,shows=shows)

@app.route("/venue/<int:venue_id>/update",methods=['POST','GET'])
def update_venue(venue_id):
  if request.method=='POST':
      v_name=request.form['v_name']#we can also use .get method but here we use .form as we are sure that user must enter c_name(as it is a required field)
      v_place=request.form['v_place']
      v_capacity=request.form['v_capacity']

      s_id=request.form['s_id'] #from select tag

      #update instance
      venue=Venue.query.get(venue_id)
      venue.venue_name=v_name
      venue.venue_place=v_place
      venue.venue_capacity=v_capacity

      sh=Show.query.get(s_id)
      #adding instance to session
    
      venue.members.append(sh)
      db.session.commit()
      
      return redirect('/admindash')
  ssh=Show.query.all()#give list of available companies
  ven=Venue.query.get(venue_id)#pass employee object
  return render_template("update_venue.html",ven=ven,ssh=ssh)



@app.route("/show/<int:show_id>/venue/<int:venue_id>")#expecting a variable company_id of type int # type: ignore
def delink(show_id,venue_id):
    shows=Show.query.get(show_id)
    venu=Venue.query.get(venue_id)
    shows.venue.remove(venu)
    #print(emp.company)
    db.session.commit()
    return redirect("/venue/"+str(venue_id))

@app.route("/user/show/<int:show_id>/venue/<int:venue_id>",methods=['POST','GET'])
def create_booking(show_id,venue_id):
     
  if request.method=='POST':
    #  v_id=request.form['v_id']
    #  s_id=request.form['s_id']
     n_tic=request.form['n_tic']
     u_name=request.form['u_name']#we can also use .get method but here we use .form as we are sure that user must enter c_name(as it is a required field)
    
      #creating instance
     emp=Booking(
      venue_id=venue_id,
      show_id=show_id,
      no_of_tickets=n_tic,
      user_name=u_name)
     
     db.session.add(emp)
    #  db.session.commit()
     
     ven=Venue.query.get(venue_id)
     ven.venue_capacity-=int(n_tic)
    #  db.session.commit()
     show=Show.query.get(show_id)
     
     show.venue.append(ven)
     db.session.commit()
      #adding instance to session
   
      
     return redirect('/userdash')
  venu=Venue.query.get(venue_id)#give list of available companies
  shows=Show.query.get(show_id)#pass employee object
  
  return render_template("booking_form.html",venu=venu,shows=shows)


 
@app.route("/show_search" , methods=['POST'])
def show_search():
    if request.method=='POST':
       show_name=request.form.get('show_name')
       show_list=Show.query.filter_by(show_name=show_name).all()
  
       return render_template('show_search.html',show_list=show_list)
    else:
        return " " 
     
@app.route("/show_rating_search" , methods=['POST'])
def show_rating_search():
    if request.method=='POST':
       show_rating=request.form.get('show_rating')
       show_list=Show.query.filter_by(show_rating=show_rating).all()
  
       return render_template('show_rating_search.html',show_list=show_list)
    else:
        return " "
    
@app.route("/show_tag_search" , methods=['POST'])
def show_tag_search():
    if request.method=='POST':
       show_tag=request.form.get('show_tag')
       show_list=Show.query.filter_by(show_tag=show_tag).all()
  
       return render_template('show_tag_search.html',show_list=show_list)
    else:
        return " "

@app.route("/venue_search" , methods=['POST'])
def venue_search():
    if request.method=='POST':
       venue_name=request.form.get('venue_name')
       venue_list=Venue.query.filter_by(venue_name=venue_name).all()
  
       return render_template('venue_search.html',venue_list=venue_list)
    else:
         return " " 
     

@app.route("/venue_place_search" , methods=['POST'])
def venue_place_search():
    if request.method=='POST':
       venue_place=request.form.get('venue_place')
       venue_list=Venue.query.filter_by(venue_place=venue_place).all()
  
       return render_template('venue_place_search.html',venue_list=venue_list)
    else:
        return " " 
     


if __name__ == "__main__":
    app.run(debug=True)

