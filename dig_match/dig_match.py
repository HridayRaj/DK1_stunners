from pocketsphinx import Pocketsphinx, get_model_path, get_data_path
import soundfile


#Digit Transcript Map
digmap = {
    '0':'ZERO',
    '1':'ONE',
    '2':'TWO',
    '3':'THREE',
    '4':'FOUR',
    '5':'FIVE',
    '6':'SIX',
    '7':'SEVEN',
    '8':'EIGHT',
    '9':'NINE'
}

#Model files
config = {
    'hmm': 'indigits.cd_cont_200', #HMM model
    'lm': 'indigits.lm', #Language Model
    'dict': 'indigits.dic' #Dictionary
}

def match(wav_path,target_number,threshold):

    #Obtain number transcript
    target = str(target_number)
    target_array = []
    for d in target:
        target_array.append(digmap[d])
    
    #Changing bitrate to PCM_16
    data, samplerate = soundfile.read(wav_path)
    soundfile.write('match.wav', data, samplerate, subtype='PCM_16')

    #Configuring decoder
    ps = Pocketsphinx(**config)

    #Decoding
    ps.decode(
        audio_file= 'match.wav',
        buffer_size=2048,
        no_search=False,
        full_utt=False
    )

    #Obtain segments and remove silent segments
    segments = ps.segments()
    seg_array = []
    for seg in segments:
        if(seg!='<s>' and seg!='</s>' and seg!='<sil>'):
            seg_array.append(seg)
    
    #Matching
    matches = 0
    for t,s in zip(target_array,seg_array):
        if(t==s):
            matches=matches+1

    #Analyze according to threshold
    score = int(((matches/len(target))*10))
    if(score>=threshold):
        return True
    else:
        return False

