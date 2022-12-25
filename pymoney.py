import sys
import ast
import tkinter
from tkinter import ttk
from tkinter import messagebox
from pyrecord import *
from pycategory import *

categories = Categories()


record=Records()

window=tkinter.Tk()
window.title('Pymoney')
window.geometry('630x230')
window.configure(background='#cccccc')
text=tkinter.Listbox(window,width=45,height=10)

def Sumup(L):
	all_money=[int(L[i]) for i in range(0,len(L)) if i%4==3]
	return sum(all_money)
def setrecord(*event): #Can't delete argument "event", it means <Return> event.
	e2=datetime.get()
	# if datetime.get()=='':
	# 	e2=str(date.today())
	
	D=e2.split('-')
	try:
		assert len(D)==3 and len(D[0])==4 and len(D[1])==2 and len(D[2])==2
	except AssertionError:
		print('The format of date should be YYYY-MM-DD.\nFail to add a record.')
		tkinter.messagebox.showerror(title="error", message="The format of date should be YYYY-MM-DD.\nFail to add a record.'")
		datetime.delete(0,'end') #輸入後 自動清除輸入欄
		datetime.insert(0,str(date.today()))
		return None

	e3=flat_category[category.current()]
	e4=Description.get()
	if e4=='(Optional)':
		e4=''

	e5=Price.get()
	if e5=='':
		tkinter.messagebox.showerror(title="error", message="Price entry is empty!")
		return
	else:
		try:
			p=int(e5)
		except Exception:
			Price.delete(0,'end')
			tkinter.messagebox.showerror(title="error", message="Price must have to be a number!")
			return

	e=e2+' '+e3+' '+ e4+' '+ e5
	Record=tkinter.StringVar()
	Record.set((e,))
	
	text.insert('end',e)
	text.grid(row=2,column=1,rowspan=20,columnspan=20)

	if not initial_money.get().isnumeric():
		initial_money.delete(0,'end')
		initial_money.insert(0,record._inital_money)
	#add new data to records
	record._inital_money=int(initial_money.get())
	record._records.append(e2)
	record._records.append(e3)
	record._records.append(e4)
	record._records.append(e5)

	status=tkinter.Label(window,text=f'Now you have {Sumup(record._records)+int(initial_money.get()):5} dollars.  ' )
	status.grid(row=1,column=25)
	
	# datetime.insert(0,str(date.today()))
	datetime.delete(0,'end') #輸入後 自動清除輸入欄
	datetime.insert(0,str(date.today()))

	category.delete(0,'end')
	category.insert(0,'expense')

	Description.delete(0,'end')
	Description.insert(0,'(Optional)')
	Price.delete(0,'end')

def setInitMoney(*event):
	if not initial_money.get().isnumeric():
		initial_money.delete(0,'end')
		initial_money.insert(0,record._inital_money)
	record._inital_money=int(initial_money.get())
	status=tkinter.Label(window,text=f'Now you have {Sumup(record._records)+int(initial_money.get()):5} dollars.  ')
	status.grid(row=1,column=25)
def Delete():
	if text.curselection()==():    #null tuple
		return
	for i in range(0,len(record._records),4):

		t=' '.join((record._records[i],record._records[i+1],record._records[i+2],str(record._records[i+3])))

		if t==text.get(text.curselection()):
			record._records.pop(i+3)
			record._records.pop(i+2)
			record._records.pop(i+1)
			record._records.pop(i)
			text.delete(text.curselection())
			status=tkinter.Label(window,text=f'Now you have {Sumup(record._records)+int(initial_money.get()):5} dollars.  ')
			status.grid(row=1,column=25)
			break
		# if i+4==len(record._records):
		# 	return
	
	'''
	value=eval(text.get(text.curselection()))
	ind=R.index(value)
	print(ind)
	'''
def saverecord():
#	record.ad(R)
	record.save()
def on_closing():
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		saverecord()
		window.destroy()

def printRecord(Record,init="0"):
	if Record!=None:
		for i in range(0,len(Record),4):
			e2=Record[i]
			e3=Record[i+1]
			e4=Record[i+2]
			e5=Record[i+3]
			e=e2+' '+e3+' '+ e4+' '+ e5
			text.insert('end',e)#以上為導入listbox紀錄
		status=tkinter.Label(window,text=f'Now you have {Sumup(Record)+int(init):5} dollars.  ' )
		#以上為算出紀錄總金額
		status.grid(row=1,column=25)
	else:
		status=tkinter.Label(window,text=f'Now you have no money.' )
		status.grid(row=1,column=25)

def Reset():
	text.delete(0,'end')
	printRecord(record._records,record._inital_money)
	find_data.delete(0,'end')

def search(*event): # *event -> optional argument
	target = find_data.get()
	target_categories=categories.find_subcategories(target)
	#this is essential, for there may be more than 1 subcategories.
	dataFind=record.find(target_categories)
	
	if dataFind==[]:
		Reset()
		tkinter.messagebox.showerror(title="error", message='''The category you searhed isn't exist!''')
		return
	
	text.delete(0,'end')
	printRecord(dataFind)

printRecord(record._records,record._inital_money)
text.grid(row=2,column=1,rowspan=20,columnspan=20)

F=tkinter.Label(window,text='Find categories')
F.grid(row=1,column=1,rowspan=2,columnspan=9)

find=tkinter.Button(window,text='search',command=search)#no command so far！！！
find.grid(row=1,column=11)

find_data=tkinter.Entry(window)
find_data.bind("<Return>",search)
find_data.grid(row=1,column=10,rowspan=1,columnspan=1)

reset=tkinter.Button(window,text='Reset',command=Reset)#no command！！！
reset.grid(row=1,column=12)

init_label=tkinter.Label(window,text='Initial money')
init_label.grid(row=3,column=24,sticky=tkinter.E)

date_label=tkinter.Label(window,text='Date')
date_label.grid(row=4,column=24,sticky=tkinter.E)

datetime=tkinter.Entry(window)
datetime.insert(0,str(date.today()))
datetime.grid(row=4,column=25)

cate_label=tkinter.Label(window,text='Category')
cate_label.grid(row=5,column=24,sticky=tkinter.E)

category=ttk.Combobox(window,width=19)#Combobox
category.grid(row=5,column=25,sticky=tkinter.E)
category["value"]=['expense','---food','------meal','------snack','------drink','---transportation','------bus','------railway','income','---salary','---bonus']

flat_category=['expense','food','meal',' snack','drink','transportation','bus','railway','income','salary','bonus']
category.current(0)

desc_label=tkinter.Label(window,text='Description')
desc_label.grid(row=6,column=24,sticky=tkinter.E)

price_label=tkinter.Label(window,text='Price')
price_label.grid(row=7,column=24,sticky=tkinter.E)

def KK(*event):
	Description.delete(0,'end')

Description=tkinter.Entry(window)
Description.insert(0,'(Optional)')
Description.bind('<Button-1>',KK)
Description.grid(row=6,column=25)

Price=tkinter.Entry(window)
Price.bind("<Return>",setrecord)
Price.grid(row=7,column=25)

initial_money=tkinter.Entry(window) #Initial money entry
initial_money.insert(0,record._inital_money)
initial_money.bind("<Return>",setInitMoney)
initial_money.grid(row=3,column=25)

add_record=tkinter.Button(window,text='Add a record',command=setrecord)
add_record.grid(row=8,column=25)

update=tkinter.Button(window,text='Update',command=setInitMoney)
update.grid(row=3,column=26)

delete=tkinter.Button(window,text='Delete',command=Delete)
delete.grid(row=22,column=10)

window.protocol("WM_DELETE_WINDOW",on_closing)
window.mainloop()


# import sys
# import ast
# import tkinter
# from tkinter import ttk
# from pyrecord import *
# from pycategory import *

# categories = Categories()


# records=Records()
# with open('records.txt','a') as fh:
#     while True:
#         order=input('''What do you want to do?\n(add / view / delete / \
# view categories / find / exit)\n''')

#         if order=='add':
#             record = input('Add an expense or income record with date (optional),category,\
# description, and price (separate by spaces):\n')
#             records.add(record)
#         elif order=='view':
#             records.view()
#         elif order=='delete':
#             delete_record=input("Which record do you want to delete? ")
#             records.delete(delete_record)
#         elif order=='view categories':
#             categories.view()
#         elif order=='find':
#             category = input('Which category do you want to find? ')
#             target_categories=categories.find_subcategories(category)
#             #this is essential, for there may be more than 1 subcategories.
#             records.find(target_categories)
#         elif order=='exit':
#             records.save()
#             break
#         else:
#             sys.stderr.write('Invalid command. Try again.\n')

