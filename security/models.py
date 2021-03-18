from django.db import models

# Create your models here.

class Vote_Groups(models.Model):
	group_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=70)
	phone = models.CharField(max_length=50, default="")
	state = models.CharField(max_length=50, default="")
	city = models.CharField(max_length=50, default="")
	address = models.CharField(max_length=80, default="")
	date = models.DateField()
	image = models.ImageField(upload_to="security/images")
	
	def __str__(self):
		return self.name


class Startvote(models.Model):
	start_id = models.AutoField(primary_key=True)
	confirmation = models.CharField(max_length=50, default="")

	def __str__(self):
		return self.confirmation

class Vote_Result(models.Model):
	voter_id = models.AutoField(primary_key=True)
	voter_name = models.CharField(max_length=70, default="")
	votes = models.CharField(max_length=10, default="") 

	def __str__(self):
		return self.voter_name

class Maintenance(models.Model):
	main_id = models.AutoField(primary_key=True)
	bill_date = models.DateField()
	Flat_no = models.CharField(max_length=10, default='')
	Due_date = models.DateField()
	Period = models.CharField(max_length=30, default='')
	Name = models.CharField(max_length=70)
	
	All_municiple_due = models.CharField(max_length=20, default='')
	Adminis_general_expenses = models.CharField(max_length=20, default='')
	Sinking_funds = models.CharField(max_length=20, default='')
	Periodic_build_mainten = models.CharField(max_length=20, default='')
	CAU_parking = models.CharField(max_length=20, default='')
	Non_Ocupancy_charg_miscelnous = models.CharField(max_length=20, default='')
	Past_areas_contribution = models.CharField(max_length=20, default='')
	Interest_due = models.CharField(max_length=20, default='')
	Amount = models.IntegerField(default=0)

	def __str__(self):
		return self.Flat_no

class Payment_detail(models.Model):
	p_id = models.AutoField(primary_key=True)
	bill_num = models.IntegerField(default=0)
	bill_name = models.CharField(max_length=70, default="")
	flat_num = models.CharField(max_length=50, default="")
	bill_Date = models.DateField()
	bill_amount = models.IntegerField(default=0)
	m_order_id = models.CharField(max_length=100, default="")
	m_payment_id = models.CharField(max_length=100, default="")
	m_razorpay_signature = models.CharField(max_length=150, default="")

class Recent_Maintenance(models.Model):
	rmain_id = models.AutoField(primary_key=True)
	rbill_date = models.DateField()
	rFlat_no = models.CharField(max_length=10, default='')
	rDue_date = models.DateField()
	rPeriod = models.CharField(max_length=30, default='')
	rName = models.CharField(max_length=70)
		
	rAll_municiple_due = models.CharField(max_length=20, default='')
	rAdminis_general_expenses = models.CharField(max_length=20, default='')
	rSinking_funds = models.CharField(max_length=20, default='')
	rPeriodic_build_mainten = models.CharField(max_length=20, default='')
	rCAU_parking = models.CharField(max_length=20, default='')
	rNon_Ocupancy_charg_miscelnous = models.CharField(max_length=20, default='')
	rPast_areas_contribution = models.CharField(max_length=20, default='')
	rInterest_due = models.CharField(max_length=20, default='')
	rAmount = models.IntegerField(default=0)

	def __str__(self):
		return self.rFlat_no
