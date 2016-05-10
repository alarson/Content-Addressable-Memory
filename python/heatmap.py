#This script just makes a heatmap from a 2D python list
#Class page: http://www.cems.uvm.edu/~rsnapp/teaching/cs256/index.html
#Ari Larson
#5/8/2016

import sys, getopt
import pickle
import matplotlib.pyplot as plt
import math

def main(argv):
	filename = argv[0]+'.pickle'
	filename2 = argv[1]+'.pickle'
	with open(filename, 'rb') as handle:
		to_graph = pickle.load(handle)

	with open(filename2, 'rb') as handle:
		second = pickle.load(handle)

	to_graph.reverse()
	second.reverse()
	fig, ax = plt.subplots()

		#and graph the expected relationship
	x = ([n for n in range(2,225)])  
	y = []
	for i in x:
		y.append(meliece_expected(i))
	ax.plot(x, y)  
	print x
	print y
	for i in range(len(to_graph)):
		for j in range(len(to_graph[i])):
			to_graph[i][j]+=second[i][j]

	plt.title("Partition Location over time, E5",fontsize=20)
	
	
	# plt.imshow(to_graph, cmap=plt.cm.gray,interpolation='nearest', extent=[0,25,0,125], aspect = 25/225.0)

	# We need to draw the canvas, otherwise the labels won't be positioned and 
	# won't have values yet.
	fig.canvas.draw()
	plt.ylabel('m')
	plt.xlabel('n')
	plt.title('r in vanilla networks')
	ax.set_yticklabels([n for n in range(0,30,4)])
	ax.set_xticklabels([m for m in range(0,250,50)])


	# plt.show()
	plt.savefig('r_perf_25.png')


def meliece_expected(x):
	return x/(4*math.log(x))
if __name__ == "__main__":
   main(sys.argv[1:])