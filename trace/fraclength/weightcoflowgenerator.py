#encoding:utf-8

import random
import math
import numpy

TOTAL=200
RACKS=50
ARRIVALMAX=1000000
MAXWEIGHT=4

def fillArray(rack):
	length=len(rack)
	for i in range(0,length):
		rack[i]=0
	return rack

def selectMachine(rack):
	while True:
		machine=random.randint(0, RACKS-1)
		if rack[machine]==0:
			rack[machine]=1
			return rack,machine

def selectMachineN(rack,racknumber):
	while True:
		machine=random.randint(0, racknumber-1)
		if rack[machine]==0:
			rack[machine]=1
			return rack,machine



def generateFactor(file,mid,short):
	handler=open(file,"a+")
	jobs=[]
	sumjob=0

    
	jobshort=(int)((float)(short*TOTAL)/100.0)
	joblarge=TOTAL-jobshort
	handler.write(str(RACKS)+" "+str(TOTAL)+"\n")
	
	
	for i in range(0,TOTAL):
		print i
		jobname=str(i)+" "
		handler.write(jobname)
		
		#generate weight and arrival time
		weight=random.randint(1, MAXWEIGHT)
		arrivaltime=random.randint(0,ARRIVALMAX)
		handler.write(str(weight)+" ")
		handler.write(str(arrivaltime)+" ")

		#generate mapper, in this section, the number of mapper is fixed
		numMappers=random.randint(1,RACKS-1)
		handler.write(str(numMappers)+" ")
		rack=[0 for x in range (0,RACKS)]
		rack=fillArray(rack)
		
		for j in range(0,numMappers):
			rack,machine=selectMachine(rack)
			handler.write(str(machine)+" ")
		#generate reduce

		numReducers=random.randint(1,RACKS-1)
		handler.write(str(numReducers)+" ")
		rack=[0 for x in range (0,RACKS)]
		rack=fillArray(rack)

		for j in range(0,numReducers):
			if i < jobshort:
				numMB=random.randint(10,mid)
			else:
				numMB=random.randint(mid,1000)
			shuffleBytes = numMB * numMappers
			rack,reduceid=selectMachine(rack)
			handler.write(str(reduceid)+":"+str(shuffleBytes)+" ")
		handler.write("\n")






if __name__ == "__main__":

	i=5
	while i <=95:
		filename=str(i)+".tr"
		generateFactor(filename,300,i)
		i+=5
