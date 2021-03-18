from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Contact, Complaints, Visitors
from security.models import Startvote, Vote_Groups, Maintenance, Payment_detail, Recent_Maintenance
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
	return render(request, 'society/index.html')

def about(request):
	return render(request, 'society/about.html')



def handlesignup(request):

 	if request.method == 'POST':
 		# get parameters
 		username = request.POST['username']
 		fname = request.POST['fname']
 		lname = request.POST['lname']
 		email = request.POST['email']
 		pass1 = request.POST['pass1']
 		pass2 = request.POST['pass2']


 		# checks for errror input
 		if len(username) > 10:
 			messages.error(request,"Username must be under 10 charactor.")
 			return redirect('/society/')

 		if pass1 != pass2:
 			messages.error(request,"password do not same.")
 			return redirect('/society/')

 		# Create user
 		myuser = User.objects.create_user(username, email, pass1)
 		myuser.first_name = fname
 		myuser.last_name = lname
 		myuser.save()
 		messages.success(request,"your account has been created successfully.")
 		return redirect('/society/')

 	else:
 		return HttpResponse("404-Not Found")

def handlelogin(request):
	if request.method == 'POST':
		loginusername = request.POST['loginusername']
		loginpassword = request.POST['loginpassword']

		user = authenticate(username=loginusername, password=loginpassword)

		if user is not None:
			login(request,user)
			messages.success(request,"Successfully logged In.")
			return redirect('/society/home/',loginusername)
		else:
			messages.error(request,"Invalid credentials, Please try again.")
			return redirect('/society/')
	return HttpResponse("404-not found")


def handlelogout(request):
	logout(request)
	messages.success(request,"Successfully logged out.")
	return redirect('/society/')

def contact(request):
	if request.method=="POST":
		name = request.POST.get('name', '')
		email = request.POST.get('email', '')
		phone = request.POST.get('phone', '')
		msg = request.POST.get('msg', '')
		contact = Contact(name=name, email=email, phone=phone, msg=msg)
		contact.save()

		messages.success(request,"Message send successfully.")
		return redirect('/society/')
	else:
		return render(request, 'society/contact.html')

def home(request):
	try:
		confirm1 = Startvote.objects.all() #logic for voting is live
		return render(request, 'society/home.html', { 'yes' : confirm1[0]})
	except:
		c = ''
		return render(request, 'society/home.html', { 'yes' : c } )



def complaint(request):
	if request.method=="POST":
		name = request.POST.get('uname','')
		flat = request.POST.get('flat','')
		complaint = request.POST.get('complaint','')
		complaints = Complaints(uname=name, flat=flat, complaint=complaint)
		complaints.save()
		com = Complaints.objects.all()
		return render(request,'society/complaint.html', { 'com' : com })
	else:
		try:
			com = Complaints.objects.all()
			confirm1 = Startvote.objects.all() #logic for voting is live
			return render(request, 'society/complaint.html', { 'yes' : confirm1[0], 'com' : com })
		except:
			c = ''
			return render(request, 'society/complaint.html', { 'yes' : c, 'com' : com } )

def makevote(request):
	try:
		confirm1 = Startvote.objects.all()
		lgroup = Vote_Groups.objects.all()
		return render(request, 'society/makevote.html', { 'listgroup' : lgroup, 'confirm2' : confirm1[0], 'yes' : confirm1[0]})
	except:
		c = ''
		return render(request, 'society/makevote.html', { 'listgroup' : lgroup, 'confirm2' : c, 'yes' : c})

def maintenance(request):
	try:
		ls1 = User.objects.filter(username = request.user)
		confirm1 = Startvote.objects.all()
		return render(request, "society/maintenance.html", { 'ls1' : ls1[0], 'confirm2' : confirm1[0], 'yes' : confirm1[0] })
	except:
		c = ''
		return render(request, "society/maintenance.html", { 'ls1' : ls1[0], 'confirm2' : c, 'yes' : c})

def paybill(request, mynum):
	try:
		ls2 = Maintenance.objects.filter(Flat_no = mynum)
		ls3 = Payment_detail.objects.filter(flat_num= mynum)
		for i in ls3:
			# print(i)
			if ls2[0].main_id == i.bill_num:
				orderid = i.m_order_id
		confirm1 = Startvote.objects.all()
		return render(request, "society/paybill.html", { 'ls2' : ls2[0],'ls3' : ls3[0], 'confirm2' : confirm1[0], 'yes' : confirm1[0], 'order' : orderid })
	except:
		try:
			ls2 = Maintenance.objects.filter(Flat_no = mynum)
			ls3 = Payment_detail.objects.filter(flat_num= mynum)
			for i in ls3:
				if ls2[0].main_id == i.bill_num:
					orderid = i.m_order_id
			
			c = ''
			return render(request, "society/paybill.html", { 'ls2' : ls2[0], 'ls3': ls3[0], 'confirm2' : c, 'yes' : c, 'order' : orderid})
		except:
			c = ''
			messages.error(request, 'Your maintenance bill is not generated...')
			return render(request, "society/paybill.html", { 'confirm2' : c, 'yes' : c})


def recentbil(request, myflat):
	try:
		l11 = Recent_Maintenance.objects.filter(rFlat_no = myflat)
		confirm1 = Startvote.objects.all()
		return render(request, 'society/recentbil.html', { 'l1' : l11, 'confirm2' : confirm1[0], 'yes' : confirm1[0] })
	except:
		try:
			l11 = Recent_Maintenance.objects.filter(rFlat_no = myflat)
			c = ''
			return render(request, 'society/recentbil.html', { 'l1' : l11, 'confirm2' : c, 'yes' : c })
		except:
			c = ''
			messages.error(request, 'You have no recent bills...')
			return render(request, 'society/recentbil.html', { 'confirm2' : c, 'yes' : c})

def rbilview(request, rmt_id):
	try:
		rbil = Recent_Maintenance.objects.filter(rmain_id=rmt_id)
		confirm1 = Startvote.objects.all()
		return render(request, 'society/rbilview.html', { 'rbil' : rbil[0], 'confirm2' : confirm1[0], 'yes' : confirm1[0] })
	except:
		c = ''
		return render(request, 'society/rbilview.html', { 'rbil' : rbil[0], 'confirm2' : c, 'yes' : c})

def visitor(request):
	if request.method == "POST":
		vname = request.POST.get('vname', '')
		vdate = request.POST.get('vdate', '')
		vnumber = request.POST.get('vnum', '')
		vpurpose = request.POST.get('vpurpose', '')

		v_data = Visitors(v_name=vname, v_date=vdate, v_number=vnumber, v_purpose=vpurpose)
		v_data.save()
		messages.success(request, 'Thank you for your data........Enjoy :)')
		return render(request, 'society/visitor.html')
	else:
		return render(request, 'society/visitor.html')
