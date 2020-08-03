''' importing all the libraries '''
import speech_recognition as sr
import os
import time
import pyaudio
from IPython.display import Audio, display, clear_output
import wave
import random
import pickle
from scipy.io.wavfile import read
from sklearn.mixture import  GaussianMixture as GMM
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

    ''' recogizer'''

    print("You Said")
    text=r.recognize_google(audio , language='en-US')
    print(text)
    return int(text)

def adduser(name):
    # name=input("Enter your name \n")
    # Voice authentication

    # CHUNK = 1024
    # FORMAT = pyaudio.paInt16
    # CHANNELS = 1
    # RATE = 44100
    # RECORD_SECONDS = 4
    # WAVE_OUTPUT_FILENAME = "output.wav"

    source = "./voice_database/" + name
        
    # os.mkdir(source)


    # for i in range(5):

    #     if i == 0:
            
    #         j = 3
    #         while j>=0:
    #             time.sleep(1.0)
    #             os.system('cls' if os.name == 'nt' else 'clear')
    #             print("Speak the bellow number in {} seconds".format(j))
    #             j-=1
            
    #         t=random.randint(1000,9999)
    #         print(f' \n{t}')


    #     else:
    #         time.sleep(2.0)

    #         t=random.randint(1000,9999)
    #         print(f"********Speak One more time************\n{t}")
    #         print(f' \n{t}')
            
            
    #         #time.sleep(3.0)
                


    #     p = pyaudio.PyAudio()

    #     stream = p.open(format=FORMAT,
    #                     channels=CHANNELS,
    #                     rate=RATE,
    #                     input=True,
    #                     frames_per_buffer=CHUNK)

    #     print("Recording")

    #     frames = []

    #     for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #         data = stream.read(CHUNK)
    #         frames.append(data)

    #     print("* done recording")

    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()

    #     wf = wave.open(source + '/' + str((i+1)) + '.wav', 'wb')
    #     wf.setnchannels(CHANNELS)
    #     wf.setsampwidth(p.get_sample_size(FORMAT))
    #     wf.setframerate(RATE)
    #     wf.writeframes(b''.join(frames))
    #     wf.close()
    #     if(t==recog(source + '/' + str((i+1)) + '.wav')):
    #         print("\t Recorded Successfully\t")

    
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
        

        if count==3:
            gmm = GMM(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)

            # saving the trained gaussian model
            print("Saving Model")
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully') 
            
            features = np.asarray(())
            count = 0

        count=count+1

if __name__== '__main__':
    adduser()


    
