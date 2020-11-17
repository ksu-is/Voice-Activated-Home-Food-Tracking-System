#from tkinter import *

#master = Tk()
#listbox = Listbox(master)
#listbox.pack()

#listbox.insert(END, "Item\tquantity")
inventoryFile = open('inventory.csv','r+')
inventoryFile.seek(0)
lines = inventoryFile.readlines()
inventoryFile.close()
lst = []
lst.append(['Item','Quantity'])
for line in lines:
    print(line.strip())
    lst.append(line.strip().split(',')) 
print(lst)   
#for line in lines:
    #listbox.insert(END, line.replace(',','\t'))

#mainloop()


from tkinter import *
pad=3
class Table: 
      
    def __init__(self,root): 
          
        # code for creating table 
        for i in range(total_rows): 
            for j in range(total_columns): 
                  
                self.e = Entry(root, width=30, fg='blue', 
                               font=('Arial',40,'bold')) 
                  
                self.e.grid(row=i, column=j) 
                self.e.insert(END, lst[i][j]) 
#label.config(width=200)  
#take the data 
#find total number of rows and 
#columns in list 
total_rows = len(lst) 
total_columns = len(lst[0]) 
   
#create root window 
root = Tk() 
t = Table(root) 
root.mainloop()

