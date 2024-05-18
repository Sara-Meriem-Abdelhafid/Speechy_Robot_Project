import speech_recognition as sr
import pyttsx3


r = sr.Recognizer() 


def record_text():
    #loop in case of errors
    while(1):
        try:
            #use the mic as a source of input
            with sr.Microphone() as source2:
                #prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                #listen for the user's input
                audio2 = r.listen(source2)

                #using google to recognaize audio
                Mytext = r.recognize_google(audio2)

                return Mytext

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown Error Occurred") 


def output_text(text):
    f = open("speech_to_text_output_file.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    return


while(True):
    text= record_text()
    output_text(text)


    print("Text")

