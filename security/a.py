ls = [1,2,3,4,5]
ls2 = [1,2]

for i in ls:
	for j in ls2:
		if i == j:
			ls[0]=5
			ls[1]=11
			print(i)
		else:
			ls[0]=1
			ls[2]=2
			print(i)
