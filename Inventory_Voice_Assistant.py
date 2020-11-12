#Test
import os.path
from os import path 
import speech_recognition as sr
import pyttsx3

sysName='Kitchen'

def respond(msg,speaker):
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    
    engine.setProperty('voice',voices[1].id)
    print(speaker+':', msg)
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
    respond('Removing Item',sysName)    

def getAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:     
        #respond("Speak Anything :")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source) 
    try:
        text = r.recognize_google(audio)
        text = text.lower().strip()    
        print('You:',text)
        return(text) 
    except:
        respond("Sorry could not recognize your voice",sysName)
        return(getAudio())
    
def confirm(msg):
    respond(msg,sysName)
    c = getAudio()
    if 'yes' in c or 'ya' in c or 'yeah' in c:
        return True
    elif 'no' in c:
        return False
    else:
        respond('Sorry, I did not quite catch that. Please respond with yes or no.',sysName)
        return(confirm(msg))



def main():
    # If inventory.csv does not exist, create the file
    if (not path.exists("inventory.csv")):
        inventoryFile = open('inventory.csv','w')
        inventoryFile.close()

    text = "default"
    while not "exit kitchen" in text:            
        print('not shut down kitchen in text','shut down kitchen' in text)
        text=getAudio()
        if 'hey kitchen' in text:
            while True:
                respond('What would you like to do?',sysName)
                text=getAudio()
                if 'nevermind' in text:
                    respond('ok',sysName)
                    break

                elif text.startswith('add'):
                    item = text[3::].strip()
                    if item == "":
                        respond('What item would you like to add?',sysName)
                        item = getAudio()
                    if 'nevermind' in item:
                        break
                    while(not confirm('Just to be sure, you would like to add 1 '+item)):
                        respond('What item would you like to add?',sysName)
                        item=getAudio()
                        if 'nevermind' in item:
                            break
                    if 'nevermind' in item:
                        break 
                    respond('Adding 1 ' + item,sysName)
                    addItem(item,1)
                    break  
                
                elif text.startswith('remove'):
                    item = text[6::].strip()
                    if item == "":
                        respond('What item would you like to remove?',sysName)
                        item = getAudio()
                    if 'nevermind' in item:
                        break
                    while(not confirm('Just to be sure, you would like to remove 1 '+item)):
                        respond('What item would you like to remove?',sysName)
                        item=getAudio()
                        if 'nevermind' in item:
                            break  
                    if 'nevermind' in item:
                        break 
                    respond('removing 1 ' + item,sysName)
                    addItem(item,1)
                    break
                
    respond("exiting",sysName)
main()
