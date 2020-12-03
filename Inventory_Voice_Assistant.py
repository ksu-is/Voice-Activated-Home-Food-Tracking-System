#Test
import os.path
from os import path 
import speech_recognition as sr
import pyttsx3

#sysName must be lowercase
sysName='kitchen'
#Function allows for program to speak to user#
#Prints text to console#
def respond(msg:str, speaker:str):
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    
    engine.setProperty('voice',voices[1].id)
    print(speaker.title()+':', msg)
    engine.say(msg)
    engine.runAndWait()

#Adds item to inventory.csv#
def addItem(itemName:str,qt:str="1"):
    #Reading inventory#
    inventoryFile = open('inventory.csv','r+')
    inventoryFile.seek(0)
    lines = inventoryFile.readlines()
    inventoryFile.close()
    
    #check to see if item is already inventory#
    found = False
    for index in range(len(lines)):
        #if item is found in inventory, modifies existing quatity#
        if itemName in lines[index]:
            temp = lines[index].split(',')
            temp2= temp[1]
            oldQ=int(temp2)
            lines[index]=itemName+','+str(int(qt)+oldQ)+'\n'
            found = True
            break
    #if item is found in inventory, add new entry#    
    if(not found):
        lines.append(itemName+','+str(qt)+'\n')
    #overwrite old inventory with new changes#  
    inventoryFile = open('inventory.csv','w+')
    inventoryFile.seek(0) 
    inventoryFile.write("".join(lines))

#removes item from inventory.csv#
def removeItem(itemName:str,qt:str="1"):
    inventoryFile = open('inventory.csv','r+')
    inventoryFile.seek(0)
    lines = inventoryFile.readlines()
    inventoryFile.close()
    #print(lines)
    found = False
    #check to see if item is already inventory#
    for index in range(len(lines)):
        #if item is found in inventory, modifies existing quatity#
        if itemName in lines[index]:
            temp = lines[index].split(',')
            temp2= temp[1]
            oldQ= int(temp2)
            found= True
            if oldQ-qt >0:
                lines[index]=itemName+','+str(oldQ-int(qt))+'\n'
            else:
                lines.remove(index)
            break
    if(not found):
        respond(itemName, ' not found')
    #overwrite old inventory with new changes#
    global lst
    lst = lines
    inventoryFile = open('inventory.csv','w+')
    inventoryFile.seek(0) 
    inventoryFile.write("".join(lines))
    respond('Removing Item',sysName)    

#function checks to see if item is in inventory, returns quantity as a string
def query(itemName:str)-> str:
    inventoryFile = open('inventory.csv','r+')
    inventoryFile.seek(0)
    lines = inventoryFile.readlines()
    inventoryFile.close()
    #print(lines)
    found = False
    #check to see if item is already inventory#
    for index in range(len(lines)):
        #if item is found in inventory, modifies existing quatity#
        if itemName in lines[index]:
            temp = lines[index].split(',')
            quantity= temp[1].strip()
            found = True
            return quantity
    if not found:
        return "0"    

#listens to speech from user and transcribes to text#
#If silent, system is listening with no output to user#
def getAudio(silent=False):
    #Record user#
    r = sr.Recognizer()
    with sr.Microphone() as source:     
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source) 
    #transcription of audio#
    try:
        text = r.recognize_google(audio)
        text = text.lower().strip()
        if not silent:    
            print('You:',text)
        return(text) 
    except:
        if not silent:
            respond("Sorry could not recognize your voice",sysName)
        #Since speech recognition fails try again#
        return(getAudio(silent))

#confirms action with user#
#returns "yes", "no", "nevermind"#    
def confirm(msg:str)-> str: 
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

#Function isolates the quanitity from the given text and returns quantity#
#Quantity must be stated before the item or Q will return ""#
def findQ(txt:str)-> str:
    quantity = ""
    for char in txt:
        if char.isdigit():
            quantity+=char
        else:
            break
    return quantity

#Function strips out digits and returns the item to be added by the program#
def findItem(txt:str)->str:
    item = ""
    item=txt.strip('0123456789').strip()
    return item 

def main():
    # If inventory.csv does not exist, create the file#
    if (not path.exists("inventory.csv")):
        inventoryFile = open('inventory.csv','w')
        inventoryFile.close()
    text = "default"
    #Loop keeps listening until user speaks sysName and will only exit with "exit" + sysName#
    while not "exit " + sysName in text:            
        #system will remain silent until user speaks "hey" + sysName#
        
        text=getAudio(True)
        if "hey " + sysName in text:
            while True:
                respond('What would you like to do?',sysName)
                text=getAudio()
                if 'nevermind' in text:
                    respond('ok',sysName)
                    break

                
                elif text.startswith('add'):
                    #remove "add" from command so as not to be processed in "addItem" function#
                    text = text[3::].strip()
                    #extracting quantity from user speech#
                    quantity = findQ(text)
                    #extracting item from user speech#
                    item = findItem(text)
                    #if user does not supply item, system prompts user to do so#
                    if item == "":
                        respond('What would you like to add?',sysName)
                        if text.startswith('add'):
                            text = text[3::].strip()
                        text = getAudio()
                        quantity = findQ(text)
                        item = findItem(text)
                        if 'nevermind' in item:
                            break
                    #confirm that user wants to perform action#
                    confirmation = confirm('Just to be sure, you would like to add'+' '+quantity+' '+item)
                    if confirmation == 'nevermind':
                        break
                    while(confirmation != 'yes'):
                        respond('What would you like to add?',sysName)
                        if text.startswith('add'):
                            text = text[3::].strip()
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
                    #adds to inventory.csv#
                    respond('Adding '+quantity +' '+item,sysName)
                    if quantity == "":
                        addItem(item)
                    else:
                        addItem(item,quantity)
                    break  
                
                elif text.startswith('remove'):
                    #remove "remove" from command so as not to be processed in "remove" function#
                    text = text[6::].strip()
                    #extracting quantity from user speech#
                    quantity = findQ(text)
                    #extracting item from user speech#
                    item = findItem(text)
                    #if user does not supply item, system prompts user to do so#
                    if item == "":
                        respond('What would you like to remove?',sysName)
                        if text.startswith('remove'):
                            text = text[6::].strip()
                        text = getAudio()
                        quantity = findQ(text)
                        item = findItem(text)
                        if 'nevermind' in item:
                            break
                    #confirm that user wants to perform action#    
                    confirmation = confirm('Just to be sure, you would like to remove'+' '+quantity+' '+item)
                    if confirmation == 'nevermind':
                        break
                    while(confirmation != 'yes'):
                        respond('What would you like to remove?',sysName)
                        if text.startswith('remove'):
                            text = text[6::].strip()
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
                    #removes item from inventory.csv#
                    if quantity == "":
                        removeItem(item)
                    else:
                        removeItem(item,quantity)
                    break
                
                elif text.startswith("clear"):
                    confirmation = confirm('Just to be sure, you would like to clear inventory?')
                    if confirmation != "yes":
                        break
                    else:
                        inventoryFile = open('inventory.csv','w')
                        inventoryFile.close()
                        respond('Inventory has been cleared', sysName)
                        break

                elif text.startswith('look up'):
                    itemName = text[7::].strip()
                    if itemName == "":
                        respond('What would you like to look up?', sysName)
                        itemName = getAudio()
                    quantity = query(itemName) 
                    respond('Found ' + quantity + ' ' + itemName, sysName)
                    break
main()                    
respond("exiting",sysName)