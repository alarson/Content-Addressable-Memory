#First attempt at use case of addressable memory using hopfield networks
#Class page: http://www.cems.uvm.edu/~rsnapp/teaching/cs256/index.html
#Ari Larson
#4/12/2016
import network
def main():
	a = network.Hopfield_Network(10)
	a.store([1,1,1,1,1,1,1,1,1,1])
	a.store([-1,-1,-1,-1,-1,1,1,1,1,1])
	
	a.retrieve_asynch([-1,-1,-1,1,-1,1,1,1,1,1],5)
main()