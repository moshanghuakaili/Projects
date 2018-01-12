#import data 
import math

def recursion(data,CT,f,CA,no,activity_no,alpha):
	SA1=[no]
	DC1=data[no-1]["c"]*(math.e**(-alpha*f[no-1]))
	CA=mergeCAorSA(CA,[no])
	#print("recursion(",no,")")
	#print("SA1",SA1)
	#print("DC1",DC1)
	#print("CA",CA)
	for j in range(1,activity_no+1):
		if(find_successor_not_in_CA(CA,CT,j,no)==1):
			SA2,DC2,CA,CT,f=recursion(data,CT,f,CA,j,activity_no,alpha)
			#print("------",j,no,DC2,SA2,"")
			if DC2>=0:
				SA1=mergeCAorSA(SA1,SA2)
				DC1=DC1+DC2
			else:
				for p in CT:
					if p[0]==no and p[1]==j:
						CT.remove(p)
				k,l,v=find_min(data,SA2,f,activity_no)
				CT=mergeCTorET(CT,[(k,l)])
				for i in SA2:
					f[i-1]=f[i-1]+v
				#print("---search_current_tree",f)
				search_current_tree(data,CT,f,activity_no,alpha)	
	for m in range(1,activity_no+1):
		if(find_predecessors_not_in_CA(CA,CT,m,no)==1):
			SA2,DC2,CA,CT,f=recursion(data,CT,f,CA,m,activity_no,alpha)
			SA1=mergeCAorSA(SA1,SA2)
			DC1=DC1+DC2
	#print("finishrecursion(------",no,DC1,SA1,"")
	return SA1,DC1,CA,CT,f
def find_predecessors_not_in_CA(CA,CT,j,no):
	flag_j=0;
	#print ("finddpre",j,no,CA)
	for i in CA:
		if i==j:
			flag_j=1
	if(flag_j==0):
		for c in CT:
			if(c[0]==j and c[1]==no):
				return 1
	return 0
def mergeCAorSA(A,B):
	for b in B:
		flag_b=0
		for a in A:
			if a==b:
				flag_b=1
				break
		if(flag_b==0):
			A=A+[b]
	return A
def mergeCTorET(A,B):
	for b in B:
		flag_b=0
		for a in A:
			if a[0]==b[0] and a[1]==b[0]:
				flag_b=1
				break
		if(flag_b==0):
			A=A+[b]
	return A
def find_min(data,SA,f,activity_no):
	min=9999999
	i=0
	j=0
	for k in range(2,activity_no+1):
		for l in range(2,activity_no+1):
			if k==l:
				continue
			else:
				flag_k=0
				flag_l=0
				for m in SA:
					#print("       ",m)
					if m==k:
						flag_k=1
					if m==l:
						flag_l=1
				if flag_k==1 and flag_l==0: 
					for p in data[k-1]["successors"]:
						if(l==p):
							v=f[l-1]-data[l-1]["d"]-f[k-1]
							#print("                    ",k,l,v)
							if(v<min):
								min=v
								i=k
								j=l
	if(min==9999999):
		min=0
	#print("findmin_",SA,i,j,min)
	return i,j,min
def find_successor_not_in_CA(CA,CT,j,no):
	flag_j=0;
	for i in CA:
		if i==j:
			flag_j=1
	if(flag_j==0):
		for c in CT:
			if(c[0]==no and c[1]==j):
				return 1
	return 0
def search_current_tree(data,CT,f,activity_no,alpha):
	CA=[]
	SA1,DC1,CA,CT,f=recursion(data,CT,f,CA,1,activity_no,alpha)
	return SA1,DC1,CA,CT,f
def construct_early_tree(data,ET,f,activity_no):
	#print ("construct_early_tree")
	for j in range(2,activity_no):
		f[j-1]=0
		get_i=0
		for i in data[j-1]["predecessors"]:
			if f[i-1]+data[j-1]["d"]>f[j-1]:
				f[j-1]=f[i-1]+data[j-1]["d"]
				get_i=i;
		ET=mergeCTorET(ET,[(get_i,j)])
	# for i in ET:
	#  	print (i,"\n")
	# for i in f:
	# 	print (i,"\n")
	return ET,f
def construct_current_tree(data,CT,ET,f,max_time,activity_no):
	#print ("construct_current_tree")
	f[activity_no-1]=max_time
	CT=ET
	CT=mergeCTorET(CT,[(activity_no,1)])
	
	j=activity_no-1
	while(j>1):
		# node with negative cash flow  
		if data[j-1]["c"]<0:
			# find if exist a successor
			flag_s=0
			for p in CT:
				# if exist
				if p[0]==j:
					flag_s=1
					break
			# if not
			if(flag_s==0):
				f[j-1]=100
				get_i=0
				for i in data[j-1]["successors"]:
					if f[i-1]-data[i-1]["d"]<f[j-1]:
						f[j-1]=f[i-1]-data[i-1]["d"]
						get_i=i
				CT=mergeCTorET(CT,[(j,get_i)])
				for p in CT:
					if p[1]==j:
						CT.remove(p)		
		j=j-1
	# for i in CT:
	#  	print (i,"\n")
	# for i in f:
	# 	print (i,"\n")	
	#CT=CT+[(8,9)]
	return CT,f
def recursive_calculate_max_npv(activity_no,max_time,alpha,data):
	f=[0]*activity_no
	ET=[]
	CT=[]
	ET,f=construct_early_tree(data,ET,f,activity_no)
	CT,f=construct_current_tree(data,CT,ET,f,max_time,activity_no)
	SA,DC,CA,CT,f=search_current_tree(data,CT,f,activity_no,alpha)
	DCC=0
	#print(f)
	#print(CT)
	for i in range(1,activity_no+1):
		DCC=DCC+data[i-1]["c"]*(math.e**(-alpha*f[i-1]))
	#print (DCC)
	return f,DCC,CT

#f,DC,CT=recursive_calculate_max_npv(9,20,0.01,data.data1)
