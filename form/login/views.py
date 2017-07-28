from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

def login(request):
	return render_to_response('Login.html')

@csrf_exempt #decorator for by passing cross-site request form 
def years(request):
	iamt=int(request.POST['iamt'])
	a=int(request.POST['iamt'])
	famt=int(request.POST['famt'])
	rate=int(request.POST['rate'])
	i=-1
	while iamt<=famt:
		iamt=(iamt+(rate/100)*iamt)
		i+=1
	mydata={'init':a,'final':famt,'rt':rate,'yrs':i}
	return render_to_response('years.html',mydata)
