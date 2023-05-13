import pickle
from flask import Flask,flash, render_template, request, url_for, session, redirect
from flask_mysqldb import MySQL
import numpy as np
import urllib.request
import pymysql
import re
import os
import tensorflow as tf
from keras.models import load_model
from werkzeug.utils import secure_filename

from keras.utils import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key="124$89afd#*%42*(23("

mysql=MySQL()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456789'
app.config['MYSQL_DB']='distracteddriverdetection'
mysql.init_app(app)

class_names = ['Safe driving',
              'Texting - right',
              'Talking on the phone - right',
              'Texting - left',
              'Talking on the phone - left',
              'Operating the radio',
              'Drinking',
              'Reaching behind',
              'Hair and makeup',
              'Talking to passenger']


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/drivingmode')
def drivingmode():
    if 'loggedin' not in session:
        return redirect(url_for('home'))
    return render_template('drivingmode.html')

@app.route('/profile')
def profile():
    if 'loggedin' not in session:
       return redirect(url_for('home'))
    username=session['username']
    cursor=mysql.connection.cursor()
    cursor.execute("select * from userdata where username=%s ",(username,))
    data=cursor.fetchall()
    return render_template("profile.html",data=data)

@app.route('/editprofile',methods=["GET","POST"])
def editprofile():
    if 'loggedin' not in session:
        return redirect(url_for('home'))
    if request.method=='POST':
        print("POST")
        cursor=mysql.connection.cursor()
        msg=''
        age=request.form['age']
        licenseNumber=request.form['licenseNumber']
        gender=request.form['gender']
        vehicleNumber=request.form['vehicleNumber']
        vehicleType=request.form['vehicleType']
        vehicleName=request.form['vehicleName']
        company=request.form['company']
        buydate=request.form['buyDate']

        cursor.execute("select * from userdata where username=%s",(session['username'],))
        data=cursor.fetchone()
        if data:
            cursor.execute("delete from userdata where username=%s",(session['username'],))
            mysql.connection.commit()
        cursor.execute('insert into userdata(username,fullname,age,licenseNumber,gender,vehicleNumber,VehicleType,vehicleName,ManufacturingCompany,BuyDate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(session['username'],session['name'],age,licenseNumber,gender,vehicleNumber,vehicleType,vehicleName,company,buydate))
        mysql.connection.commit()
        msg='Data Updated Successfully !!'
        print(msg)
        return render_template('editprofile.html',msg=msg)
    
    return render_template('editprofile.html')



@app.route('/login',methods=["GET","POST"])
def login():
    cursor=mysql.connection.cursor()
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']

        cursor.execute('select * from accounts where username=%s and password=%s',(username,password))
        account=cursor.fetchone()
        #print(account)
        if account:
            session['loggedin']=True
            session['name']=account[2] + " " +  account[3]
            session['id']=account[0]
            session['username']=username

            cursor.execute("select * from userdata where username=%s ",(username,))
            data=cursor.fetchall()

            return render_template('profile.html',data=data)
        else:
            msg='Invalid Credentials'

    return render_template("login.html")

@app.route('/register',methods=["GET","POST"])
def register():
    cursor=mysql.connection.cursor()
    msg=''
    if request.method=='POST' and 'username' in request.form and 'fname' in request.form and 'lname' in request.form and 'email' in request.form and 'password' in request.form and 'confirmPass' in request.form:
        if(request.form['password']!=request.form['confirmPass']):
            msg="Password doesn't Match"
            return url_for(register)
        
        username=request.form['username']
        firstname=request.form['fname']
        lastname=request.form['lname']
        email=request.form['email']
        password=request.form['password']

        cursor.execute('select firstname from accounts where username=%(username)s',{'username':username})

        account=cursor.fetchone()

        if account:
            msg='user already exists'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='username not valid'
        else:
            cursor.execute('insert into accounts(username,firstname,lastname,email,password) values(%s,%s,%s,%s,%s)',(username,firstname,lastname,email,password))
            mysql.connection.commit()
            return redirect(url_for('home'))
            
        
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    session.pop('firstname',None)
    return redirect(url_for('login'))


#Prediction Using Deep Learning Model

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




def predict_util(filename):
    model = load_model('static\models\model3.h5')

    my_image = load_img(f'static/uploads/{filename}', target_size=(128, 128))

#preprocess the image
    my_image = img_to_array(my_image)

#make the prediction
    prediction = model.predict(np.array([my_image]))

    res=np.argmax(prediction)
    result=class_names[res]

    return result

@app.route('/predict',methods=["GET","POST"])
def predict():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('drivingmode'))
    file=request.files['file']
    if file.filename=='':
            flash('no file uploaded')
            return redirect(url_for('drivingmode'))
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        res=predict_util(filename)

        return render_template('drivingmode.html',filename=file.filename,res=res)
    else:
        flash("Only images selection is allowed !!")
        return redirect(url_for('drivingmode'))


if __name__ == '__main__':
    app.run()

