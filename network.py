#First attempt at addressable memory using hopfield networks
#Class page: http://www.cems.uvm.edu/~rsnapp/teaching/cs256/index.html
#Ari Larson
#4/12/2016

class Hopfield_Network(object):
	'''
	Meant to serve as a model of the hopefield associative memory
	'''

	def __init__(n,m):
		'''
		The network should be initialized with desired dimensions, equal to the dimensions 
		of the units stored and retrieved
		'''

	def store():
		'''
		The passed matrix is added to the set of stored matrices, and the network weights are re-calculated.
		'''

	def remove():
		'''
		The passed matrix is removed from the set of stored matrices, and the network weights are re-calculated. If
		the passed matrix does not exist in the set of stored values, then a warning is raised and no change is made to the network weights.
		'''

	def retrieve():
		'''
		The passed matrix is used to initialize the state of the network, and should be a mildly permuted version of the memory
		that should be retrieved. This function then starts the update() cycle, and ends when the network reaches a stable state.
		The network will not fall into a periodic or chaotic attractor thanks to the entropy rules described and demonstrated by
		Dr. Snapp in the class notes: http://www.cems.uvm.edu/~rsnapp/teaching/cs256/index.html
		'''

	def update_asynch():
		'''
		One timestep in the network update process, when the network is updated asynchronously
		'''

	def update_synch():
		'''
		One timestep in the network update process, when the network is updated synchronously
		'''