# newMessage() is called by a Client object when a new message is received from its associated IMClient
# updateConnected() will broadcast messages stored inside the messageQueue to the list of
# connectedClients when a new entry in ther queue is detected

from Client import Client
from Queue import Queue
import threading


class ChatRoom:

	def __init__(self, name):
		self.chatRoomRunning = True
		self.name = name
		self.clientsConnected = []
		self.messageQueue = Queue()
		self.startLoop()

	def newClient(self, newClient):
		''' called by IMServer, newClient is of type Client '''
		self.clientsConnected.append(newClient)
		newClient.sendMessageUpdateToIMClient("Welcome to " + self.name)

	def removeClient(self, newClient):
		if newClient in self.clientsConnected:
			self.clientsConnected.remove(newClient)
		
	def updateConnectedClients(self, messageIn):
		# loop through all clients updating them
		for client in self.clientsConnected:
			client.sendMessageUpdateToIMClient(messageIn)

	def startLoop(self):
		''' Is called once ChatRoom is initted '''
		queueHandler = threading._start_new_thread(self.mainLoop, ())
		return

	def mainLoop(self):
		# get is blocking by default (yay)
		while self.chatRoomRunning:
			messToBroadcast = self.messageQueue.get()
			self.updateConnectedClients(messToBroadcast)
		return 