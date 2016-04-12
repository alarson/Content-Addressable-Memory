#First attempt at addressable memory using hopfield networks
#Class page: http://www.cems.uvm.edu/~rsnapp/teaching/cs256/index.html
#Ari Larson
#4/12/2016

import numpy as np
import random as rand
class Hopfield_Network(object):
	'''
	Meant to serve as a model of the hopefield associative memory
	'''

	def __init__(self, n):
		'''
		The network should be initialized with desired dimensions, equal to the dimensions 
		of the units stored and retrieved
		'''
		self.n = n
		self.weights = np.matrix([np.zeros(n)]*n)
		
		self.memories = []
		self.num_memories = 0

		self.state_vector = np.zeros(n)

	def __str__(self):
		return str(self.weights)

	def store(self, memory):
		'''
		The passed memory vector is added to the set of stored matrices, and the network weights are re-calculated.
		'''
		self.memories.append(np.matrix(memory))
		self.num_memories += 1
		#self.sum_outer_products() inefficient
		self.weights += np.transpose(np.matrix(memory))*np.matrix(memory) - np.identity(self.n)

	def remove(self, memory):
		'''
		The passed memory vector is removed from the set of stored matrices, and the network weights are re-calculated. If
		the passed vector does not exist in the set of stored values, then a warning is raised and no change is made to the network weights.
		'''
		if(memory in self.memories):
			self.memories.remove(memory)
			self.num_memories -= 1
			self.sum_outer_products()
		else:
			print "Attempted to remove memory, not present in weight matrix"

	def sum_outer_products(self):
		'''
		For re-calculating network weights when set of recorded memories changes
		'''
		if(self.memories): #nonempty
			self.weights = np.zeros((self.n,self.n))
			for memory in self.memories:
				outer_product =np.transpose(memory)*memory - np.identity(self.n)
				self.weights+=outer_product
				print outer_product
		else:
			print "attempted to sum outer products of unpopulated memory set"

	def retrieve(self, probe):
		'''
		The passed (generally perturbed) memory is used to initialize the state of the network, and should be a mildly permuted version of the memory
		that should be retrieved. This function then starts the update() cycle, and ends when the network reaches a stable state.
		The network will not fall into a periodic or chaotic attractor thanks to the entropy rules as described and demonstrated by
		Dr. Snapp in the class notes: http://www.cems.uvm.edu/~rsnapp/teaching/cs256/index.html
		'''
		self.state_vector = probe
		for i in range(10):
			self.update_asynch()
		print self.state_vector

	def update_asynch(self):
		'''
		One timestep in the network update process, when the network is updated asynchronously.
		In the asycnhronous scheme, a node is selected for update at random.
		'''
		#select random node for update
		node = rand.randint(0,self.n-1)

		#sum inputs, and take the sign of the resulting integer
		node_sum = (np.transpose(self.weights[node])*self.state_vector).sum()
		node_sign = node_sum/abs(node_sum)

		#update
		self.state_vector[node]=node_sign

	def update_synch(self):
		'''
		One timestep in the network update process, when the network is updated synchronously
		'''
		#for index in network_state:
