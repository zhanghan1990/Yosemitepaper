# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import stats

from matplotlib import rcParams
rcParams.update({'font.size': 16,'font.weight':'bold'})

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
		VarysResult.append(percentageFairwc[i]/Varyswc[i])
		percentageVarysResult.append(percentageFairwc[i]/percentageVaryswc[i])

		YosemiteResult.append(percentageFairwc[i]/Yosemitewc[i])
		percentageYosemiteResult.append(percentageFairwc[i]/percentageYosemitewc[i])

		BarratResult.append(percentageFairwc[i]/Barratwc[i])
		percentageBarratResult.append(percentageFairwc[i]/percentageBarratwc[i])

		DarkResult.append(percentageFairwc[i]/Darkwc[i])
		percentageDarkResult.append(percentageFairwc[i]/percentageDarkwc[i])


	N=5
	ind = np.arange(N)  # the x locations for the groups
	width = 0.1       # the width of the bars
	fig, ax = plt.subplots(figsize=(12,6))
	rects1 = ax.bar(ind, BarratResult, width, yerr=[up,up],hatch="/",color='#AAAAAA',ecolor='k')
	rects2 = ax.bar(ind+width, DarkResult, width, yerr=[up,up],hatch="+",color='#DDDDDD',ecolor='k')
	rects3 = ax.bar(ind+2*width, VarysResult, width, yerr=[up,up],hatch='-',color='white',ecolor='k')
	rects4 = ax.bar(ind+3*width, YosemiteResult, width, yerr=[up,up],hatch='+',color='k',ecolor='k')

	rects5 = ax.bar(ind+4*width, percentageBarratResult, width, yerr=[up,up],hatch="/",color='#666666',ecolor='k')
	rects6 = ax.bar(ind+5*width, percentageDarkResult, width, yerr=[up,up],hatch="+",color='#444444',ecolor='k')
	rects7 = ax.bar(ind+6*width, percentageVarysResult, width, yerr=[up,up],hatch='-',color='#EEE9E9',ecolor='k')
	rects8=ax.bar(ind+7*width, percentageYosemiteResult, width, yerr=[up,up],hatch='+',color='#696969',ecolor='k')

	ax.set_xticks(ind+width)
	ax.set_xticklabels(('S-N','L-N','S-W','L-W','ALL'),fontsize=16,fontweight='bold')
	ax.set_yticklabels((0,1,2,3,4,5,6),fontsize=16,fontweight='bold')
	ax.legend((rects1[0],rects2[0],rects3[0],rects4[0],rects5[0],rects6[0],rects7[0],rects8[0]), ('Barrat','Aalo','Varys','Yosemite','Barrat(95th)','Aalo(95th)','Varys(95th)','Yosemite(95th)'),loc=0,fontsize=14)
	ax.set_ylabel('Factor of Improvement',fontsize=16,fontweight='bold')
	ax.set_ylim([0,5])
	ax.set_xlabel('Coflow types',fontsize=16,fontweight='bold')
	#plt.figure(figsize=(12,3))
	#plt.show()
	fig.savefig("weight_real_type.eps")



	fig, ax = plt.subplots(figsize=(6,7))

	x = np.linspace(0, 1000, 10)
	Yosemitewc=getWcResult(Yosemite)
	Varyswc=getWcResult(Varys)
	Fairwc=getWcResult(Fair)
	pFabricwc=getWcResult(pFabric)
	Barratwc=getWcResult(Barrat)
	Darkwc=getWcResult(DARK)

	YosemiteCDF=[]
	VarysCDF=[]
	FairCDF=[]
	pFabricCDF=[]
	BarratCDF=[]
	AaloCDF=[]

	for v in x:
		YosemiteCDF.append(frac(Yosemitewc,v))
		VarysCDF.append(frac(Varyswc,v))
		FairCDF.append(frac(Fairwc,v))
		pFabricCDF.append(frac(pFabricwc,v))
		BarratCDF.append(frac(Barratwc,v))
		AaloCDF.append(frac(Darkwc,v))

	ax.plot(x, BarratCDF,".",linewidth=3,color='k',marker='v',label='Barrat')

	ax.plot(x, FairCDF,":",linewidth=3,color='k',label='TCP-fair')
	ax.plot(x, AaloCDF,"--",linewidth=3,color='k',label='Aalo')
	ax.plot(x, YosemiteCDF,linewidth=3,color='k',label='Yosemite')
	ax.set_xticklabels(('0','200','400','600','800','1000'),fontsize=14,fontweight='bold')
	ax.legend(loc='lower right')
	plt.ylabel('CDF',fontsize=16,fontweight='bold')
	plt.xlabel('WCCT(s)',fontsize=16,fontweight='bold')
	plt.show()
	fig.savefig("weight_CDF_compare.eps")

