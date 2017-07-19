import Queue
import select
import socket
import sys
import random
from ChatRoomHandler import ChatRoomHandler
from Client import Client
from threading import Thread
from time import gmtime, strftime

# Loops, listening for new IMClients wanting to enter a ChatRoom
# Keep a list of Client objects for each IMClient and a list for existing ChatRooms

class IMServer:

	def __init__(self):
		# TODO REVIEW THIS
		# I changed this into a dict so that it could be something like this general:General's Chatroom Object
		# ToDo: Delete when sure it unnecessary
		# self.chatRooms = {}
		self.clientAdjectivesList = open('Adjectives.txt').read().splitlines()
		self.clientNounsList = open('Nouns.txt').read().splitlines()
		self.connectedClients = []
		self.HOST = ''
		self.PORT = 12345

		# Create the socket and make sure to make it reusable and non-blocking
		# AF_INET is IPv4 and IIRC SOCK_STREAM is TCP
		self.base = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Make it so that sockets can be reused
		self.base.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# We don't want it blocking
		self.base.setblocking(0)

		# Bind the socket
		self.bind(self.base, self.HOST, self.PORT)

		self.base.listen(5)

		# inputs is what's coming into our program
		self.inputs = [self.base]
		self.outputs = []
		# Each connection gets its own message queue
		# self.message_queues = {}
		# ToDo: Delete when sure it unnecessary
		# self.createDefaultChatRooms()
		self.chatRoomHandler = ChatRoomHandler()
		self.startLoop()
		return


	# ToDo: Delete when sure it unnecessary	
	# TODO this is a new function
	# def createDefaultChatRooms(self):
	# 	self.chatRooms["General"] = ChatRoom("General")
	# 	self.chatRooms["Random"] = ChatRoom("Random")


	# ToDo: Delete when sure it unnecessary
	# # Add support for custom chatrooms
	# def createChatRoom(self, roomName):
	# 	# general = ChatRoom("General")
	# 	# self.chatRooms.append(general)
	# 	# random = ChatRoom("Random")
	# 	# self.chatRooms.append(random)

	# 	raise NotImplementedError

	def startLoop(self):
		# threading._start_new_thread(self.listenForConnections())
		Thread(target=self.listenForConnections).start()

	def listenForConnections(self):
		while self.inputs:
			# Select monitors inputs and puts them into three categories
			readable, writable, errors = select.select(self.inputs, self.outputs, self.inputs)

			for sock in readable:
				# The base socket has to keep listening for things that want to connect
				if sock is self.base:
					# accept the connection
					conn, addr = sock.accept()
					conn.setblocking(0)
					self.addNewClient(conn, addr, "General")
		return

	# This was changed from clientName, clientIP and clientPort
	def addNewClient(self, sock, addr, roomName):
		clientName = random.choice(self.clientAdjectivesList)+" "+random.choice(self.clientNounsList)
		client = Client(sock, addr, None, self.chatRoomHandler, clientName)
		# ToDo: Delete when sure it unnecessary
		# self.chatRooms["General"].newClient(client)
		chatRoomObj = self.chatRoomHandler.addClient(roomName, client)
		client.chatroom = chatRoomObj
		return 

	@staticmethod
	def bind(sock, host, port):
		try:
			sock.bind((host, port))
		except socket.error, msg:
			print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

if __name__ == "__main__":
	IMServer()
