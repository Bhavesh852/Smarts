from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from society.models import Complaints, Visitors
from .models import Vote_Groups, Startvote, Vote_Result, Maintenance, Payment_detail, Recent_Maintenance
from django.views.decorators.csrf import csrf_exempt
import smtplib

# Create your views here.
def index(request):
	return render(request, 'security/index.html')

# secretary login system

def securityLogin(request):
	if request.method == 'POST':
		loginusername = request.POST['loginusername']
		loginpassword = request.POST['loginpassword']

		user = authenticate(username=loginusername, password=loginpassword)

		if user is not None:
			if loginusername=='secretary':
				login(request,user)
				messages.success(request,"Successfully logged In.")
				return redirect('/security/home')
			else:
				messages.error(request,"OOPs you are not a secretary.........")
				return redirect('/security/')
		else:
			messages.error(request,"Invalid credentials, Please try again.")
			return redirect('/security/')

	messages.error(request,"404-not found")
	return render(request, 'security/index.html') 	


def handlelogout(request):
	logout(request)
	messages.success(request,"Successfully logged out.")
	return redirect('/security/')

def home(request):
	b = Maintenance.objects.all()
	no_bil = len(b) #total bill

	rb = Recent_Maintenance.objects.all()
	rno_bil = len(rb) #total recent bill
	
	u = User.objects.all()
	no_u = len(u) - 1 #total user including secretary
	
	v = Visitors.objects.all()
	no_v = len(v) #total visitors
	
	c = Complaints.objects.all()
	no_c = len(c)
	return render(request, 'security/home.html', {'no_bil':no_bil, 'rno_bil':rno_bil, 'no_u':no_u, 'no_v':no_v, 'no_c':no_c})


# ---------------------secretary login end-------------------

# online complaint functionality

def complain(request):
	com = Complaints.objects.all()
	di = {}
	for i in com:
		di[i.uname] = i.flat
	print(di) 
	return render(request, 'security/complain.html', {'complain' : com})

def view(request, myid):
	complain = Complaints.objects.filter(com_id=myid)
	for i in complain:
		if myid == i.com_id:
			mycom = i
	return render(request, 'security/view.html',{'ll' : mycom})

def reply(request, comid):
	rep = Complaints(com_id=comid)
	if request.method == "POST":
		rep.uname = request.POST.get('uname', '')
		rep.flat = request.POST.get('flat', '')
		rep.complaint = request.POST.get('complaint', '')
		rep.reply = request.POST.get('reply', '')
		rep.save()
	cc = Complaints.objects.filter(com_id=comid)
	return render(request, "security/view.html", {'ll':cc[0]})

		
def delete(request, myid):
	complain = Complaints.objects.filter(msg_id=myid)
	complain.delete()
	messages.error(request,"complaint is deleted.")
	return redirect('http://127.0.0.1:8000/security/home/')


# ---------------------complaint end-------------------


# online voting functionality

def voting(request):
	try:
		confirm3 = Startvote.objects.all() #logic for voting is live
		# print(confirm3[0])
		return render(request, 'security/voting.html', { 'y' : confirm3[0]})
	except:
		e = ''
		return render(request, 'security/voting.html', { 'y' : e } )

def group_add(request):
	if request.method=="POST":
		name = request.POST.get('name', '')
		phone = request.POST.get('phone', '')
		state = request.POST.get('state', '')
		city = request.POST.get('city', '')
		address = request.POST.get('address', '')
		dob = request.POST.get('dob', '')
		image = request.FILES['image']
		group = Vote_Groups(name=name, phone=phone, state=state, city=city, address=address, date=dob, image=image)
		group.save()
		messages.success(request,"Successfully Added")
	return render(request, 'security/voting.html')
	
def listgroup(request):
	lgroup = Vote_Groups.objects.all()
	return render(request, 'security/listgroup.html', { 'listgroup' : lgroup })

def groupview(request, myid):
	msg = myid.split(',')
	try:
		listgroup = Vote_Groups.objects.filter(group_id=int(msg[0]))
		ls = Vote_Result.objects.filter(votes=msg[1])
		list_1 = []
		for i in range(len(ls)):
			list_1.append(ls[i])
		length = len(list_1)
		return render(request, 'security/groupview.html',{'listgroup':listgroup[0], 'lists':list_1, 'votes':length})
	except:
		return render(request, 'security/groupview.html',{'listgroup':listgroup[0]})

def delete_group(request, myid):
	listgroup = Vote_Groups.objects.filter(group_id=myid)
	listgroup.delete()
	messages.error(request,"Vote Group is deleted.")
	return redirect('http://127.0.0.1:8000/security/listgroup/')


# ----------------------end Vote_Groups------------------------

# make vote 

def makevote(request):
	try:
		confirm1 = Startvote.objects.all()
		lgroup = Vote_Groups.objects.all()
		return render(request, 'security/makevote.html', { 'listgroup' : lgroup, 'confirm2' : confirm1[0], 'yes' : confirm1[0]})
	except:
		c = ''
		return render(request, 'security/makevote.html', { 'listgroup' : lgroup, 'confirm2' : c, 'yes' : c})

count = 0
def startingvote(request):
	global count
	if request.method=="POST":
		confirm = request.POST.get('confirm')
		con = Startvote(confirmation=confirm)
		print(confirm)
		count = count + 1
		print(count)
		if count <= 1:
			con.save()
			messages.success(request,"Voting Is Now Live")
			
		else:
			messages.error(request,'Voting is already started.., Please end the voting first.....')
	try:
		confirm3 = Startvote.objects.all() #logic for voting is live
		# print(confirm3[0])
		return render(request, 'security/voting.html', {'msg' : count, 'y' : confirm3[0]})
	except:
		e = ''
		return render(request, 'security/voting.html', {'msg' : count, 'y' : e } )
	# return render(request,'security/voting.html' {'msg' : count})

def endvoting(request, msg): 
	try:
		end = Startvote.objects.filter(confirmation=msg)
		ms = str(end[0])
		# print(type(ms))
		# print(ms)
		if ms!=msg:
			messages.error(request,"Voting is not started yet....")
		else:
			end.delete()
			global count
			count = 0 
			messages.success(request,"Voting Is Ended")
	except:
		messages.error(request,'Please start the voting First...')
	return redirect('/security/voting/')

def votecount(request, voter):
	try:
		voter = Vote_Result.objects.all().filter(voter_name=voter)
		v_name = str(voter[0])
		print(v_name)

	except:
		v_name = None
	if request.method=="POST":
		vname = request.POST.get('uname','')
		vvote = request.POST.get('realvote','')
		if vname!=v_name: 
			vv = Vote_Result(voter_name=vname, votes=vvote)
			vv.save()
			messages.success(request,"Thank You For Voting.....")
		else:
			messages.error(request,"You have already voted..")
		if vname=='secretary':
			return redirect('/security/makevote')
		else:
			return redirect('/society/makevote')

def erase(request, msg):
	ls = Vote_Result.objects.filter(votes=msg)
	ls.delete()
	messages.success(request,"Votes erase Successfully")
	return redirect('http://127.0.0.1:8000/security/listgroup')



def v_result(request):
	ls1 = Vote_Result.objects.all()
	list2 = []
	list3 = []
	list4 = []
	for i in range(len(ls1)):
		list2.append(ls1[i])
		list3.append(i)

	for j in range(len(list2)):
		list3[j] = list2[j]
		list4.append(list3[j].votes)
	
	dic = {}
	
	for k in list4:
		dic[k] = dic.get(k,0) + 1
	
	return render(request,'security/v_result.html', {'win' : dic })


# Maintenance system----------------------------------------------------------------------------------------------------------------------------

def main(request):
	return render(request, 'security/main.html') 

def billgenerat(request):
	ls11 = User.objects.all()
	adminn = ls11[0].last_name
	ls5 = []
	ls3 = Maintenance.objects.all()
	for j in ls3:
		ls5.append(j.Flat_no)
	ls5.append('onetime')
	return render(request, 'security/billgenerat.html', {'users' : ls11, 'adm' : adminn, 'ls5' : ls5})

def billform(request, flat):
	lis = User.objects.filter(last_name=flat)
	print(lis)
	return render(request, 'security/billform.html', {'lis1' : lis[0]})

def bilgenrated(request):
	if request.method=='POST':
		bil_date = request.POST.get("billdate", '')
		flat_num = request.POST.get("flatno", '')
		due_date = request.POST.get("duedate", '')
		period_bil = request.POST.get("period", '')
		name_bil = request.POST.get("nname", '')
		
		al_munici_due = request.POST.get("amd", '')
		adminis_generl_expense = request.POST.get("age", '')
		sinking_fund = request.POST.get("sf", '')
		periodic_build_main = request.POST.get("pbm", '')
		comon_area_utility = request.POST.get("cau", '')
		non_ocupation_charg = request.POST.get("noc", '')
		past_areas_contribute = request.POST.get("pac", '')
		interest_due = request.POST.get("intd", '')
		total = int(al_munici_due) + int(adminis_generl_expense) + int(sinking_fund) + int(periodic_build_main) + int(comon_area_utility) + int(non_ocupation_charg) + int(past_areas_contribute) + int(interest_due)

		bill = Maintenance(bill_date=bil_date, Flat_no=flat_num, Due_date=due_date, 
			Period=period_bil, Name=name_bil, All_municiple_due=al_munici_due, 
			Adminis_general_expenses=adminis_generl_expense, Sinking_funds=sinking_fund, 
			Periodic_build_mainten=periodic_build_main, CAU_parking=comon_area_utility, 
			Non_Ocupancy_charg_miscelnous=non_ocupation_charg, Past_areas_contribution=past_areas_contribute, 
			Interest_due=interest_due, Amount=total)
		ls3 = Maintenance.objects.all()
		ls4 = []

		def sendEmail(to, content):
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.login('170020107006ait@gmail.com', 'B@llU7006')
			server.sendmail('170020107006ait@gmail.com', to, content)
			server.close()
			
		for k in ls3:
			ls4.append(k.Flat_no)
		if flat_num not in ls4:
			list_email = User.objects.filter(last_name=flat_num)
			to = 'bchandora60@gmail.com'			#list_email[0].email
			content = "Your Maintenance Bill is generated. You can pay your bill on Smart_Society Portal"
			sendEmail(to, content)
			
			bill.save() #bill generated

			# Generating order id for payments....

			key_id = "rzp_test_1KJUpadoKAOTFI"
			key_secret = "CEqYDDC0cEiYTibAN9JHsMQA"

			import razorpay
			client = razorpay.Client(auth=(key_id, key_secret))

			#checkout part
			data = {
				'amount' : total*100,
				'currency' : "INR",
				'receipt' : "Smart Society",
				'notes' : {
					"name" : name_bil,
					"Payment_for" : "Society Maintenance"
				}
			}

			#server request and get order_id
			order = client.order.create(data=data)
			
			b_no = Maintenance.objects.filter(Flat_no=flat_num)
			print(b_no[0].main_id)

			bill_num = b_no[0].main_id
			bill_name =	name_bil
			flat_number = flat_num
			bill_Date = bil_date
			bill_amount = total
			m_order_id = order['id']
			# print(m_order_id)

			pay = Payment_detail(bill_num=bill_num, bill_name=bill_name, flat_num=flat_number, bill_Date=bill_Date, 
				bill_amount=bill_amount, m_order_id=m_order_id)
			pay.save()

			
			messages.success(request, f'{flat_num} bill has Generated Successfully!...')
		else:
			messages.error(request, f'{flat_num} bill has Already Generated...')
		ls6 = Maintenance.objects.all()
		ls11 = User.objects.all()
		adminn = ls11[0].last_name
		ls5 = []
		
		for j in ls6:
			ls5.append(j.Flat_no)
		ls5.append('onetime')
		return render(request, 'security/billgenerat.html', {'users' : ls11, 'adm' : adminn, 'ls5' : ls5})
	else:
		messages.error(request, 'error')
		return render(request, 'security/billgenerat.html')

def billview(request):
	l1 = Maintenance.objects.all()
	return render(request, 'security/billview.html', { 'l1' : l1 })

def bill(request, mt_id):
	bil = Maintenance.objects.filter(main_id=mt_id)
	return render(request, 'security/bill.html', { 'bil' : bil[0] })

def bilupdate(request, main_id):
	# updating bill 
	b = Maintenance(main_id=main_id)
	if request.method=='POST':
		b.bill_date = request.POST.get("billdate", '')
		b.Flat_no = request.POST.get("flatno", '')
		b.Due_date = request.POST.get("duedate", '')
		b.Period = request.POST.get("period", '')
		b.Name = request.POST.get("nname", '')
		
		b.All_municiple_due = request.POST.get("amd", '')
		b.Adminis_general_expenses = request.POST.get("age", '')
		b.Sinking_funds = request.POST.get("sf", '')
		b.Periodic_build_mainten = request.POST.get("pbm", '')
		b.CAU_parking = request.POST.get("cau", '')
		b.Non_Ocupancy_charg_miscelnous = request.POST.get("noc", '')
		b.Past_areas_contribution = request.POST.get("pac", '')
		b.Interest_due = request.POST.get("intd", '')
		b.Amount = request.POST.get("amt", '')
		b.save()
		list11 = Maintenance.objects.filter(main_id=main_id)
		return redirect('/security/billview/')
	else:
		list11 = Maintenance.objects.filter(main_id=main_id)
		return render(request, 'security/bilupdate.html', { 'bil' : list11[0] })

def recent(request):
	ls11 = User.objects.all()
	adminn = ls11[0].last_name
	ls5 = []
	ls3 = Maintenance.objects.all()
	
	try:	
		for i in ls3:
			con = Recent_Maintenance(rbill_date=i.bill_date, rFlat_no=i.Flat_no, rDue_date=i.Due_date, 
				rPeriod=i.Period, rName=i.Name, rAll_municiple_due=i.All_municiple_due, 
				rAdminis_general_expenses=i.Adminis_general_expenses, rSinking_funds=i.Sinking_funds, 
				rPeriodic_build_mainten=i.Periodic_build_mainten, rCAU_parking=i.CAU_parking, 
				rNon_Ocupancy_charg_miscelnous=i.Non_Ocupancy_charg_miscelnous, rPast_areas_contribution=i.Past_areas_contribution, 
				rInterest_due=i.Interest_due, rAmount=i.Amount)
			con.save()
		messages.success(request, 'All bills added to the recent files...')
	except:
		messages.error(request,'error')
	ls3.delete()
	ls4 = Maintenance.objects.all()
	for j in ls4:
		ls5.append(j.Flat_no)
	ls5.append('onetime')
	return render(request, "security/billgenerat.html", {'users' : ls11, 'adm' : adminn, 'ls5' : ls5})

def recentview(request):
	list1 = Recent_Maintenance.objects.all()
	for i in list1:
		print(i.rFlat_no)
	return render(request, 'security/recentview.html', { 'list1' : list1})

def recentbilview(request, rmt_id): 
	rbil = Recent_Maintenance.objects.filter(rmain_id=rmt_id)
	return render(request, 'security/recentbilview.html', { 'rbil' : rbil[0] })

def visit(request):
	visitors = Visitors.objects.all() 
	return render(request, 'security/visit.html', { 'visitors_' : visitors })

# @csrf_exempt
# def handlerequest(request):
# 	# paytm will send you post request here
# 	pass