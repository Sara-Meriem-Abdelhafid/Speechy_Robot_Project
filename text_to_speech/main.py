import os
import wave 
import langid
#import openai
#import librosa

import sklearn
import pyaudio #python bindings for PortAudio the cross_platform audio i/o  library

import fasttext
import playsound
from gtts import gTTS
import librosa.display
from langdetect import detect
from pydub import AudioSegment
import pyttsx3 #text to speech
import matplotlib.pyplot as plt
import speech_recognition as sr #Speech to text
from translate import Translator
#from googletrans import Translator
from tempfile import NamedTemporaryFile
from IPython.display import Audio, display
from transformers import MarianMTModel, MarianTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
#from transliterate import translit




#### FUNCTIONS
# choose_microphone
def choose_microphone():
    print("Available Microphones:")
    microphones = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(microphones):
        print(f"{i}: {mic}")
    while True:
        choice = input("Enter the index or name of the microphone you want to use to record audio: ")
        if choice.isdigit():
            choice = int(choice)
            if 0 <= choice < len(microphones):
                print(f"The microphone used is {choice} : {microphones[choice]}.")
                return choice
        elif choice in microphones:
            print(f"The microphone used is {choice} : {microphones[choice]}.")
            return choice
        print("Invalid choice. Please enter a valid index or microphone name.")


# Function to translate "I'm Listening to you..." automatically
def translit_message(text,language):
    translator = Translator(to_lang=language)

    try:
        # Translate using translate library
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Language not supported for translation: {str(e)}"


# save input audio wave
def save_input_audio(audio, c, save_dir="audio_in_out/inputs_audio"):
    # Ensure the directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Write wave file
    sample_rate = 48000.0  # Hertz
    frames = audio.get_wav_data()
    wav_filename = os.path.join(save_dir, f"input_audio_{c}.wav")
    with wave.open(wav_filename, 'w') as obj:
        obj.setnchannels(1)  # Mono or 2
        obj.setsampwidth(2)
        obj.setframerate(sample_rate)
        obj.writeframes(frames)
    
    print(f"Audio has been saved to: {wav_filename}")
    return wav_filename


# save output audio wave
def save_output_audio(audio, c, save_dir="audio_in_out/outputs_audio"):
    # Ensure the directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Write wave file
    sample_rate = 48000.0  # Hertz
    frames = audio.get_wav_data()
    wav_filename = os.path.join(save_dir, f"output_audio_{c}.wav")
    with wave.open(wav_filename, 'w') as obj:
        obj.setnchannels(1)  # Mono or 2
        obj.setsampwidth(2)
        obj.setframerate(sample_rate)
        obj.writeframes(frames)
    
    print(f"Audio has been saved to: {wav_filename}")
    return wav_filename


# save the INPUT text output in a file 
def input_text_to_file(text, c, save_dir="text_in_out/inputs_text"):
    file_path = os.path.join(save_dir, f"input_text_{c}.txt")
    with open(file_path, "a") as f:
        f.write(text + "\n")
        print(text," was written in ",file_path)


# save the OUTPUT text output in a file 
def output_text_to_file(text, c, save_dir="text_in_out/outputs_text"):
    file_path = os.path.join(save_dir, f"output_text_{c}.txt")
    with open(file_path, "a") as f:
        f.write(text + "\n")
        print(text," was written in ",file_path)


# record Speech and convert it to Text as input
def record_speech_to_text(chosen_microphone,c,language):
    recognizer = sr.Recognizer()
    #get audio and save it
    with sr.Microphone() as source: #device_index=chosen_microphone
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        translation=translit_message("Hello I'm listening, how can I help you?",language)
        text_to_speech(translation, language) 
        print(translation,"...")
        '''if language=='en' :
            print("Listening...")
        elif language=='ar':
            print("...في الاستماع")
        elif language=='fr':
            print("écoute...")'''
        audio = recognizer.listen(source)
        # Save the captured audio to a WAV file
        wav_filename = save_input_audio(audio, c)

        # Play back the captured audio
        #play_audio(audio)
        playsound.playsound(wav_filename)  # Play the input wav file in recorded voice instead of speak it 

    #convert audio to text
    try:
        # Use Google's speech recognition with language detection
        text = recognizer.recognize_google(audio, language=language) # Use Google's speech recognition and Specify language parameter for Arabic ('ar')
        print("audio has been converted to : ",text)
        #input_text_to_file(text, c)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""


# read the INPUT text from a file
def read_text_from_inputs(c,save_dir="text_in_out/inputs_text"):
    file_path = os.path.join(save_dir, f"input_text_{c}.txt")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# read the OUTPUT text from a file
def read_text_from_outputs(c,save_dir="text_in_out/outputs_text"):
    file_path = os.path.join(save_dir, f"output_text_{c}.txt")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# speak the text_output and save it in a file 
def text_to_speech(text, lang):
    if not text:
        translation = translit_message("There is no text_to_speech conversion.", lang)
        print(translation)
        return  # Return if there is no text to convert

    # Convert text to speech
    with NamedTemporaryFile(delete=False) as tmp_mp3:
        tts = gTTS(text=text, lang=lang)
        tts.save(tmp_mp3.name)
        tmp_mp3.flush()  # Ensure all data is written to the file

        # Play the speech
        playsound.playsound(tmp_mp3.name, True)



# speak the text_output and save it in a file 
def text_to_speach_input(text, lang, c, audio_save_dir="audio_in_out/inputs_audio"):
    if not text:
        translation=translit_message("There is no text_to_speech conversion.",lang)
        print(translation)
        return
        '''if lang == 'en':
            print("There is no text_to_speech conversion.")
        elif lang == 'ar':
            print(".لا يوجد نص للتحويل إلى كلام")
        elif lang == 'fr':
            print("Il n’y a pas de conversion texte-parole.")
        '''

    # Ensure the directory exists
    if not os.path.exists(audio_save_dir):
        os.makedirs(audio_save_dir)
        
    # Generate the filename for the wav file
    wav_filename = os.path.join(audio_save_dir, f"input_audio_{c}.wav")

    # Convert text to speech and save directly as wav using a temporary mp3 file
    with NamedTemporaryFile(delete=True) as tmp_mp3:
        tts = gTTS(text=text, lang=lang)
        tts.save(tmp_mp3.name)

        # Convert the mp3 file to wav
        sound = AudioSegment.from_mp3(tmp_mp3.name)
        sound.export(wav_filename, format="wav")


    # Play the wav file
    playsound.playsound(wav_filename)

    print(f"The response audio has been saved to: {wav_filename}")


# speak the text_output and save it in a file 
def text_to_speach_output(text, lang, c, audio_save_dir="audio_in_out/outputs_audio"):
    if not text:
        translation=translit_message("There is no text_to_speech conversion.",lang)
        print(translation)
        return
        '''if lang == 'en':
            print("There is no text_to_speech conversion.")
        elif lang == 'ar':
            print(".لا يوجد نص للتحويل إلى كلام")
        elif lang == 'fr':
            print("Il n’y a pas de conversion texte-parole.")
        '''

    # Ensure the directory exists
    if not os.path.exists(audio_save_dir):
        os.makedirs(audio_save_dir)
        
    # Generate the filename for the wav file
    wav_filename = os.path.join(audio_save_dir, f"output_audio_{c}.wav")

    # Convert text to speech and save directly as wav using a temporary mp3 file
    with NamedTemporaryFile(delete=True) as tmp_mp3:
        tts = gTTS(text=text, lang=lang)
        tts.save(tmp_mp3.name)

        # Convert the mp3 file to wav
        sound = AudioSegment.from_mp3(tmp_mp3.name)
        sound.export(wav_filename, format="wav")


    # Play the wav file
    playsound.playsound(wav_filename)

    print(f"The response audio has been saved to: {wav_filename}")


# speak the text_output from a file and save it in an audio 
def text_to_speach_output_from_file(c, audio_save_dir="audio_in_out/outputs_audio"):
    # Generate the filename for the wav file
    wav_filename = os.path.join(audio_save_dir, f"output_audio_{c}.wav")

    # Ensure the directory exists
    if not os.path.exists(audio_save_dir):
        os.makedirs(audio_save_dir)

    # Read the text from the file
    text = read_text_from_outputs(c)
    if not text:
        #translation=translit_message("There is no text_to_speech conversion.",language_code)
        #print(translation)
        print("There is no text_to_speech conversion.")
        '''if lang == 'en':
            print("There is no text_to_speech conversion.")
        elif lang == 'ar':
            print(".لا يوجد نص للتحويل إلى كلام")
        elif lang == 'fr':
            print("Il n’y a pas de conversion texte-parole.")'''
        return
    language_code, language = detect_language(text)
    print("text: ", text, " in ",language)


    # Convert text to speech and save directly as wav using a temporary mp3 file
    with NamedTemporaryFile(delete=True) as tmp_mp3:
        tts = gTTS(text=text,lang=language_code)#, 
        tts.save(tmp_mp3.name)

        # Convert the mp3 file to wav
        sound = AudioSegment.from_mp3(tmp_mp3.name)
        sound.export(wav_filename, format="wav")

    # Play the wav file
    playsound.playsound(wav_filename)

    print(f"The response audio has been saved to: {wav_filename}")



# Function to detect the language of the input text
fasttext_model = fasttext.load_model('lid.176.bin')# Pre-Trained model for language identification
# Language code to language name mapping
language_mapping = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "ca": "Catalan",
    "cs": "Czech",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "ka": "Georgian",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ms": "Malay",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sq": "Albanian",
    "sr": "Serbian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh": "Chinese",
    # Add more languages as needed
}
# Function to detect the language of the input text using fastText
def detect_language(text):
    # Remove newline characters from the input text
    text = text.replace('\n', ' ')
    predictions = fasttext_model.predict(text, k=1)  # k=1 returns the top prediction
    language_code = predictions[0][0].replace('__label__', '')
    language_name = language_mapping.get(language_code, "Unknown")
    return language_code, language_name

#'''
#play audio function
def play_audio(audio):
    audio_data = audio.get_wav_data()
    with wave.open("temp_audio.wav", "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        f.setframerate(16000)
        f.writeframes(audio_data)
        
    # Open the temporary WAV file and play it
    p = pyaudio.PyAudio()
    wf = wave.open("temp_audio.wav", "rb")# read byte mode
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()

    p.terminate()#'''




    ###### RUN

    # Ensure pydub can find the ffmpeg/ffprobe binary
AudioSegment.converter = "ffmpeg"  # path to ffmpeg binary

#pip install translate
#wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
'''/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ffmpeg
ffmpeg -version
#pip install speechrecognition
#pip install pyttsx3
#pip install pyttsx4
#brew install portaudio
#pip uninstall pyaudio
#pip install pyaudio

'''


# choose_microphone
chosen_microphone = 1 #choose_microphone()#3 #

# test audio:
#text_to_speech("Hello, how are you?", "en")


'''
# Function to translate "I'm Listening to you..." automatically
text="how are you I'm Listening to you...?"
print(translit_message(text,'ar'))  # Output: أنا أستمع إليك... (or similar in Arabic)
print(translit_message(text,'en'))  # Output: I'm Listening to you...
print(translit_message(text,'fr'))  # Output: Je vous écoute... (or similar in French)
print(translit_message(text,'it'))  # Output: 我在听你... (or similar in Chinese)'''


'''# save the INPUT text output in a file 
input_text_to_file("كم الساعة الان؟", 1)


# save the OUTPUT text output in a file 
output_text_to_file("الساعة الان الواحدة و النصف ",1)#'''




'''# read the INPUT text from a file
input=read_text_from_inputs(0)
print("input: ",input)

# read the OUTPUT text from a file
output=read_text_from_outputs(13)
print("output: ",output)

#language_code, language = detect_language(output) #get language of output
#text_to_speach_output(output, language_code, c) # speak the text_output and save it in a file '''

'''detected language
prompt1 = "Cómo estás hoy"
prompt2 = "Bonjour Speechy"
prompt3 = "Hello Speechy how are you"
prompt4 = "مرحبا سبيشي"

code1, name1 = detect_language(prompt1)
code2, name2 = detect_language(prompt2)
code3, name3 = detect_language(prompt3)
code4, name4 = detect_language(prompt4)

print(f"The detected language1 is: {code1} ({name1})")
print(f"The detected language2 is: {code2} ({name2})")
print(f"The detected language3 is: {code3} ({name3})")
print(f"The detected language4 is: {code4} ({name4})")'''

# record Speech and convert it to Text as input
text = record_speech_to_text(chosen_microphone,6,'ar')
print("text recorded: ",text)#'''


# General Test
'''c+=1

#GET INPUT
input_text = record_speech_to_text(chosen_microphone,c,'ar')# record Speech and convert it to Text as input
print("text recorded: ",input_text)
input_text_to_file(input_text, c) #save input to file in inputs_folder 
language_code, language = detect_language(input_text)
print("input: ", input_text, " in ",language)
playsound.playsound(f"audio_in_out/inputs_audio/input_audio_{c}.wav")  # Play the input wav file in recorded voice instead of speak it 
#text_to_speach_input(input_text, language_code, c)




#GENERATE OUTPUT
gen_output=read_text_from_inputs(c) #geting text from inputs insted of generating a new output based on the input    #(in futer) generating a new output based on the input   
output_text_to_file(gen_output, c)  #save gen_output to a file in outputs_folder 



#GIVE OUTPUT
#output=read_text_from_outputs(c)    #get output from outputs_folder
#language_code, language = detect_language(output) #get language of output
#text_to_speach_output(output, language_code, c) # speak the text_output and save it in a file 
text_to_speach_output_from_file(c)# speak the text_output from a file and save it in an audio '''
