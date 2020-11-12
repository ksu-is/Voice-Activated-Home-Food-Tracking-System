#Test
import os.path
from os import path 
import speech_recognition as sr
import pyttsx3

sysName='Kitchen'

def respond(msg, speaker):
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
        respond(itemName, ' not found')
    inventoryFile = open('inventory.csv','w+')
    inventoryFile.seek(0) 
    inventoryFile.write("".join(lines))
    respond('Removing Item',sysName)    

def getAudio(silent=False):
    r = sr.Recognizer()
    with sr.Microphone() as source:     
        #respond("Speak Anything :")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source) 
    try:
        text = r.recognize_google(audio)
        text = text.lower().strip()
        if not silent:    
            print('You:',text)
        return(text) 
    except:
        if not silent:
            respond("Sorry could not recognize your voice",sysName)
        return(getAudio(silent))
    
def confirm(msg):
    respond(msg,sysName)
    c = getAudio()
    if 'yes' in c or 'ya' in c or 'yeah' in c:
        return 'yes'
    elif 'no' in c:
        return 'no'
    elif 'nevermind' in c:
        return 'nevermind'
    else:
        respond('Sorry, I did not quite catch that. Please respond with yes or no.',sysName)
        return(confirm(msg))

#Function isolates the quanitity from the given text and returns quantity
#Quantity must be stated before the item or Q will return ""
def findQ(txt):
    quantity = ""
    for char in txt:
        if char.isdigit():
            quantity+=char
        else:
            break
    return quantity

#Function strips out digits and returns the item to be added by the program
def findItem(txt):
    item = ""
    item=txt.strip('0123456789').strip()
    return item

def main():
    # If inventory.csv does not exist, create the file
    if (not path.exists("inventory.csv")):
        inventoryFile = open('inventory.csv','w')
        inventoryFile.close()

    text = "default"
    while not "exit kitchen" in text:            
        print('not shut down kitchen in text','shut down kitchen' in text)
        text=getAudio(True)
        if 'hey kitchen' in text:
            while True:
                respond('What would you like to do?',sysName)
                text=getAudio()
                if 'nevermind' in text:
                    respond('ok',sysName)
                    break

                elif text.startswith('add'):
                    text = text[3::].strip()
                    quantity = findQ(text)
                    item = findItem(text)
                    if item == "":
                        respond('What would you like to add?',sysName)
                        text = getAudio()
                        quantity = findQ(text)
                        item = findItem(text)
                        if 'nevermind' in item:
                            break
                    confirmation = confirm('Just to be sure, you would like to add'+' '+quantity+' '+item)
                    if confirmation == 'nevermind':
                        break
                    while(confirmation != 'yes'):
                        respond('What would you like to add?',sysName)
                        text=getAudio()
                        item = findItem(text)
                        quantity = findQ(text)
                        if 'nevermind' in item:
                            break
                        confirmation = confirm('Just to be sure, you would like to add'+' '+quantity+' '+item)
                        if confirmation == 'nevermind':
                            break
                    if 'nevermind' in item or 'nevermind' in confirmation:
                        break
                    respond('Adding '+quantity +' '+item,sysName)
                    if quantity == "":
                        addItem(item)
                    else:
                        addItem(item,quantity)
                    break  
                
                elif text.startswith('remove'):
                    item = text[6::].strip()
                    quantity = findQ(text)
                    item = findItem(text)
                    if item == "":
                        respond('What would you like to remove?',sysName)
                        text = getAudio()
                        quantity = findQ(text)
                        item = findItem(text)
                        if 'nevermind' in item:
                            break
                    confirmation = confirm('Just to be sure, you would like to remove'+' '+quantity+' '+item)
                    if confirmation == 'nevermind':
                        break
                    while(confirmation != 'yes'):
                        respond('What would you like to remove?',sysName)
                        text=getAudio()
                        item = findItem(text)
                        quantity = findQ(text)
                        if 'nevermind' in item:
                            break
                        confirmation = confirm('Just to be sure, you would like to remove'+' '+quantity+' '+item)
                        if confirmation == 'nevermind':
                            break
                    if 'nevermind' in item or 'nevermind' in confirmation:
                        break
                    respond('Removing '+quantity +' '+item,sysName)
                    if quantity == "":
                        removeItem(item)
                    else:
                        removeItem(item,quantity)
                    break
                
    respond("exiting",sysName)
main()
