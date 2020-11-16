from tkinter import *

master = Tk()
listbox = Listbox(master)
listbox.pack()

listbox.insert(END, "Item\tquantity")
inventoryFile = open('inventory.csv','r+')
inventoryFile.seek(0)
lines = inventoryFile.readlines()
inventoryFile.close()
for line in lines:
    listbox.insert(END, line.replace(',','\t'))

mainloop()