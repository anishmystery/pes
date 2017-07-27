from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from exam.models import Exam
import matplotlib.pyplot as plt

@csrf_exempt
def index(request):
	return render_to_response('index.html')

@csrf_exempt
def save(request):
	mval=float(request.POST['m'])
	vval=float(request.POST['v0'])
	y=[]
	pval=[]
	kval=[]
	v=[]
	pkval=[]
	t=[0,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.2,2.3]
	for i in t:
		f=vval*i-0.5*9.8*i*i
		y.append(f)
		vval=f
		v.append(vval)
		print(v)
	for i in y:
		f=mval*9.8*i
		pval.append(f)
		#print(pval)
	for i in v:
		f=0.5*mval*i*i
		kval.append(f)
		#print(kval)
	for i in range(0,10):
		f=pval[i]+kval[i]
		e=Exam()
		e.p=pval[i]
		e.k=kval[i]
		e.p_k=f
		e.save()
		pkval.append(f)
	for i in pval:
		file=open("file1.txt","w")
		file.write("%s\n" % i)
		file.close()
	for i in kval:
		file1=open("file1.txt","a")
		file1.write("%s\n" % i)
	for i in pkval:
		file1=open("file1.txt","a")
		file1.write("%s\n" % i)
	file1.close()
	plt.plot(pval,t)
	plt.show()
	plt.plot(kval,t)
	plt.show()
	plt.plot(pkval,t)
	plt.show()
	# print(pkval)
	return render_to_response('save.html')
