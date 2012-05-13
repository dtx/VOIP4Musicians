import sys
import pjsua as pj
import MySQLdb as sql

LOG_LEVEL=2
current_call = None
lib=None
acc = None
waitVar = 0
# Logging callback
def log_cb(level, str, len):
    print str,

# Callback to receive events from account
class MyAccountCallback(pj.AccountCallback):
	def __init__(self, account=None):
		pj.AccountCallback.__init__(self, account)

	# Notification on incoming call
	def on_incoming_call(self, call):
        	global current_call
		global waitVar
        	if current_call:
            		call.answer(486, "Busy")
            		return
        	print "Incoming call from ", call.info().remote_uri
        	print "Press 'a' to answer"
        	current_call = call
        	call_cb = MyCallCallback(current_call)
        	current_call.set_callback(call_cb)
        	current_call.answer(180)

	
        
# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):

	def __init__(self, call=None):
        	pj.CallCallback.__init__(self, call)

    	# Notification when call state has changed
    	def on_state(self):
        	global current_call
		global waitVar
        	print "Call with", self.call.info().remote_uri,
        	print "is", self.call.info().state_text,
        	print "last code =", self.call.info().last_code, 
        	print "(" + self.call.info().last_reason + ")"
		if(self.call.info().last_code == 180):
			waitVar = 1
        	if self.call.info().state == pj.CallState.DISCONNECTED:
            		current_call = None
            		waitVar = 0
            	print 'Current call is', current_call

    	# Notification when call's media state has changed.
	def on_media_state(self):
        	if self.call.info().media_state == pj.MediaState.ACTIVE:
            	# Connect the call to sound device
            		call_slot = self.call.info().conf_slot
            		pj.Lib.instance().conf_connect(call_slot, 0)
          		pj.Lib.instance().conf_connect(0, call_slot)
            		print "Media is now active"
        	else:
            		print "Media is inactive"

#This is the method called by the view of the gui to check if the 
# call state has changed
def changeVariable():
	global waitVar
	if(waitVar == 1):
		return 1
	else: 
		return 0
	
# Function to make call
def make_call(uri):
	global acc
    	try:
        	print "Making call to", uri
        	return acc.make_call(uri, cb=MyCallCallback())
    	except pj.Error, e:
        	print "Exception: " + str(e)
        	return None
        
class MakeACall:

	# Create library instance and connect to database to let other people know 
	# that you are online
	def __init__(self, uname, passw, skill, genre):
		self.username = uname
		self.password = passw
		self.transport = None
		self.skill = skill
		self.genre = genre
		self.conn = sql.connect(host = "128.174.252.75",
				   port = 3306,
				   user = "vempati1_adm",
				   passwd = "123987",
				   db = "vempati1_musicUsers")
		self.cursor = self.conn.cursor()

	def authenticate(self):
		# Create local account
		global current_call
		global acc
		global lib
		acc_cfg = pj.AccountConfig()
		id = "sip:" + self.username + "@iptel.org"
		print id
		acc_cfg.id = id
		acc_cfg.reg_uri = "sip:iptel.org"
		acc_cfg.auth_cred = [pj.AuthCred("iptel.org", self.username, self.password)]
		acc = lib.create_account(acc_cfg, cb=MyAccountCallback())
		current_call = None
		self.cursor.execute("INSERT INTO users (username, skill, genre) VALUES (%s, %s, %s)", (id, self.skill, self.genre))

	def make(self, input):
		global current_call
		global lib
		global acc
		if current_call:
			print "Already have another call"
			return
		print "Enter destination URI to call: ", 
		lck = lib.auto_lock()
		current_call = make_call(input)
		del lck
	
	def hangup(self):
		global current_call
		if not current_call:
			print "There is no call"
			return
		current_call.hangup()
	
	def answer(self):
		global current_call
		if not current_call:
			print "There is no call"
			return
		current_call.answer(200)

	def quit(self):
		global acc
		global lib
		# Shutdown the library
		self.cursor.execute("DELETE FROM users WHERE username = (%s)", ("sip:"+self.username+"@iptel.org"))
		self.cursor.close()
		self.conn.commit()
		self.conn.close()
		acc.delete()
		acc = None
		lib.destroy()
		lib = None

	# The function to find who all are online for the user to call. 
	def getOnlinePeople(self):
		global acc
		peopleArray = []
		print "In online people"
		self.cursor.execute("SELECT * FROM users WHERE username != (%s) AND skill = (%s) AND genre = (%s)", ("sip:"+self.username+"@iptel.org", self.skill, self.genre))
		row = self.cursor.fetchall ()
		for x in row:
			peopleArray.append(x[0])
		return peopleArray
	
	def initiateCall(self):
		print "here"
		global lib
		global acc
		lib = pj.Lib()

		try:
			my_ua_cfg = pj.UAConfig()
			my_ua_cfg.stun_host = "stun.faktortel.com.au"

			my_media_cfg = pj.MediaConfig()
			my_media_cfg.enable_ice = True 
			# Init library with default config and some customized
			# logging config.
			lib.init(log_cfg = pj.LogConfig(level=LOG_LEVEL, callback=log_cb), media_cfg = my_media_cfg)

			# Create UDP transport which listens to any available port
			self.transport = lib.create_transport(pj.TransportType.UDP, 
			pj.TransportConfig(0))
			print "\nListening on", self.transport.info().host, 
			print "port", self.transport.info().port, "\n"

			# Start the library
			lib.start()
						
			my_sip_uri = "sip:" + self.transport.info().host + ":" + str(self.transport.info().port)

		except pj.Error, e:
			self.cursor.execute("DELETE FROM users WHERE username = %s",(self.username))
			self.cursor.close()
			self.conn.commit()
			self.conn.close()
			print "Exception: " + str(e)
			lib.destroy()
			lib = None
