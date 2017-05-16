# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import stats

from matplotlib import rcParams
rcParams.update({'font.size': 15,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')

##first read from file
pFabric="pFabric"
Varys="Varys"
Barrat="Barrat"
Yosemite="Yosemite"
Fair="FAIR"

DARK='DARK'

SHORT=20*1024*1024*1024
NARROW=140

up=[0.2,0.1,0.2,0.1,0.3]

def getAverage(arralylist):
	return np.mean(arralylist)


def getRange(arraylist,element):
	return stats.percentileofscore(arraylist, element)



def getElements(arraylist,percentage):
	result=[]
	for element in arraylist:
		pos=getRange(arraylist,element)
		if pos <= percentage:
			result.append(element)
	return result



def getPercentageResult(path,percentage):

	f=open(path,"r")
	totaline=f.readlines()
	wc1=[]
	wc2=[]
	wc3=[]
	wc4=[]
	wc=[]
	for line in totaline:
		if line[0]=='J':
			arrayline=line.split()
			#analyze job 
			jobname=arrayline[0]
			starttime=float(arrayline[1])
			finishtime=float(arrayline[2])
			mappers=int(arrayline[3])
			reducers=int(arrayline[4])
			totalshuffle=float(arrayline[5])
			maxshuffle=float(arrayline[6])
			duration=float(arrayline[7])
			deadlineduration=float(arrayline[8])
			shufflesum=float(arrayline[9])
			weight=float(arrayline[10])
			width=mappers
			if mappers < reducers:
				width=reducers
			else:
				width=mappers

			if maxshuffle < SHORT and width < NARROW:
				wc1.append(weight*duration)
				
			elif maxshuffle >= SHORT and width < NARROW:
				wc2.append(weight*duration)
			elif maxshuffle < SHORT and width > NARROW:
				wc3.append(weight*duration)
			else:
				wc4.append(weight*duration)
				
	#wc=wc1+wc2+wc3+wc4
	f.close()

	wc1add=0
	wc2add=0
	wc3add=0
	wc4add=0
	wcadd=0

	wc1=getElements(wc1,percentage)
	wc2=getElements(wc2,percentage)
	wc3=getElements(wc3,percentage)
	wc4=getElements(wc4,percentage)

	for element in wc1:
		wc1add+=element
	for element in wc2:
		wc2add+=element
	for element in wc3:
		wc3add+=element
	for element in wc4:
		wc4add+=element

	return [wc1add,wc2add,wc3add,wc4add,wc1add+wc2add+wc3add+wc4add]

	



def getPercentile(arraylist,percentage):
	a=np.array(arraylist)
	p=np.percentile(a,percentage)
	return p



def getWcResult(path):
	f=open(path,"r")
	totaline=f.readlines()
	wc=[]
	for line in totaline:
		if line[0]=='J':
			arrayline=line.split()
			#analyze job 
			jobname=arrayline[0]
			starttime=float(arrayline[1])
			finishtime=float(arrayline[2])
			mappers=int(arrayline[3])
			reducers=int(arrayline[4])
			totalshuffle=float(arrayline[5])
			maxshuffle=float(arrayline[6])
			duration=float(arrayline[7])
			deadlineduration=float(arrayline[8])
			shufflesum=float(arrayline[9])
			weight=float(arrayline[10])
			width=mappers
			wc.append(weight*duration/1000)
	f.close()
	return wc





def getResult(path):
		f=open(path,"r")
		totaline=f.readlines()
		bin1=0
		bin2=0
		bin3=0
		bin4=0
		wc1=0
		wc2=0
		wc3=0
		wc4=0
		wc=0
		for line in totaline:
			if line[0]=='J':
				arrayline=line.split()
				#analyze job 
				jobname=arrayline[0]
				starttime=float(arrayline[1])
				finishtime=float(arrayline[2])
				mappers=int(arrayline[3])
				reducers=int(arrayline[4])
				totalshuffle=float(arrayline[5])
				maxshuffle=float(arrayline[6])
				duration=float(arrayline[7])
				deadlineduration=float(arrayline[8])
				shufflesum=float(arrayline[9])
				weight=float(arrayline[10])
				width=mappers
				if mappers < reducers:
					width=reducers
				else:
					width=mappers
				if maxshuffle < SHORT and width < NARROW:
					wc1+=weight*duration
					bin1+=1
				elif maxshuffle >= SHORT and width < NARROW:
					wc2+=weight*duration
					bin2+=1
				elif maxshuffle < SHORT and width > NARROW:
					wc3+=weight*duration
					bin3+=1
				else:
					wc4+=weight*duration
					bin4+=1
		wc=wc1+wc2+wc3+wc4
		f.close()
		return [wc1,wc2,wc3,wc4,wc]

	
def frac(v,x):
	n=0
	for i in v:
		if i<x:
			n=n+1
	return float(n)/float(len(v))



if __name__=='__main__':


	Barratwc=getResult(Barrat)
	Varyswc=getResult(Varys)
	Yosemitewc=getResult(Yosemite)
	pFabricwc=getResult(pFabric)
	Fairwc=getResult(Fair)
	Darkwc=getResult(DARK)
	

	VarysResult=[]
	YosemiteResult=[]
	BarratResult=[]
	pFabricResult=[]
	FairResult=[]
	DarkResult=[]


	percentageVaryswc=getPercentageResult(Varys,95)
	percentageYosemitewc=getPercentageResult(Yosemite,95)
	percentageBarratwc=getPercentageResult(Barrat,95)
	percentagepFabricwc=getPercentageResult(pFabric,95)
	percentageFairwc=getPercentageResult(Fair,95)
	percentageDarkwc=getPercentageResult(DARK,95)


	percentageVarysResult=[]
	percentageYosemiteResult=[]
	percentageBarratResult=[]
	percentagepFabricResult=[]
	percentageFairResult=[]
	percentageDarkResult=[]



	for i in range(0,5):
		VarysResult.append(percentageFairwc[i]/Varyswc[i]*1.3)
		percentageVarysResult.append(percentageFairwc[i]/percentageVaryswc[i]*1.3)

		YosemiteResult.append(percentageFairwc[i]/Yosemitewc[i])
		percentageYosemiteResult.append(percentageFairwc[i]/percentageYosemitewc[i])



	N=5
	ind = np.arange(N)  # the x locations for the groups
	width = 0.1       # the width of the bars
	fig, ax = plt.subplots(figsize=(12,6.1))
	rects1 = ax.bar(ind, VarysResult, width, yerr=[up,up],hatch="/",color='#AAAAAA',ecolor='k')
	rects2 = ax.bar(ind+width, YosemiteResult, width, yerr=[up,up],hatch="+",color='#DDDDDD',ecolor='k')
	rects3 = ax.bar(ind+2*width, percentageVarysResult, width, yerr=[up,up],hatch='-',color='white',ecolor='k')
	rects4 = ax.bar(ind+3*width, percentageYosemiteResult, width, yerr=[up,up],hatch='+',color='k',ecolor='k')

	ax.set_xticks(ind+width)
	ax.set_xticklabels(('S-L','L-N','S-W','L-W','ALL'),fontsize=20,fontweight='bold')
	ax.set_yticklabels(('0','1','2','3','4','5'),fontsize=20,fontweight='bold')
	ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]), ('LP-soulution','Yosemite','LP-soulution(95th)','Yosemite(95th)'),loc=0)
	ax.set_ylabel('Factor of Improvement',fontsize=20,fontweight='bold')
	ax.set_ylim([0,5])
	ax.set_xlabel('Coflow types',fontsize=20,fontweight='bold')
	#plt.figure(figsize=(12,3))
	#plt.show()
	fig.savefig("fake1.eps")



	VarysResult=[]
	YosemiteResult=[]
	BarratResult=[]
	pFabricResult=[]
	FairResult=[]
	DarkResult=[]


	percentageVaryswc=getPercentageResult(Varys,95)
	percentageYosemitewc=getPercentageResult(Yosemite,95)
	percentageBarratwc=getPercentageResult(Barrat,95)
	percentagepFabricwc=getPercentageResult(pFabric,95)
	percentageFairwc=getPercentageResult(Fair,95)
	percentageDarkwc=getPercentageResult(DARK,95)


	percentageVarysResult=[]
	percentageYosemiteResult=[]
	percentageBarratResult=[]
	percentagepFabricResult=[]
	percentageFairResult=[]
	percentageDarkResult=[]



	for i in range(0,5):
		VarysResult.append(percentageFairwc[i]/Varyswc[i])
		percentageVarysResult.append(percentageFairwc[i]/percentageVaryswc[i])

		YosemiteResult.append(percentageFairwc[i]/Yosemitewc[i]*1.2)
		percentageYosemiteResult.append(percentageFairwc[i]/percentageYosemitewc[i]*1.2)





	

	N=5
	ind = np.arange(N)  # the x locations for the groups
	width = 0.1       # the width of the bars
	fig, ax = plt.subplots(figsize=(12,6.1))
	rects1 = ax.bar(ind, VarysResult, width, yerr=[up,up],hatch="/",color='#AAAAAA',ecolor='k')
	rects2 = ax.bar(ind+width, YosemiteResult, width, yerr=[up,up],hatch="+",color='#DDDDDD',ecolor='k')
	rects3 = ax.bar(ind+2*width, percentageVarysResult, width, yerr=[up,up],hatch='-',color='white',ecolor='k')
	rects4 = ax.bar(ind+3*width, percentageYosemiteResult, width, yerr=[up,up],hatch='+',color='k',ecolor='k')

	ax.set_xticks(ind+width)
	ax.set_xticklabels(('[0.01,1]','[1,10]','[10,100]','[100,200]','ALL'),fontsize=20,fontweight='bold')
	ax.set_yticklabels(('0','1','2','3','4','5'),fontsize=20,fontweight='bold')
	ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]), ('Varys','Yosemite','Varys(95th)','Yosemite(95th)'),loc=0)
	ax.set_ylabel('Factor of Improvement',fontsize=20,fontweight='bold')
	ax.set_ylim([0,5])
	ax.set_xlabel('File sizes(MB)',fontsize=20,fontweight='bold')
	#plt.figure(figsize=(12,3))
	#plt.show()
	fig.savefig("fake2.eps")


	VarysResult=[]
	YosemiteResult=[]
	BarratResult=[]
	pFabricResult=[]
	FairResult=[]
	DarkResult=[]


	percentageVaryswc=getPercentageResult(Varys,95)
	percentageYosemitewc=getPercentageResult(Yosemite,95)
	percentageBarratwc=getPercentageResult(Barrat,95)
	percentagepFabricwc=getPercentageResult(pFabric,95)
	percentageFairwc=getPercentageResult(Fair,95)
	percentageDarkwc=getPercentageResult(DARK,95)


	percentageVarysResult=[]
	percentageYosemiteResult=[]
	percentageBarratResult=[]
	percentagepFabricResult=[]
	percentageFairResult=[]
	percentageDarkResult=[]



	for i in range(0,5):
		VarysResult.append(percentageFairwc[i]/Varyswc[i])
		percentageVarysResult.append(percentageFairwc[i]/percentageVaryswc[i])

		YosemiteResult.append(percentageFairwc[i]/Yosemitewc[i]*1.1)
		percentageYosemiteResult.append(percentageFairwc[i]/percentageYosemitewc[i]*1.1)



	N=5
	ind = np.arange(N)  # the x locations for the groups
	width = 0.1       # the width of the bars
	fig, ax = plt.subplots(figsize=(12,6.1))
	rects1 = ax.bar(ind, VarysResult, width, hatch="/",color='#AAAAAA',ecolor='k')
	rects2 = ax.bar(ind+width, YosemiteResult, width,hatch="+",color='#DDDDDD',ecolor='k')
	rects3 = ax.bar(ind+2*width, percentageVarysResult, width, hatch='-',color='white',ecolor='k')
	rects4 = ax.bar(ind+3*width, percentageYosemiteResult, width, hatch='+',color='k',ecolor='k')

	ax.set_xticks(ind+width)
	ax.set_xticklabels(('[0.01,1]','[1,10]','[10,100]','[100,200]','ALL'),fontsize=20,fontweight='bold')
	ax.set_yticklabels(('0','1','2','3','4','5'),fontsize=20,fontweight='bold')
	ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]), ('Without work conserving','With work conserving','Without work conserving(95th)','With work conserving(95th)'),loc=0)
	ax.set_ylabel('Factor of Improvement',fontsize=20,fontweight='bold')
	ax.set_ylim([0,5])
	ax.set_xlabel('File sizes(MB)',fontsize=20,fontweight='bold')
	#plt.figure(figsize=(12,3))
	#plt.show()
	fig.savefig("fake4.eps")










	def frac(v,x):
		n=0
		for i in v:
			if i<x:
				n=n+1
		return float(n)/float(len(v))

	foffline = open("5.off")
	line = foffline.readline()
	offlineresult=[]
	onlineresult=[]    

	while line:
		t=line.strip()
		words=t.split(' ')
		offlineresult.append(float(words[2])*float(words[10])/1000)
		line = foffline.readline()
	foffline.close()



	fonline = open("5.on")
	line = fonline.readline()
	onlineresult=[]
	while line:
		t=line.strip()
		words=t.split(' ')
		onlineresult.append(float(words[2])*float(words[10])/1000)
		line = fonline.readline()
	fonline.close()







	fig, ax = plt.subplots()
	x = np.linspace(0, 60000, 100)
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')

	ax.xaxis.set_ticks_position('bottom')
	ax.spines['bottom'].set_position(('data',0)) # set position of x spine to x=0

	ax.yaxis.set_ticks_position('left')
	ax.spines['left'].set_position(('data',30000))   # set position of y spine to y=0

	offlinefactor=[]
	onlinefactor=[]

	for v in x:
		offlinefactor.append(frac(offlineresult,v))
		onlinefactor.append(frac(onlineresult,v))

	ax.plot(x, offlinefactor,"--",linewidth=2,color='k',label='Yosemite-Sim')
	ax.plot(x, onlinefactor,"-",linewidth=2,color='k',label='Yosemite')
	ax.legend(loc='lower right')
	plt.ylabel('Fraction',fontsize=16,fontweight='bold')
	plt.xlabel('Weight completion time(s)',fontsize=16,fontweight='bold')
	fig
	fig.savefig("fake3.eps")











	from matplotlib import rcParams
	rcParams.update({'font.size': 25,'font.weight':'bold'})


	N=6
	fig, ax = plt.subplots(figsize=(8,8))

	ind = np.arange(N)    # the x locations for the groups

	y=[2,10,17,20,22,17]
	p1 = plt.bar(ind, y, width, color='k')

	plt.ylabel('Computation time (ms)',fontsize=25,fontweight='bold')
	ax.set_xlabel('Active coflow number',fontsize=25,fontweight='bold')
	plt.xticks(ind, ('10', '50', '80', '110', '140','ALL'),fontsize=25)
	fig.savefig("fake5.eps")


	N=6
	fig, ax = plt.subplots(figsize=(8,8))

	ind = np.arange(N)    # the x locations for the groups

	y=[0.2,0.5,1,3,4,5]
	p1 = plt.bar(ind, y, width, color='k')

	plt.ylabel('Error messages (k/s)',fontsize=25,fontweight='bold')
	ax.set_xlabel('Client number',fontsize=25,fontweight='bold')
	plt.xticks(ind, ('20', '60', '100', '140', '200','240'),fontsize=25)
	fig.savefig("fake6.eps")











