from flask import Flask, session, redirect, render_template, request
import recog_user as reco
import record as add
import os
import random
from flask import Flask
import sqlite3
import datetime

con = sqlite3.connect('database1.db')
current_time = datetime.datetime.now()
date = str(current_time.day) + '-'+ str(current_time.month) + '-' + str(current_time.year)
time = str(current_time.hour) + '-'+ str(current_time.minute)
print(date)
print(time)

app = Flask(__name__)
app.secret_key =os.urandom(24)
t = None

@app.route("/")
# this route is redering homepage
def index():

#    if os.path.exists("output.wav"):
#         os.remove("output.wav")
   t = random.randint(1000,9999)
   session['t'] = t
   if 'identity' in session:
       return redirect('/dashboard')
   else:
        return render_template("Login.html",t=t)

@app.route('/location',methods=['POST', 'GET'])
def location():
     if request.method == 'POST':
         lon = request.form.get('long')
         lat = request.form.get('lat')
         session['lattitude'] =  lat
         session['longitude'] =  lon
         print(session.get('lattitude'))
         print(session.get('longitude'))
         print("________lattitude is_________")
         print(session.get('lattitude'))
         print("________longitude is_________")
         print(session.get('longitude'))
         return ('', 204)
@app.route('/readme')
def readme():
    return render_template('about.html')
@app.route('/login')
def hello():
    print("actual t is")
    print(session.get('t'))
    var2 = session.get('t')
    print(var2)
    session.pop('identity', None)
    session.pop('recognized', None)
    var = reco.recog_user(var2)
    print("-------printing var")
    print(var)
    print("-------------var2")
    print(var2)
    if var2 == "Stranger":
        return render_template("strenger.html")
    else:
        session['recognized']=var2
        session['identity'] = var
        print("---------printing identity")
        print(session.get('identity'))
        con = sqlite3.connect('database1.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (var,))
        dat4 = cur.fetchall() 
        cur.close()
        if (dat4[0][10]==session.get('longitude')) and (dat4[0][11]==session.get('lattitude')):
            con = sqlite3.connect('database1.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM attendence WHERE email=? AND date=?", (session.get('identity'),date))
            dat2 = cur.fetchall() 
            cur.close()
            if len(dat2)>0:
                return render_template('alr.html') 
            else:
                con = sqlite3.connect('database1.db')
                cur = con.cursor()
                cur.execute("INSERT INTO attendence (email,date,time,status)VALUES (?,?,?,?)",(var,date,time,'P') )
                con.commit()
                print("valid location")
                print(dat4[0][10])
                print(session.get('longitude'))
                return render_template('alr.html')
        else:
            print('invalid location')
            return render_template("inloc.html")     
        
        
        
        
        
        
    
@app.route("/dashboard")
def dashboard():
    if 'recognized' in session:
        email = session.get('identity')
        # name = session.get('recognized')
        con = sqlite3.connect('database1.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        dat1 = cur.fetchall()
        name = str(dat1[0][0])+ " "+ str(dat1[0][1])
        mobile = dat1[0][2]
        dob = dat1[0][5]
        address = dat1[0][6]   
        state = dat1[0][8] 
        city = dat1[0][9] 
        pincode = dat1[0][7]
        longitude  = dat1[0][10]
        lattitude = dat1[0][11]
        
        con = sqlite3.connect('database1.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM attendence WHERE email=?", (email,))
        dat3 = cur.fetchall()
        present = len(dat3)
        return render_template('dashboard.html',name  =name,email=email,mobile=mobile,dob=dob,address=address,state=state,city=city,pincode=pincode,longitude=longitude,lattitude=lattitude,present=present)
    
    else:
        return render_template('empty.html')
@app.route('/userlogout')
def userlogout():
    session.pop('identity', None)
    session.pop('recognized', None)
    return redirect('/')

@app.route("/record", methods=['POST', 'GET'])
def record():
    
    if request.method == "POST":
        f = request.files['audio_data']
        with open('output.wav', 'wb') as audio:  
            f.save(audio)
            print('file uploaded successfully')
            print("actual t is")
            print(session.get('t'))
            return redirect("/login")
            # var = reco.recog_user(session.get('t'))

        return redirect("/")
    else:
        return "case b"

@app.route('/model')
def model():
    nn =  session.get('femail')
    add.adduser(nn)
    return render_template("fmodel.html")

@app.route('/admin')
def admin():
    if 'adminusername' in session:
       return redirect('/adminpanel')
    else:
       error = ""
       return render_template('admin.html',error=error)
        
    

@app.route('/adminlogin',methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        adminusername = request.form.get('admin-username')
        adminpassword = request.form.get("admin-password")
        # if adminusername == 'admin' and adminpassword == 'admin':
        if adminusername == 'admin':
            if adminpassword == 'admin':
                session['adminusername'] = adminusername
                return redirect('/adminpanel')
                
            
        else:
            pass
    error = "Wrong Credentials"
    return render_template('admin.html',error=error)

@app.route('/adminpanel')
def adminpanel():
    if 'adminusername' in session:
       msg = ""
       return render_template("adminpanel.html",msg=msg)
    else:
       return redirect('/admin')


@app.route('/addemp',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       firstname = request.form.get('register-firstname')
       lastname = request.form.get('register-lastname')
       phone = request.form.get('register-phone')
       email = request.form.get('register-email')
       password = request.form.get('register-password')
       dob = request.form.get('register-dob')
       address = request.form.get('register-address')
       pincode = request.form.get('register-pincode')
       city = request.form.get('register-city')
       state = request.form.get('register-state')
       longitudes = request.form.get('register-longitude')
       lattitudes = request.form.get('register-lattitude')
       con = sqlite3.connect('database1.db')
       cur = con.cursor()
       cur.execute("INSERT INTO users (firstname,lastname,phone,email,password,dob,address,pincode,city,state,       longitude,lattitude)VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(firstname,lastname,phone,email,password,dob,address,pincode,city,state,longitudes,lattitudes) )
       con.commit()
       msg = "Record successfully added"
       return render_template("adminpanel.html",msg = msg)
       con.close()

@app.route('/register')
def register():
    t1 = random.randint(1000,9999)
    t2 = random.randint(1000,9999)
    t3 = random.randint(1000,9999)
    return render_template('register.html',t1=t1,t2=t2,t3=t3)      

@app.route('/first',methods=['GET', 'POST'])
def first():
    if request.method == 'POST':
        femail = request.form.get('first-email')
        fpassword = request.form.get("first-password")
        session['femail'] = femail
        session['fpassword'] = fpassword
        con = sqlite3.connect('database1.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (femail,fpassword))
        ress = cur.fetchall()
        session['user']=ress
        cur.close()
        if len(ress)>0:
            path1 = 'gmm_models/' + femail + '.gmm'
            if os.path.isfile(path1):
                return render_template("falready.html")  
            else:
                return ('', 204)
        else:
            return render_template("fwrong.html")
                 
@app.route('/adminlogout')
def adminlogout():
    session.pop('adminusername', None)  
    error = "Logged out Successfully !!!"
    return render_template('admin.html',error=error)   


@app.route("/rec1", methods=['POST', 'GET'])
# this route records first voice sample in registration and return ('', 204) means it will not bredirect to another npage or template
def rec1():
    
    if request.method == "POST":
         emp_var = session.get('femail')
         pathfolder  ='voice_database/'+str(emp_var)
         os.mkdir(pathfolder)
         vv = pathfolder + "/1.wav"

         r1 = request.files['audio_data']
         with open(vv, 'wb') as audio:  
            # emp-var = session.get('emp-id')
            # emp-var1 = str(emp-var)
            r1.save(audio)
            print('file uploaded successfully')

         return ('', 204)
    else:
         return ('', 204)
     
@app.route("/rec2", methods=['POST', 'GET'])
# this route records second voice sample in registration
def rec2():
    
    if request.method == "POST":
        emp_var2 = session.get('femail')
        pathfolder2  ='voice_database/'+str(emp_var2)
        vv2 = pathfolder2 + "/2.wav"
        r2 = request.files['audio_data']
        with open(vv2, 'wb') as audio:  
            r2.save(audio)
            print('file uploaded successfully')

        return ('', 204)
    else:
        return ('', 204)
    
@app.route("/rec3", methods=['POST', 'GET'])
# this route records third voice sample in registration
def rec3():
    
    if request.method == "POST":
        emp_var3 = session.get('femail')
        pathfolder3  ='voice_database/'+str(emp_var3)

        vv3 = pathfolder3 + "/3.wav"

        r3 = request.files['audio_data']
        with open(vv3, 'wb') as audio:  
            r3.save(audio)
            print('file uploaded successfully')
            

        return ('', 204)
    else:
        return ('', 204)

    

if __name__ == "__main__":
    app.run(debug=True)