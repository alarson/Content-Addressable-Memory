#Experimental setup for testing capacity hueristics proposed by papers available in lit section, using differing update / network construction schemes.
#Class page: http://www.cems.uvm.edu/~rsnapp/teaching/cs256/index.html
#Ari Larson
#5/8/2016
import network
import numpy as np
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def main():
	#How many simulations (unique nets) should be run:
	sims = 1
	#general parameters
	n=100
	num_overlap_levels = 5

	if(n<num_overlap_levels):
		print "Be better."
		exit()

	num_trials=1
	time_limit = 20
	r = .025 #r is the ratio of memories to neurons m:n

	synch=True #if false, use async update scheme.
	part_reverse=True;
	tolerance = 0.025 #ratio of bits that can be incorrect allowing the network to be considered correct
	num_tol=int(tolerance*n)
	print num_tol

	for r in range(25,275,25):
		r*=0.001
		#Here we run the simulation sims times
		tally=[]
		tally,tally_total,tally_perfect,tally_25,tally_5 = (simulate(n,num_overlap_levels,num_trials,time_limit,r,synch,part_reverse,num_tol))
		tally_total=0
		tally_perfect=0
		for i in range(sims-1):
			new,tot,perf,t25,t5 = (simulate(n,num_overlap_levels,num_trials,time_limit,r,synch,part_reverse,num_tol))

			tally_total+=tot
			tally_perfect+=perf
			tally_25+=t25
			tally_5+=t5
			#runs contains a tally, we update it using new

			for j in range(len(tally)):
				tally[j]= [sum(x) for x in zip(tally[j], new[j])]
			# print "run "+str(i+1)+" complete."
		
		#we normalize runs back down from tally to average
		for i in range(len(tally)):
			for j in range(len(tally[i])):
				tally[i][j]= tally[i][j]/sims

		print "r = "+str(r)+", total end states evaluated: "+str(tally_total)
		print "total perfect end states:"+str(tally_perfect)+"\n"
		print "total end states within 0.0025 error:"+str(tally_25)+"\n"
		print "total end states within 0.05 error:"+str(tally_5)+"\n"
		graph(tally,n,r)

def simulate(n,num_overlap_levels,num_trials,time_limit,r,synch,part_reverse,tolerance):
	'''
	For one simulation, a single nxn network is generated. Each index of the o_levels list contains itself a list of length num_trials. Each index of this list contains a 
	single "trial", which is a list corresponding to the overlap values over time when the network is exposed to a randomized permutation of the target memory, with the appropriate
	overlap level as dictated by its location in the o_levels list. Cool.
	'''
	
	p_references = np.arange(n/2, n+1, n/num_overlap_levels) #just for keeping track of which indexes of o_levels are for which overlap percentages
	#o_levels is a list. Each index has a set of trials conducted for that initial overlap level, which is a "trials" list. Each trials list contains time-series lists
	#containing integers corresponding to how many indexes of the memory are correct.
	o_levels=[]
	#the list of memories that this net stores
	memories = []

	#first we generate the experimental network, at the appropriate r ratio of m:n
	m = int(r*n)
	net = network.Hopfield_Network(n)
	for i in range(m):
		memories.append(generate_memory(n))
		net.store(memories[i])
	print compare(memories[0],memories[1])
	net.normalize_net()
	#now, we run trials on this network.
	tally_perfect=0
	total=0
	t25=0
	t5=0
	for p in p_references:
		trials= []
		for trial in range(num_trials):
			# print p
			#run trial
			mem = memories[random.choice(range(m))]
			# print compare(permute(mem,p),mem)
			if(part_reverse):
				states = net.retrieve_partial_reverse(permute(mem,p),time_limit,r)
			else:
				if(synch):
					states = net.retrieve_synch(permute(mem,p),time_limit)
				else:
					states = net.retrieve_asynch(permute(mem,p),time_limit)
			#compare to original memory at each timestep
			overlaps = []
			for t in range(len(states)):
				comparison = compare(states[t], mem)
				overlaps.append(comparison)
				if(n-comparison==0):
					tally_perfect+=1
				elif(n-comparison<tolerance):
					t25+=1
				elif(n-comparison<2*tolerance):
					t5+=1
				total+=1
				
			#store resulting overlap time-series
			trials.append(overlaps[:])
			# print "tally perfect: "+str(tally_perfect)
		#we could store all trials:
		# o_levels.append(trials[:])
		#but that's unnecessary detail for my purposes, so I'll just store averages:
		# print len(trials)
		o_levels.append(average(trials))

	return (o_levels,total,tally_perfect,t25,t5)

def graph(series,n,param):
	fig, ax = plt.subplots()
	ax.margins(0.04)


	for s in series:
		wrongness=n-s[len(s)-1]
		if(wrongness<float(n)/10):
			ax.plot(s,'.g-')
		elif(wrongness>(float(n)/10)*9):
			ax.plot(s,'.r-')
		else:
			ax.plot(s,'.y-')
	plt.ylabel('Overlap (p)')
	plt.xlabel('Time (t)')
	plt.title("Time courses for overlap")
	# plt.figure(facecolor="white")
	fig1 = plt.gcf()
	fig1.savefig('r_'+str(param)+'.png')
	# plt.show()

def compare(ar1,ar2):
	'''
	returns overlap for two memories
	'''
	return len([i for i, j in zip(ar1, ar2) if i == j])

def average(ar1):
	'''
	One would think numpy would have this covered but noooo...
	'''
	return [sum(col) / float(len(col)) for col in zip(*ar1)]

def permute(original,num_permutes):
	'''
	generates propabilistic permutations of the original memory.
	'''
	copy=original[:]
	indexes = random.sample(range(0, len(original)), num_permutes)
	for i in indexes:
		copy[i]*=-1
	return copy
def generate_memory(n):
	'''
	just generates a list of length n populated with +/- 1, uniformly distributed
	'''
	return [x if x == 1 else -1 for x in np.random.randint(2, size=n)]

main()