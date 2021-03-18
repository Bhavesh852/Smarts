from django.db import models

# Create your models here.



class Contact(models.Model):
	msg_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=70)
	email = models.CharField(max_length=70, default="")
	phone = models.CharField(max_length=50, default="")
	msg= models.CharField(max_length=50, default="")
	
	def __str__(self):
		return self.name

class Complaints(models.Model):
	com_id = models.AutoField(primary_key=True)
	uname = models.CharField(max_length=70)
	flat = models.CharField(max_length=10, default="")
	complaint = models.CharField(max_length=255, default="")
	reply = models.CharField(max_length=255, default="")
	
	def __str__(self):
		return self.uname

class Visitors(models.Model):
	v_id = models.AutoField(primary_key=True)
	v_name = models.CharField(max_length=30, default='')
	v_date = models.DateField()
	v_number = models.CharField(max_length=20, default='')
	v_purpose = models.CharField(max_length=30, default='')

	def __str__(self):
		return self.v_name