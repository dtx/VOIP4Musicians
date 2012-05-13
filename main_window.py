#This program is written as a class. The constructor(the ___init__
#method) is called with a parent widget, to which it adds a
#number of child widgets. The constructor starts by creating a Frame widget.
#A frame is a simple container, and is in this case used to hold the
#button and entry widgets.


from Tkinter import *
from calls import *
import tkMessageBox
import command

# This is a global variable later to be instantiated as a class.
makecall=None

class App:
	def __init__(self,parent):
		#The frame instance is stored in a local variable 'f'.
		#After creating the widget, we immediately call the 
		#pack method to make the frame visible.
		global makecall
		f = Frame(parent)
		f.pack(padx=15,pady=15)
		self.flag = 0
		# self.photoR = parent.PhotoImage(file="phone-iconred.gif")
		# self.photoB = parent.PhotoImage(file="phone-iconblue.gif")
		
		# We then create an entry widget,pack it and then 
		# create three more button widgets as children to the frame.
    
   		self.entry = Entry(f,text="enter your choice")
		self.entry.pack(side= TOP,padx=10,pady=12)
		
		#this time, we pass a number of options to the
		# constructor, as keyword argument.t
        	#All buttons also take a command option. This option 
		#specifies a function, or (as in this
        	#case) a bound method, which will be called when the button is clicked.
		
		self.exit = Button(f, text="Exit", command=f.quit)
		self.exit.pack(side=BOTTOM,padx=10,pady=10)

		self.end = Button(f, text="End", command=self.endCall)
		# self.end.photo = self.photoR
		self.end.pack(side=BOTTOM,padx=10,pady=10)
		
		self.button = Button(f, text="Call",command=self.callEntry)
		# self.button.photo = self.photoB
		self.button.pack(side=BOTTOM,padx=10,pady=10)
		
		#The function .after ensure that corresponding function is after 1 sec.
		self.label = Label(f, text="Connected!!")
		self.label.pack(side=BOTTOM,padx=10,pady=10)
		self.label.after(1000, self.incomingCallHandler)

	# This is a function to let the user know if there is the phone is ringing. 
	# This could be in the case of an incoming call, or an connected outgoing call. 
	def incomingCallHandler(self):

		# Make sure there is an instance of makecall.
		# We define a recursive function to keep calling itself with a regularity of 5 milliseconds. 
		if(makecall == None):
			self.label.after(50, self.incomingCallHandler)
		
		# The variable x acts a flag to check whether there the phone is ringing. 
		# In this case we check the value of waitForVar
		x = (command.waitForVar(makecall)).execute()

		if(x == 1):
			self.label.configure(text = "Phone Ringing!!")
			x = 0
			self.flag = 1
			self.label.after(50, self.incomingCallHandler)

		else:
			if(self.flag != 0):
				self.label.configure(text = "Connected!")
				self.flag = 0
				self.label.after(50, self.incomingCallHandler)
			else:
				self.label.after(50, self.incomingCallHandler)

	# This is the function to either make a new phone to the uri in the box,
	# or answer an incoming phone call. 	
	def callEntry(self):
		
		# Answer incoming phone call.
		if(self.flag != 0):
			(command.answerPhoneCall(makecall)).execute()
	
		# Make a phone call to desired uri.
		else:
			if(self.entry.get().strip() == ""):
				tkMessageBox.showerror("Oops!", "You need to enter an address to call to.")
			else:
				(command.makePhoneCall(makecall)).execute(self.entry.get().strip())

	# This is a function to end an active phone call.		
	def endCall(self):
		(command.hangupPhoneCall(makecall)).execute()


# This is a function to display the people who are online with your preferences.
def showContacts(contactsLabel):
	array = []
	array = (command.findPeople(makecall)).execute()
	str = ""
	for x in array:
		str = str + x + "\n"
	contactsLabel.configure(text = str)
	contactsLabel.after(5000, showContacts, contactsLabel)
	
# The main window, this is responsible for calling all the methods and initializing the classes decribed above.
class mainWindow:
	
	# Create a root for the GUI, and another root for the contacts. 
	def __init__(self,username, password, skill, genre):
		global makecall
		self.root = Tk()
		self.contactsRoot = Tk()
		self.setTitle(self.root, "Make Calls")
		self.app = App(self.root)
		self.setTitle(self.contactsRoot,"Contacts")
		print "-->Initialising the Library"
		makecall=(command.initialise(username, password, skill, genre)).execute()
		print "-->Initiating calling protocol"
		(command.initiateCall(makecall)).execute()
		print "-->Autheticating user"
		(command.authenticateUser(makecall)).execute()
		print "-->Initialising the contacts frame"
		self.showContactFrame(self.contactsRoot)
		print "-->Going into GUI loop"
		self.root.mainloop()
		print "-->Wrapping up everything"
		print "-->Have a good day"
		(command.quitApp(makecall)).execute()
		
	def setTitle(self, root, title):
		root.title(title)

	# This function is called from __init to set of the loop to make sure that the contacts are updating
	def showContactFrame(self,root):
		frame = Frame(root)
		frame.pack(padx=15,pady=15)
		contactsLabel = Label(frame, text = "")
		contactsLabel.pack(side=BOTTOM, padx=10, pady=10)
		contactsLabel.after(5000, showContacts, contactsLabel)

