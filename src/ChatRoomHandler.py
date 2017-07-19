from ChatRoom import ChatRoom
import os
import time

class ChatRoomHandler(object):

	def __init__(self):	
		self.chatRoomList = []
		self.shuttingDown = False
		self.initChatRooms()

	def initChatRooms(self):
		self.createChatRoom("General")
		self.createChatRoom("Random")	
		return

	def addClient(self, roomName, clientObj):
		''' Returns the ChatRoom obj so the Client can keep reference to it '''
		room = self.findChatRoom(roomName)
		room.newClient(clientObj)
		return room

	def removeClient(self, roomName, clientObj):
		room = self.findChatRoom(roomName)
		room.removeClient(clientObj)		
		return

	def createChatRoom(self, roomName):
		# Avoid duplicates
		for room in self.chatRoomList:
			if room.name == roomName:
				return
		tempRoom = ChatRoom(roomName)
		self.chatRoomList.append(tempRoom)
		return

	def findChatRoom(self, roomName):
		for room in self.chatRoomList:
			if room.name == roomName:
				return room
		print "ChatRoomHandler: unable to find specified ChatRoom", roomName
		return None

	def changeChatRoom(self, newRoomName, oldRoomName, clientObj):
		self.removeClient(oldRoomName, clientObj)
		room = self.addClient(newRoomName, clientObj)
		return room

	def shutdownClients(self):
		self.shuttingDown = True
		for chatroom in self.chatRoomList:
			chatroom.messageQueue.put("Server shutting down")
		for i in xrange(10, 0, -1):
			for chatroom in self.chatRoomList:
				chatroom.messageQueue.put(str(i) + "...")
			if self.shuttingDown == False:
				for chatroom in self.chatRoomList:
					chatroom.messageQueue.put("Server shutdown has been cancelled")
				return
			time.sleep(1)
		for chatroom in self.chatRoomList:
			for client in chatroom.clientsConnected:
				client.shutdown()
				# Thread(target=client.shutdown()).start
		os._exit(0)  # This doesn't work currently,
