from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import make_password, check_password
from PES.models import Employee, Department, Designation, City, State, Skill, SkillReview 
from PES.models import SkillDesignation, EmployeeAuthority, AdditionalSkill, AdditionalSkillReview
import datetime
import base64

#----------------------------Login Start--------------------------------------
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def login(request):
    return render_to_response('Login.html')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def logout(request):
	try: 
		del request.session['user']
		del request.session['encstr']		
		request.session.modified = True
	except: pass
	return render_to_response('Login.html')

@csrf_exempt
def signin(request):
	username = request.POST['un']
	password = request.POST['psw']
	e = Employee.objects.get(Email=username)
	request.session['user'] = e.Name
	request.session['encstr'] = e.ProfilePic
	request.session['dsgid'] = e.Designation_id
	request.session['id'] = e.id
	if "chk" in request.POST and check_password(password, e.Password):
		emp_q2 = Employee.objects.filter(Email=username).filter(IsAdmin=1)
		if(emp_q2.count()==0):
			return render_to_response('Login.html')
		else:
			rec_emp = Employee.objects.filter(IsActive=1)
			rec_desg = Designation.objects.all()
			rec_dept = Department.objects.all()
			rec_state = State.objects.all()
			rec_city = City.objects.all()
			for i in rec_emp:
				desg = rec_desg.filter(id=i.Designation_id)
				dept = rec_dept.filter(id=i.Department_id)
				state = rec_state.filter(id=i.State_id)
				city = rec_city.filter(id=i.City_id)
				for j in desg:
					i.DesignationName = j.DesignationName
				for x in dept:
					i.DepartmentName = x.DepartmentName
				for y in state:
					i.StateName = y.StateName
				for z in city:
					i.CityName = z.CityName
			return render_to_response('Admin_Index.html',{"records":rec_emp,"user":request.session['user'],"encstr":request.session['encstr']})

	else:
		if check_password(password, e.Password):
			emp_q = Employee.objects.filter(Email=username).filter(IsActive=1)
			if(emp_q.count()==0):
				return render_to_response('Login.html')
			else:
				return render_to_response('Employee_Index.html',{"user":request.session['user'],"encstr":request.session['encstr']})
#----------------------------Login End--------------------------------------

#----------------------------Admin Start--------------------------------------
def home(request):
	rec_emp = Employee.objects.filter(IsActive=1)
	rec_desg = Designation.objects.all()
	rec_dept = Department.objects.all()
	rec_state = State.objects.all()
	rec_city = City.objects.all()
	for i in rec_emp:
		desg = rec_desg.filter(id=i.Designation_id)
		dept = rec_dept.filter(id=i.Department_id)
		state = rec_state.filter(id=i.State_id)
		city = rec_city.filter(id=i.City_id)
		for j in desg:
			i.DesignationName = j.DesignationName
		for x in dept:
			i.DepartmentName = x.DepartmentName
		for y in state:
			i.StateName = y.StateName
		for z in city:
			i.CityName = z.CityName
	return render_to_response('Admin_Index.html',{"records":rec_emp,"user":request.session['user'],"encstr":request.session['encstr']})

def addemp(request):
	desg = Designation.objects.all()
	dept = Department.objects.all()
	city = City.objects.all()
	state = State.objects.all()
	dictn = {"desg":desg,"dept":dept,"city":city,"state":state,"user":request.session['user'],"encstr":request.session['encstr']}
	return render_to_response('Add_Employee.html', dictn)

@csrf_exempt
def detailsemp(request):
	code = request.POST['ecode']
	name = request.POST['ename']
	dg = request.POST['dropdesg']
	gender = request.POST.get('gen')
	dp = request.POST['dropdept']
	bd = request.POST['dob']
	jd = request.POST['join']
	ad = request.POST['addr']
	ct = request.POST['dropcity']
	mn = request.POST['mob']
	st = request.POST['dropstate']
	em = request.POST['email']
	ps = request.POST['pw']
	pc = request.POST['pin']
	bdt = datetime.strptime(bd, "%d/%m/%Y")
	jdt = datetime.strptime(jd, "%d/%m/%Y")
	psw = make_password(ps)
	if "adm" in request.POST:
		admin = 1
	else:
		admin = 0
	for i in request.FILES.getlist('profpic'):
		with open("PES/static/images/"+i.name, "rb") as image_file:
    			encoded_string = base64.b64encode(image_file.read())
		encstr = str(encoded_string,'utf-8')
		encstr = "data:image/jpg;base64,"+encstr
	emp = Employee()
	emp.EmployeeCode = code
	emp.Name = name
	emp.Designation_id = dg
	emp.Gender = gender
	emp.Department_id = dp
	emp.DOB = bdt
	emp.JoiningDate = jdt
	emp.Address = ad
	emp.City_id = ct
	emp.Mobile = mn
	emp.State_id = st
	emp.Email = em
	emp.ProfilePic = encstr
	emp.Pincode = pc
	emp.Password = psw
	emp.IsActive = 1
	emp.IsAdmin = admin
	emp.save()
	

	rec_emp = Employee.objects.filter(IsActive=1)
	rec_desg = Designation.objects.all()
	rec_dept = Department.objects.all()
	rec_state = State.objects.all()
	rec_city = City.objects.all()
	for i in rec_emp:
		desg = rec_desg.filter(id=i.Designation_id)
		dept = rec_dept.filter(id=i.Department_id)
		state = rec_state.filter(id=i.State_id)
		city = rec_city.filter(id=i.City_id)
		for j in desg:
			i.DesignationName = j.DesignationName
		for x in dept:
			i.DepartmentName = x.DepartmentName
		for y in state:
			i.StateName = y.StateName
		for z in city:
			i.CityName = z.CityName
	return render_to_response('Admin_Index.html',{"records":rec_emp,"user":request.session['user'],"encstr":request.session['encstr']})

@csrf_exempt
def viewtech(request):
	rec_tech = Skill.objects.filter(SkillType="Technical")
	return render_to_response('Tech_Skills_Index.html',{"rec_tech":rec_tech,"user":request.session['user'],"encstr":request.session['encstr']})

def addtech(request):
	return render_to_response('Add_Tech_Skills.html',{"user":request.session['user'],"encstr":request.session['encstr']})

@csrf_exempt
def techskills(request):

	tech = request.POST['tskill']
	skill = Skill()
	skill.SkillName = tech
	skill.SkillType = "Technical"
	skill.IsActive = 1
	skill.save()
	rec_tech = Skill.objects.filter(SkillType="Technical").filter(IsActive=1)
	return render_to_response('Tech_Skills_Index.html',{"rec_tech":rec_tech,"user":request.session['user'],"encstr":request.session['encstr']})

def alltech(request):
	desg = Designation.objects.all()
	tech = Skill.objects.filter(SkillType="Technical").filter(IsActive=1)
	dept = Department.objects.all()
	techdesg = {"desg":desg,"tech":tech,"dept":dept,"user":request.session['user'],"encstr":request.session['encstr']}
	return render_to_response('Allocate_Tech_Skills.html', techdesg)

@csrf_exempt
def alloctech(request):
	dpt = request.POST['dropdept']
	dsg = request.POST['dropdesg']
	ts = request.POST['droptech']
	thresh = request.POST['dropthresh']
	skilld = SkillDesignation()
	skilld.Skill_id = ts
	skilld.Designation_id = dsg
	skilld.Department_id = dpt
	skilld.Threshold = thresh
	skilld.save()
	rec_tech = Skill.objects.filter(SkillType="Technical").filter(IsActive=1)
	return render_to_response('Tech_Skills_Index.html',{"rec_tech":rec_tech,"user":request.session['user'],"encstr":request.session['encstr']})

@csrf_exempt
def viewnontech(request):
	rec_nontech = Skill.objects.filter(SkillType="Non-Technical").filter(IsActive=1)
	return render_to_response('Non_Tech_Skills_Index.html',{"rec_nontech":rec_nontech,"user":request.session['user'],"encstr":request.session['encstr']})

def addnontech(request):
	return render_to_response('Add_Non_Tech_Skills.html',{"user":request.session['user'],"encstr":request.session['encstr']})

@csrf_exempt
def ntskills(request):

	nontech = request.POST['ntskill']
	print(nontech)
	ntskill = Skill()
	ntskill.SkillName = nontech
	ntskill.SkillType = "Non-Technical"
	ntskill.IsActive = 1
	ntskill.save()
	rec_nontech = Skill.objects.filter(SkillType="Non-Technical").filter(IsActive=1)
	return render_to_response('Non_Tech_Skills_Index.html',{"rec_nontech":rec_nontech},{"user":request.session['user'],"encstr":request.session['encstr']})

def allnontech(request):
	desg = Designation.objects.all()
	nontech = Skill.objects.filter(SkillType="Non-Technical").filter(IsActive=1)
	dept = Department.objects.all()
	nontechdesg = {"desg":desg,"nontech":nontech,"dept":dept,"user":request.session['user'],"encstr":request.session['encstr']}
	return render_to_response('Allocate_Non_Tech_Skills.html',nontechdesg)

@csrf_exempt
def allocnontech(request):
	dpt = request.POST['dropdept']
	dsg = request.POST['dropdesg']
	nts = request.POST['dropnontech']
	thresh = request.POST['dropthresh']
	skilld = SkillDesignation()
	skilld.Skill_id = nts
	skilld.Designation_id = dsg
	skilld.Department_id = dpt
	skilld.Threshold = thresh
	skilld.save()
	rec_nontech = Skill.objects.filter(SkillType="Non-Technical").filter(IsActive=1)
	return render_to_response('Non_Tech_Skills_Index.html',{"rec_nontech":rec_nontech,"user":request.session['user'],"encstr":request.session['encstr']})

def addmanager(request):
	mgr = Employee.objects.filter(Designation_id=3)
	dpt = Department.objects.all()
	for i in mgr:
		dept = dpt.filter(id=i.Department_id)
		for x in dept:
			i.DepartmentName = x.DepartmentName
	return render_to_response('Manager_Index.html',{"mgr":mgr,"user":request.session['user'],"encstr":request.session['encstr']})

def allmgr(request):
	emp = Employee.objects.filter(IsActive=1)
	mgr = Employee.objects.filter(IsActive=1).filter(Designation_id=3)
	dictn = {"emp":emp,"mgr":mgr,"user":request.session['user'],"encstr":request.session['encstr']}
	return render_to_response('Allocate_Manager.html',dictn)

@csrf_exempt
def allocmgr(request):
	e = request.POST['dropemp']
	m = request.POST['dropmgr']
	auth = EmployeeAuthority()
	auth.Employee_id = e
	auth.Authority_id = m
	auth.IsActive = 1
	auth.ActiveFrom = datetime.date.today()
	auth.save()

	mgr = Employee.objects.filter(Designation_id=3)
	dpt = Department.objects.all()
	for i in mgr:
		dept = dpt.filter(id=i.Department_id)
		for x in dept:
			i.DepartmentName = x.DepartmentName
	return render_to_response('Manager_Index.html',{"mgr":mgr,"user":request.session['user'],"encstr":request.session['encstr']})

def deactivate(request, eid):
	replace = {'IsActive':0}
	obj = Employee.objects.get(id=eid)
	for key, value in replace.items():
		setattr(obj, key, value)
	obj.save()

	rec_emp = Employee.objects.filter(IsActive=1)
	rec_desg = Designation.objects.all()
	rec_dept = Department.objects.all()
	rec_state = State.objects.all()
	rec_city = City.objects.all()
	for i in rec_emp:
		desg = rec_desg.filter(id=i.Designation_id)
		dept = rec_dept.filter(id=i.Department_id)
		state = rec_state.filter(id=i.State_id)
		city = rec_city.filter(id=i.City_id)
		for j in desg:
			i.DesignationName = j.DesignationName
		for x in dept:
			i.DepartmentName = x.DepartmentName
		for y in state:
			i.StateName = y.StateName
		for z in city:
			i.CityName = z.CityName
	return render_to_response('Admin_Index.html',{"records":rec_emp,"user":request.session['user'],"encstr":request.session['encstr']})

#----------------------------Admin End--------------------------------------

#----------------------------Employee Start--------------------------------------
def emphome(request):
	return render_to_response('Employee_Index.html',{"user":request.session['user'],"encstr":request.session['encstr']})

def distech(request):
	sk = SkillDesignation.objects.filter(Designation_id=request.session['dsgid'])
	tech = Skill.objects.filter(SkillType="Technical")
	for i in sk:
		t = tech.filter(id=i.Skill_id)
		for x in t:
			i.SkillName = x.SkillName
	return render_to_response('Employee_Tech_Skills.html',{"sk":sk,"user":request.session['user'],"encstr":request.session['encstr']})

def disnon(request):
	sk = SkillDesignation.objects.filter(Designation_id=request.session['dsgid'])
	nontech = Skill.objects.filter(SkillType="Non-Technical")
	for i in sk:
		nt = nontech.filter(id=i.Skill_id)
		for x in nt:
			i.SkillName = x.SkillName
	return render_to_response('Employee_Non_Tech_Skills.html',{"sk":sk,"user":request.session['user'],"encstr":request.session['encstr']})

def adtskills(request):
	rec_adt = AdditionalSkill.objects.filter(Employee_id=request.session['id'])
	skill = Skill.objects.filter(IsActive=1)
	for a in rec_adt:
		s = skill.filter(id=a.Skill_id)
		for j in s:
			a.SkillName = j.SkillName
	return render_to_response('Additional_Skills_Index.html',{"rec_adt":rec_adt,"user":request.session['user'],"encstr":request.session['encstr']}) 

def alladdt(request):
	skill = Skill.objects.filter(IsActive=1)
	sk = SkillDesignation.objects.exclude(Designation_id=request.session['dsgid'])
	for a in sk:
		s = skill.filter(id=a.Skill_id)
		for j in s:
			a.SkillName = j.SkillName
	dictn = {"sk":sk,"user":request.session['user'],"encstr":request.session['encstr']}
	return render_to_response('Allocate_Additional_Skills.html',dictn)

@csrf_exempt
def allocaddt(request):
	s = request.POST['dropskill']
	t = request.POST['dropthresh']
	adt = AdditionalSkill()
	adt.Skill_id = s
	adt.Threshold = t
	adt.Employee_id = request.session['id']
	adt.IsCompleted = 0
	adt.save()
	rec_adt = AdditionalSkill.objects.filter(Employee_id=request.session['id'])
	skill = Skill.objects.all()
	for i in rec_adt:
		sk = skill.filter(id=i.Skill_id)
		for x in sk:
			i.SkillName = x.SkillName
	return render_to_response('Additional_Skills_Index.html',{"rec_adt":rec_adt,"user":request.session['user'],"encstr":request.session['encstr']})

def revindex(request):
	empall = Employee.objects.filter(IsActive=1)
	emp = Employee.objects.filter(Designation_id=request.session['dsgid'])
	mgr = EmployeeAuthority.objects.filter(Authority_id=request.session['id'])
	for i in emp:
		if i.Designation_id==3:
			for j in mgr:
				e = empall.filter(id=j.Employee_id)
				for x in e:
					j.Name = x.Name
			return render_to_response('Review_Index.html',{"mgr":mgr,"user":request.session['user'],"encstr":request.session['encstr']})		
		else:
			msg = "You've no employees to review!"
			return render_to_response('Review_Error.html',{"msg":msg,"user":request.session['user'],"encstr":request.session['encstr']})

def revskill(request, eid):
	emp = Employee.objects.get(id=eid)
	skill = Skill.objects.filter(IsActive=1)
	sk = SkillDesignation.objects.filter(Designation_id=emp.Designation_id)
	for a in sk:
		s = skill.filter(id=a.Skill_id)
		for j in s:
			a.SkillName = j.SkillName
			print(a.SkillName)
	return render_to_response('Review_Skill.html',{"emp":emp,"sk":sk,"user":request.session['user'],"encstr":request.session['encstr']})

@csrf_exempt
def skillreview(request, eid):
	skill = request.POST['dropskill']
	review = request.POST['droprev']
	skrev = SkillReview()
	skrev.Skill_id = skill
	skrev.Employee_id = eid
	skrev.Authority_id = request.session['id']
	skrev.Review = review
	skrev.ReviewedOn = datetime.date.today()
	skrev.save()

	empall = Employee.objects.filter(IsActive=1)
	emp = Employee.objects.filter(Designation_id=request.session['dsgid'])
	mgr = EmployeeAuthority.objects.filter(Authority_id=request.session['id'])
	for i in emp:
		if i.Designation_id==3:
			for j in mgr:
				e = empall.filter(id=j.Employee_id)
				for x in e:
					j.Name = x.Name
			return render_to_response('Review_Index.html',{"mgr":mgr,"user":request.session['user'],"encstr":request.session['encstr']})		
		else:
			msg = "You've no employees to review!"
			return render_to_response('Review_Error.html',{"msg":msg,"user":request.session['user'],"encstr":request.session['encstr']})

def revaddskill(request, eid):
	emp = Employee.objects.get(id=eid)
	addskill = AdditionalSkill.objects.filter(IsCompleted=0).filter(Employee_id=eid)
	sk = Skill.objects.filter(IsActive=1)
	for a in addskill:
		s = sk.filter(id=a.Skill_id)
		for j in s:
			a.SkillName = j.SkillName
	return render_to_response('Review_Additional_Skill.html',{"emp":emp,"addskill":addskill,"user":request.session['user'],"encstr":request.session['encstr']})

@csrf_exempt
def addtskillreview(request, eid):
	addskill = request.POST['dropaddskill']
	review = request.POST['droprev']
	addskrev = AdditionalSkillReview()
	addskrev.AdditionalSkill_id = addskill
	addskrev.Employee_id = eid
	addskrev.Authority_id = request.session['id']
	addskrev.Review = review
	addskrev.ReviewedOn = datetime.date.today()
	addskrev.save()

	empall = Employee.objects.filter(IsActive=1)
	emp = Employee.objects.filter(Designation_id=request.session['dsgid'])
	mgr = EmployeeAuthority.objects.filter(Authority_id=request.session['id'])
	for i in emp:
		if i.Designation_id==3:
			for j in mgr:
				e = empall.filter(id=j.Employee_id)
				for x in e:
					j.Name = x.Name
			return render_to_response('Review_Index.html',{"mgr":mgr,"user":request.session['user'],"encstr":request.session['encstr']})		
		else:
			msg = "You've no employees to review!"
			return render_to_response('Review_Error.html',{"msg":msg,"user":request.session['user'],"encstr":request.session['encstr']})








#----------------------------Employee End--------------------------------------