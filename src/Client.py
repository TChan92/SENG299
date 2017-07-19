import ChatRoom
import select
# import threading
from threading import Thread
from time import gmtime, strftime

# One-to-one relationship with IMClients
# Constantly listening for new messages broadcast by the IMClient
# 	Calls its writeMessageToChatRoom() function when a new message is received
# 	writeMessage() calls the ChatRoom.newMessage() function
class Client:

	def __init__(self, sock, addr, room, chatRoomHandler, name):

		self.sock = sock
		self.addr = addr
		self.chatroom = room # I dont know if this is entirely valid
		self.name = name
		self.chatRoomHandler = chatRoomHandler
		self.startLoop()
		self.helpMessage = "/help - will provide the possible command | /switch chatroomName - switch to given chatroomName | Chat Rooms Available : General and Random"

	# TODO Changed name of this as well
	def listenForMessageFromIMClient(self):
		while True:
			receive = select.select([self.sock], [], [])
			message = self.sock.recv(4096)
			# This occurs when the client shutsdown unexpectedly
			if len(message) is 0:
				self.chatroom.removeClient(self)
				return
			Thread(target=self.writeMessageToChatRoom, args=(message,)).start()

	def startLoop(self):
		queueHandler = Thread(target=self.listenForMessageFromIMClient, args=()).start()

	# TODO I updated the name of this to be clearer
	def writeMessageToChatRoom(self, messageIn):
		newMessage = ""
		# TODO Make this clearer with a switch statement
		if self.specialMessage(messageIn):
			if self.userJoining(messageIn):
				newMessage = self.name + self.ignoreFirstWord(messageIn)
			elif self.switchCommand(messageIn):
				chat = messageIn.split(" ")[1]
				if self.chatRoomHandler.findChatRoom(chat).name == chat:
					self.changeChatRoom(chat)
			elif self.helpCommand(messageIn):
				self.sendMessageUpdateToIMClient(self.helpMessage)
			# send user help specs
			elif self.serverShutdown(messageIn):
				self.chatRoomHandler.shutdownClients()
			elif self.requestingUsers(messageIn):
				self.chatroom.listUsers(self)
			elif self.exitMessage(messageIn):
				self.shutdown()
				self.chatroom.removeClient(self)
				return
			elif self.abortMessage(messageIn):
				self.chatRoomHandler.shuttingDown = False

			# Default
			else:
				self.sendMessageUpdateToIMClient("Sorry your command wasn't recognized")
		else:
			newMessage = self.name + " : " + messageIn
			self.chatroom.messageQueue.put(newMessage)
			print "(%s) %s" % (self.chatroom.name, newMessage)

	# TODO I updated the name of this as well and it doesn't return anything as well
	def sendMessageUpdateToIMClient(self, newMessage):
		self.sock.send(newMessage)

	# TODO This is new
	def shutdown(self):
		self.sendMessageUpdateToIMClient("/exit")

	def changeChatRoom(self, newRoomName):
		newRoom = self.chatRoomHandler.changeChatRoom(newRoomName, self.chatroom.name, self)
		self.chatroom = newRoom
		return

	def serverShutdown(self, message):
		if message.split(' ', 1)[0] == "/servershutdown" or message.split(' ', 1)[0] == "/shutdownserver":
			return True
		return False

	def specialMessage(self, message):
		if message[0] is '/':
			return True

	def ignoreFirstWord(self, message):
		return message.split(' ', 1)[1]

	def switchCommand(self, message):
		if message.split(" ")[0] == "/switch":
			return True

	def helpCommand(self, message):
		if message.split(" ")[0] == "/help":
			return True

	def userJoining(self, message):
		if message.split(" ")[0] == "/announce":
			return True

	def requestingUsers(self, message):
		if message.split(" ")[0] == "/users":
			return True

	def exitMessage(selfs, message):
		if message.split(" ")[0] == "/exit":
			return True

	def abortMessage(selfs, message):
		if message.split(" ")[0] == "/a":
			return True
