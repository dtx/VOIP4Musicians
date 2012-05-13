from calls import *
class Command:
	# This is the abstract class command.
	def __init__(self):
		pass

	def execute(self):
		pass

class initialise(Command):
	# This is the class to initialize the user.
	def __init__(self, username, password, skill, genre):
		self.username = username
		self.password = password
		self.skill = skill
		self.genre = genre

	# Execute returns an instance of the class MakeACall
	def execute(self):
		makeCall = MakeACall(self.username, self.password, self.skill, self.genre)
		return makeCall

class authenticateUser(Command):
	# This is the class to authenicate the credentials given.	
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self):
		self.makeCall.authenticate()

class makePhoneCall(Command):
	# This is a class to make a phone call
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self, input):
		self.makeCall.make(input)

class hangupPhoneCall(Command):
	# The class to hand up the current phone call
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self):
		self.makeCall.hangup()

class answerPhoneCall(Command):
	# The class to answer an incoming call
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self):
		self.makeCall.answer()

class quitApp(Command):
	# This is the call to quit the Application
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self):
		self.makeCall.quit()


class findPeople(Command):
	# This is the class to find the people who are online with 
	# your preferences
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self):
		return self.makeCall.getOnlinePeople()


class initiateCall(Command):
	# The class the setup the initial calling mechanism
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self):
		self.makeCall.initiateCall()

class waitForVar(Command):
	# This is a class to wait for a given variable
	def __init__(self, makeCall):
		self.makeCall = makeCall

	def execute(self):
		return changeVariable()	
