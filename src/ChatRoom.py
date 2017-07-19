# newMessage() is called by a Client object when a new message is received from its associated IMClient
# updateConnected() will broadcast messages stored inside the messageQueue to the list of
# connectedClients when a new entry in ther queue is detected

from Client import Client
from Queue import Queue
from threading import Thread
import os
import time


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
		""" TODO lock thread till the following messages are sent to the client. 
		    TODO Fix spacing of output"""
		newClient.sendMessageUpdateToIMClient("Welcome to " + self.name + " \n")
		newClient.sendMessageUpdateToIMClient("Your username is " + newClient.name + "\n")
		newClient.sendMessageUpdateToIMClient("There are currently " + str(len(self.clientsConnected)) + " users connected")
		# if len(self.clientsConnected) > 1:

		# else:
		# 	newClient.sendMessageUpdateToIMClient("You are the first user in this chatroom \n")

	def listUsers(self, client):
		client.sendMessageUpdateToIMClient("The following users are also connected: \n")
		for c in self.clientsConnected:
			if c is not client:
				client.sendMessageUpdateToIMClient(c.name + "\n" )

	def removeClient(self, newClient):
		if newClient in self.clientsConnected:
			self.clientsConnected.remove(newClient)

	def updateConnectedClients(self, messageIn):
		# loop through all clients updating them
		for client in self.clientsConnected:
			client.sendMessageUpdateToIMClient(messageIn)

	def startLoop(self):
		''' Is called once ChatRoom is initted '''
		queueHandler = Thread(target=self.mainLoop, args=()).start()
		return

	def mainLoop(self):
		# get is blocking by default (yay)
		while self.chatRoomRunning:
			messToBroadcast = self.messageQueue.get()
			self.updateConnectedClients(messToBroadcast)
		return
