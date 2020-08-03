''' importing all the libraries '''
import speech_recognition as sr
import os
import time
import pyaudio
from IPython.display import Audio, display, clear_output
import wave
import random
import pickle
from scipy.io.wavfile import  read
from sklearn.mixture import GaussianMixture as GMM
import warnings
warnings.filterwarnings("ignore")

from sklearn import preprocessing
 # for converting audio to mfcc
import python_speech_features as mfcc
import numpy as np

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
    print("--------yahaa-------")
    # return "Stranger"
    text=r.recognize_google(audio , language='en-US')
    
    print(text)
    return int(text)

#''' functio for calculating threshold 


def calc_thresh(scores,alpha):
    meu=np.mean(scores)
    sigma=np.std(scores)
    return meu -alpha*sigma


#''' 

def recog_user(t):


    # CHUNK = 1024
    # FORMAT = pyaudio.paInt16
    # CHANNELS = 1
    # RATE = 44100
    # RECORD_SECONDS = 4
    # FILENAME = "./output.wav"

    # p = pyaudio.PyAudio()

    # stream = p.open(format=FORMAT,
    #                 channels=CHANNELS,
    #                 rate=RATE,
    #                 input=True,
    #                 frames_per_buffer=CHUNK)
    
    # for i in range(3):
    #     time.sleep(1.0)
    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     print(f"Speak in {i} sec")

    # t=random.randint(1000,9999)
    # print(t)
    # print("* recording")

    # frames = []

    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)

    # print("* done recording")

    # stream.stop_stream() 
    # stream.close()
    # p.terminate()

    # wf = wave.open(FILENAME, 'wb')
    # wf.setnchannels(CHANNELS)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(RATE)
    # wf.writeframes(b''.join(frames))
    # wf.close()
    FILENAME = "./output.wav"
    print(t)
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
    # sum_=sum(threshold_list)
    # if(sum_==0):

    #     ''' here return a false or "unknown string " value '''
    #     print("You are Stranger ")
    #     return "stranger"
       
    # else:
    pred = np.argmax(log_likelihood)
    print(f"pred value for this is : {pred}")
    identity = speakers[pred]
    
    # if voice not recognized than terminate the process
    if identity == 'unknown':
            print("Not Recognized! Try again...")
            # return "not recognized"
            print("-----------first print")
            return
    else:  
            ''' here return the user from the from the function '''
            print(f"recognised as {identity}") 
            print(" -----------second print")
            return identity
    


if __name__ == "__main__":
    recog_user()