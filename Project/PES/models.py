from django.db import models

class Designation(models.Model):
	DesignationName = models.TextField()
	IsActive = models.BooleanField()

class Department(models.Model):
	DepartmentName = models.TextField()
	IsActive = models.BooleanField()

class Skill(models.Model):
	SkillName = models.TextField()
	SkillType = models.TextField()
	IsActive = models.BooleanField()

class State(models.Model):
	StateName = models.TextField()

class City(models.Model):
	CityName = models.TextField()
	State = models.ForeignKey('State', on_delete = models.CASCADE)

class Employee(models.Model):
	EmployeeCode = models.IntegerField()
	Name = models.TextField()
	DOB = models.DateField()
	Designation = models.ForeignKey('Designation', on_delete = models.CASCADE)
	Department = models.ForeignKey('Department', on_delete = models.CASCADE)
	JoiningDate = models.DateField()
	Email = models.TextField()
	Address = models.TextField()
	Mobile = models.TextField()
	Gender = models.TextField()
	City = models.ForeignKey('City', on_delete = models.CASCADE)
	State = models.ForeignKey('State', on_delete = models.CASCADE)
	Pincode = models.TextField()
	Password = models.TextField()
	ProfilePic = models.TextField()
	IsActive = models.BooleanField()
	IsAdmin = models.BooleanField()

class SkillDesignation(models.Model):
	Skill = models.ForeignKey('Skill', on_delete = models.CASCADE)
	Designation = models.ForeignKey('Designation', on_delete = models.CASCADE)
	Department = models.ForeignKey('Department', on_delete = models.CASCADE)
	Threshold = models.IntegerField()

class AdditionalSkill(models.Model):
	Skill = models.ForeignKey('Skill', on_delete = models.CASCADE)
	Employee = models.ForeignKey('Employee', on_delete = models.CASCADE)
	Threshold = models.IntegerField()
	IsCompleted = models.BooleanField()

class EmployeeAuthority(models.Model):
	Employee = models.ForeignKey('Employee', on_delete = models.CASCADE, related_name='EmployeeId')
	Authority = models.ForeignKey('Employee', on_delete = models.CASCADE, related_name='AuthorityId')
	IsActive = models.BooleanField()
	ActiveFrom = models.DateField()
	ActiveTo = models.DateField()

class SkillReview(models.Model):
	Skill = models.ForeignKey('Skill', on_delete = models.CASCADE)
	Employee = models.ForeignKey('Employee', on_delete = models.CASCADE)
	Authority = models.ForeignKey('EmployeeAuthority', on_delete = models.CASCADE)
	Review = models.IntegerField()
	ReviewedOn = models.DateField()

class AdditionalSkillReview(models.Model):
	AdditionalSkill = models.ForeignKey('AdditionalSkill', on_delete = models.CASCADE)
	Employee = models.ForeignKey('Employee', on_delete = models.CASCADE)
	Authority = models.ForeignKey('EmployeeAuthority', on_delete = models.CASCADE)
	Review = models.IntegerField()
	ReviewedOn = models.DateField()
