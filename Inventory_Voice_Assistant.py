#Test
import os.path
from os import path 
import speech_recognition as sr
import pyttsx3

def respond(msg):
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    
    engine.setProperty('voice',voices[1].id)
    print(msg)
    engine.say(msg)
    engine.runAndWait()

def addItem(itemName,qt=1):
    inventoryFile = open('inventory.csv','r+')
    inventoryFile.seek(0)
    lines = inventoryFile.readlines()
    inventoryFile.close()
    #print(lines)
    found = False
    for index in range(len(lines)):
        if itemName in lines[index]:
            #print(lines[index])
            temp = lines[index].split(',')
            temp2= temp[1]
            oldQ=int(temp2)
            lines[index]=itemName+','+str(int(qt+oldQ))+'\n'
            found = True
            break
    if(not found):
        lines.append(itemName+','+str(qt)+'\n')
    inventoryFile = open('inventory.csv','w+')
    inventoryFile.seek(0) 
    inventoryFile.write("".join(lines))

def removeItem(itemName, qt=1):
    inventoryFile = open('inventory.csv','r+')
    inventoryFile.seek(0)
    lines = inventoryFile.readlines()
    inventoryFile.close()
    #print(lines)
    found = False
    for index in range(len(lines)):
        if itemName in lines[index]:
            #print(lines[index])
            temp = lines[index].split(',')
            temp2= temp[1]
            oldQ= int(temp2)
            found= True
            if oldQ-qt >0:
                lines[index]=itemName+','+str(oldQ-int(qt))+'\n'
            else:
                lines.remove(index)
            #found = True
            break
    if(not found):
        respond(itemName + ' not found')
    inventoryFile = open('inventory.csv','w+')
    inventoryFile.seek(0) 
    inventoryFile.write("".join(lines))
    respond('Remove Item')    

def getAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:     
        #respond("Speak Anything :")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source) 
    try:
        text = r.recognize_google(audio)
        text = text.lower().strip()    
        respond("You said : {}".format(text))
        return(text) 
    except:
        respond("Sorry could not recognize your voice")
        return(getAudio())
    
def confirm(msg):
    respond(msg)
    confirm = getAudio()
    if 'yes' in confirm or 'ya' in confirm:
        return True
    elif 'no' in confirm:
        return False
    else:
        respond('Sorry, I did not quite catch that. Please respond with yes or no.')
        return(confirm(msg))



def main():
    # If inventory.csv does not exist, create the file
    if (not path.exists("inventory.csv")):
        inventoryFile = open('inventory.csv','w')
        inventoryFile.close()

    text = "default"
    while(not "exit kitchen" in text):            
        text=getAudio()
        if 'hey kitchen' in text:
            while True:
                respond('Would you like to add or remove an item')
                text=getAudio()
                if 'nevermind' in text:
                    respond('ok')
                    break

                elif text.startswith('add'):
                    respond('What item would you like to add?')
                    item = getAudio()
                    if 'nevermind' in item:
                        break
                    while(not confirm('Just to be sure, you would like to add 1 '+item)):
                        respond('What item would you like to add?')
                        item=getAudio()
                        if 'nevermind' in item:
                            break
                    if 'nevermind' in item:
                        break 
                    respond('Adding 1 ' + item)
                    addItem(item,1)
                    break  
                
                elif text.startswith('remove'):
                    respond('What item would you like to remove?')
                    item = getAudio()
                    if 'nevermind' in item:
                        break
                    while(not confirm('Just to be sure, you would like to remove 1 '+item)):
                        respond('What item would you like to remove?')
                        item=getAudio()
                        if 'nevermind' in item:
                            break  
                    if 'nevermind' in item:
                        break 
                    respond('removing 1 ' + item)
                    addItem(item,1)
                    break
                
    respond("exiting")
main()
