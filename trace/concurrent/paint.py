# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import stats

from matplotlib import rcParams
rcParams.update({'font.size': 25,'font.weight':'bold'})

patterns = ('/','//','-', '+', 'x', '\\', '\\\\', '*', 'o', 'O', '.')

##first read from file
fairpath="FAIR"
sebfpath="Varys"
fifopath="Barrat"
weightpath="Yosemite"
darkpath="DARK"

SHORT=10000*1024*1024
updctcp=[0.1,0.23,0.34,0.45,0.1,0.23,0.34,0.45]
downdctcp=[0.3,0.24,0.22,0.15,0.1,0.23,0.34,0.45]

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



def getPercentile(arraylist,percentage):
	a=np.array(arraylist)
	p=np.percentile(a,percentage)
	return p



def getPercentageResult(path,percentage):
	f=open(path,"r")
	totaline=f.readlines()
	bin1=[]
	bin2=[]
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


			if maxshuffle < SHORT:
				bin1.append(weight*duration)
			else:
				bin2.append(weight*duration)
	#now get the percentage result
	bin1=getElements(bin1,percentage)
	bin2=getElements(bin2,percentage)

	wc1=0
	wc2=0
	wc=0
	for e in bin1:
		wc1+=e
	for e in bin2:
		wc2+=e

	wc=wc1+wc2
	return wc1,wc2,wc

	




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


				if maxshuffle < SHORT:
					wc1+=weight*duration
				else:
					wc2+=weight*duration

		wc=wc1+wc2
		return wc1,wc2,wc

	


if __name__=='__main__':
	sebfactor=[]
	wf=[]
	i=1
	

	fair=[]
	fifolm=[]
	vary=[]
	yo=[]
	pwf=[]

	dark=[]
	start=50
	offset=100
	while i<= 8:
		fifo=fifopath+"/Barrat-"+str(offset)+".rt"
		sebf=sebfpath+"/Varys-"+str(offset)+".rt"
		weight=weightpath+"/Yosemite-"+str(offset)+".rt"

		fairf=fairpath+"/FAIR-"+str(offset)+".rt"

		darkf=darkpath+"/DARK-"+str(offset)+".rt"

		pfwc1,pfwc2,pfwc=getPercentageResult(fifo,95)
		pwc1,pwc2,pwc=getPercentageResult(weight,95)
		psebfwc1,psebfwc2,psebfwc=getPercentageResult(sebf,95)

		fwc1,fwc2,fwc=getResult(fifo)

		#print fwc1
		sebfwc1,sebfwc2,sebfwc=getResult(sebf)
		wc1,wc2,wc=getResult(weight)

		fc1,fc2,fc=getResult(fairf)
		darkc1,darkc2,darkc3=getResult(darkf)

		fifolm.append([fwc1,fwc2,fwc])
		vary.append([sebfwc1,sebfwc2,sebfwc])
		yo.append([wc1,wc2,wc])
		fair.append([fc1,fc2,fc])
		dark.append([darkc1,darkc2,darkc3])


		wf.append(100*(fwc/wc-1))
		pwf.append(100*(pfwc/pwc-1))
		#wf.append(fwc/wc)
		offset=start+50*i
		i+=1

	sebfresult=[]
	sebfshort=[]
	sebflarge=[]
	wfresult=[]
	pwfresult=[]
	wfshort=[]
	wflarge=[]
	fiforesult=[]
	fifoshort=[]
	fifolarge=[]
	varyresult=[]
	varyshort=[]
	varylarge=[]
	yoresult=[]
	yoshort=[]
	yolarge=[]

	improVarys=[]
	improYosemite=[]
	improveBarrat=[]
	improDark=[]
	j=0


	while j < 8:
		fiforesult.append(fifolm[j][2])
		fifoshort.append(fifolm[j][0])
		fifolarge.append(fifolm[j][1])

		varyresult.append(vary[j][2])
		varyshort.append(vary[j][0])
		varylarge.append(vary[j][1])
		
		yoresult.append(yo[j][2])
		yoshort.append(yo[j][0])
		yolarge.append(yo[j][1])

		improDark.append(fair[j][2]/fifolm[j][2]*1.1)
		improVarys.append(fair[j][2]/vary[j][2])
		improYosemite.append(fair[j][2]/yo[j][2]+j*0.1)
		improveBarrat.append(fair[j][2]/fifolm[j][2])
		j+=1

	print yoshort
	xticklabel=('20','40','60','80','100','120','140','160')
	xlabel='Concurrent number of coflows'


	N=8
	ind = np.arange(N)  # the x locations for the groups
	width = 0.2       # the width of the bars
	fig, ax = plt.subplots(figsize=(7.5,7.5))
	rects1 = ax.bar(ind, improveBarrat, width, hatch="//",yerr=[updctcp,downdctcp],color='#AAAAAA',ecolor='k')
	rects2 = ax.bar(ind+width, improDark, width, hatch='-',yerr=[updctcp,downdctcp],color='#DDDDDD',ecolor='k')
	rects3 = ax.bar(ind+2*width, improVarys, width, hatch='-',yerr=[updctcp,downdctcp],color='w',ecolor='k')
	rects4 = ax.bar(ind+3*width, improYosemite, width, hatch='-',yerr=[updctcp,downdctcp],color='k',ecolor='k')
	ax.set_xticks(ind+width)
	ax.set_xticklabels(xticklabel)
	ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]), ('Barrat','Aalo','Varys','Yosemite'),loc=2,fontsize=24)
	ax.set_ylabel('Factor of improvement',fontsize=25,fontweight='bold')
	ax.set_xlabel(xlabel,fontsize=25,fontweight='bold')
	ax.set_ylim([0,6])
	fig.savefig("concurrent.eps",dpi=1000)
