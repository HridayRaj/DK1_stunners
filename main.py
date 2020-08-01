''' importing all the libraries '''
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for
import random 
# import mysql.connector
import os
import speech_recognition as sr
import time
from IPython.display import Audio, display, clear_output
import wave
import pickle
from scipy.io.wavfile import  read
from sklearn.mixture import GaussianMixture as GMM
import warnings
warnings.filterwarnings("ignore")

from sklearn import preprocessing
 # for converting audio to mfcc
import python_speech_features as mfcc
import numpy as np
# importing database
import sqlite3


# conn = sqlite3.connect('flask_app.db')
# print ("Opened database successfully")

t = None
identity = None 


app = Flask(__name__)
app.secret_key =os.urandom(24)

# conn =mysql.connector.connect(host="sql12.freemysqlhosting.net", user="sql12350872",password="hS481P6gxf",database="sql12350872")
# conn =mysql.connector.connect(host="localhost", user="root",password="",database="flask_app")
# cursor = conn.cursor()


def calculate_delta(array):
    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows -1:
                second = rows -1
            else:
                second = i+j
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas



#convert audio to mfcc features
def extract_features(audio,rate):    
    mfcc_feat = mfcc.mfcc(audio,rate, 0.025, 0.01,20,appendEnergy = True, nfft=1103)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)

    #combining both mfcc features and delta
    combined = np.hstack((mfcc_feat,delta)) 
    return combined

def recog(audio):
    r=sr.Recognizer()
    print('Instantiated')
    #t1='hello'
    ''' not recording from microphone '''

    audiofile=sr.AudioFile(audio)

    with audiofile   as source:
       # print("Say something")
        #audio=recognizer.listen(source)
        audio=r.record(source)

    '''     recogizer   '''

    print("You Said")
    text=r.recognize_google(audio , language='en-US')
    print(text)
    return int(text)

#''' functio for calculating threshold 


def calc_thresh(scores,alpha):
    meu=np.mean(scores)
    sigma=np.std(scores)
    return meu -alpha*sigma


#''' 



@app.route("/")
# this route is redering homepage
def index():

   if os.path.exists("output.wav"):
        os.remove("output.wav")
   t = random.randint(1000,9999)
   if 'user_id' in session:
       return redirect('/dashboard')
   else:
        return render_template("Login.html",t=t)
   
# @app.route("/home")
# def home():
#     # if 'user_id' in session:
#     #     return render_template('home.html')

#     # else:
#         return render_template('menubar.html')

@app.route("/record", methods=['POST', 'GET'])
def record():
    #this route is recording audio for login purpose and saving as output.wav
    
    if request.method == "POST":
        f = request.files['audio_data']
        with open('output.wav', 'wb') as audio:  
            f.save(audio)
            print('file uploaded successfully')

        return redirect(url_for('re'))
    else:
        return redirect("/")

@app.route("/recognize")
def re():
    # the recognition for login starts here
    print("Recognizing")
    FILENAME = "./output.wav"
    if(t== recog(FILENAME)):
        print("*** Started Configuration ***")

    # Gmm model applied from here
    #threshold=-30
    modelpath = "./gmm_models/"

    gmm_files = [os.path.join(modelpath,fname) for fname in 
               os.listdir(modelpath) if fname.endswith('.gmm')]

    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
               in gmm_files]

    (sr,audio)=read(FILENAME)
    # extracting mfcc feaures

    vector=extract_features(audio,sr)
    threshold_list=[]
    log_likelihood=np.zeros(len(models))
    print(speakers)
    threshold = -27
    threshold_list.append(0)
    #checking with each model one by one
    for i in range(len(models)):
       gmm = models[i]   
      # print(f"score of model {i} is {gmm.score(vector)}")      
       scores = np.array(gmm.score(vector))
       print(f" scores are {scores}")
       #if (scores >=-28) :
       log_likelihood[i] = scores.sum()
       if(log_likelihood[i]>=threshold):
           threshold_list.append(1)
   # ''' threshold function caculated here '''
   # already calculated
    #get_threshold=calc_thresh(log_likelihood,0.25)
    #print(f"threshold value is {get_threshold}")
    #print(f"log likehood table is as follows : {log_likelihood}")
    sum_=sum(threshold_list)
    if(sum_==0):

        ''' here return a false or "unknown string " value '''
        print("You are Stranger ")
    else:
        pred = np.argmax(log_likelihood)
        print(f"pred value for this is : {pred}")
        identity = speakers[pred]
    
    # if voice not recognized than terminate the process
        if identity == 'unknown':
            print("Not Recognized! Try again...")
        else:  
            ''' here return the user from the from the function '''
            print(f"recognised as {identity}") 
    return redirect('/dashboard')

@app.route('/dashboard')
# this route is for dashboard but not in use and will be used in future
def dashboard():
   return render_template('menubar.html')
    

        
@app.route("/register")
def register():
    t1 = random.randint(1000,9999)
    t2 = random.randint(1000,9999)
    t3 = random.randint(1000,9999)
    return render_template("register.html",t1=t1,t2=t2,t3=t3)

@app.route('/readme')
def readme():
    return render_template('details.html')


# @app.route('/add_user',methods=['POST'])
# def add_user():
#     firstname = request.form.get('register-firstname')
#     lastname = request.form.get('register-lastname')
#     phone = request.form.get('register-phone')
#     email = request.form.get('register-email')
#     post = request.form.get('register-post')
#     dob = request.form.get('register-dob')
#     address = request.form.get('register-address')
#     landmark = request.form.get('register-landmark')
#     city = request.form.get('register-city')
#     state = request.form.get('register-state')
#     longitude = request.form.get('register-longitude')
#     lattitude = request.form.get('register-lattitude')
#     pin = request.form.get('register-pin')
#     # upload_image(request)


#     cursor.execute("""INSERT INTO `users` (`emp-id`,`firstname`,`lastname`,`phone`,`email`,`post`,`dob`,`address`,`landmark`,`city`,`state`,`longitude`,`lattitude`,`pin`) VALUES 
#     (NULL,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(firstname,lastname,phone,email,post,dob,address,landmark,city,state,longitude,lattitude,pin))
#     conn.commit()

#     # inside format provide employee id 
#     cursor.execute("""SELECT * FROM `users` WHERE `emp-id` LIKE '{}'""".format(email))
#     myuser=cursor.fetchall()
#     # session['emp-id']=myuser[0][0]
#     return redirect('/dashboard')


@app.route('/add_user',methods = ['POST', 'GET'])
#  this route gets data from register form and uploads it ton database when user clicks next for last step and redirects to last step that is recorf three voice sample
def addrec():
    # connecting database
   conn = sqlite3.connect('site1.db')
   cursor = conn.cursor()
   if request.method == 'POST':
    #    f1 = request.files['register-image']  
    #    f1.save(f.filename)  
    #    print('Image uploaded')

       firstname = request.form.get('register-firstname')
       lastname = request.form.get('register-lastname')
       phone = request.form.get('register-phone')
       email = request.form.get('register-email')
       post = request.form.get('register-post')
       dob = request.form.get('register-dob')
       address = request.form.get('register-address')
       landmark = request.form.get('register-landmark')
       city = request.form.get('register-city')
       state = request.form.get('register-state')
       longitude = request.form.get('register-longitude')
       lattitude = request.form.get('register-lattitude')
       pin = request.form.get('register-pin')
       red = "INSERT INTO users (firstname,lastname,phone,email,post,dob,address,landmark,city,state,longitude,lattitude,pin) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
       cursor.execute(red,(firstname, lastname, phone, email, post, dob, address, landmark, city, state, longitude, lattitude, pin)) 


       #Commit your changes in the database
       conn.commit()
       ex = ''' SELECT * FROM users WHERE phone LIKE ?'''
       cursor.execute(ex, (phone,))
       se = cursor.fetchall()
       session.clear()
       # this session is storing emo-id and will be access in another route for creating folder in voice_database
       session['emp-id']=se[0][0]
       #Closing the connection
       conn.close()
       return ('', 204)



           

# def upload_image(req):
#     if request.method == 'POST':  
#         img = request.files['register-image']  
#         img.save(img.filename)  
#         return 'nothing'


@app.route('/logout')
# this route removes stored session and user gets logout will be used in dashboard
def logout():
    session.pop('emp-id')
    return redirect ('/')




@app.route("/rec1", methods=['POST', 'GET'])
# this route records first voice sample in registration and return ('', 204) means it will not bredirect to another npage or template
def rec1():
    
    if request.method == "POST":
         emp_var = session.get('emp-id')
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
        emp_var2 = session.get('emp-id')
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
        emp_var3 = session.get('emp-id')
        pathfolder3  ='voice_database/'+str(emp_var3)

        vv3 = pathfolder3 + "/3.wav"

        r3 = request.files['audio_data']
        with open(vv3, 'wb') as audio:  
            r3.save(audio)
            print('file uploaded successfully')
            adduser(pathfolder3)

# adduser starts here

            # dest='./gmm_models/'
            # count=1

            # for path in os.listdir(source):
            #         path=os.path.join(source,path)

            #         features=np.array([])

            #         #reading audio files
            #         #imported from line number 10
            #         (sr,audio)=read(path)

            #         #extracting mfcc and delta

            #         vector=extract_features(audio,sr)

            #         if features.size ==0:
            #             features=vector
            #         else:
            #             features=np.vstack((features,vector))
                    

            #         if count==5:
            #             gmm = GMM(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
            #             gmm.fit(features)

            #             # saving the trained gaussian model
            #             print("Saving Model")
            #             pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            #             print(name + ' added successfully') 
                        
            #             features = np.asarray(())
            #             count = 0

            #         count=count+1

        return ('', 204)
    else:
        return ('', 204)


def adduser(arg):
    print("successfully doing")
    
    source = arg
           
    dest='./gmm_models/'
    count=1

    for path in os.listdir(source):
        path=os.path.join(source,path)

        features=np.array([])

        #reading audio files
        #imported from line number 10
        (sr,audio)=read(path)

        #extracting mfcc and delta

        vector=extract_features(audio,sr)

        if features.size ==0:
            features=vector
        else:
            features=np.vstack((features,vector))
        

        if count==5:
            gmm = GMM(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)

            # saving the trained gaussian model
            print("Saving Model")
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully') 
            
            features = np.asarray(())
            count = 0

        count=count+1

if __name__ == "__main__":
    app.run(debug=True)