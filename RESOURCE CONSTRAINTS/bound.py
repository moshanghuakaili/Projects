import recursive as max_npv
import data 
import math
def initialisation(activity_no,max_time,alpha,max_r,data):
	lb=-9999999
	p=0
	f,ub,CT=max_npv.recursive_calculate_max_npv(activity_no,max_time,alpha,data1)
	print (f)
	print (ub)
	
	for i in CT:
		if i[0]==activity_no and i[1]==1:
			CT.remove(i)
	K=find_resource(max_r,f,max_time,data,activity_no)
	print (CT)
	return K,lb,p,f,ub,CT

def if_K_in_r(K,max_r,max_time):
	for t in range(0,max_time):
	#	print (K[t])
		if(K[t]["resource"]>max_r):
			return t
	return -1

def find_resource(max_r,f,max_time,data,activity_no):
	K=[]
	for t in range(0,max_time):
		count_k_r=0
		k_i=[]
		for i in range(1,activity_no+1):
			if(f[i-1]>t and f[i-1]-data[i-1]["d"]<=t):
				count_k_r=count_k_r+data[i-1]["r"]
				k_i=k_i+[i]
		K=K+[{"resource":count_k_r,"k_i":k_i}]
	#for t in range(0,max_time):
	#	print (K[t])
	return K

def branch_and_bound(activity_no,max_time,alpha,max_r,data):
	K,lb,p,f,ub,CT=initialisation(activity_no,max_time,alpha,max_r,data)
	min_r_t=if_K_in_r(K,max_r,max_time)
	#print(K)
	if(min_r_t==-1):
		print ("resource is enough")
	else:
		f2,lb,data=minimal_DA(K,lb,p,f,ub,CT,min_r_t,data,activity_no,max_time,max_r,alpha)	
		print(f2)
		print(lb)

def minimal_DA(K,lb,p,f,ub,CT,min_r_t,data,activity_no,max_time,max_r,alpha):
	p=p+1
	DS=K[min_r_t]["k_i"]
	MS=[]
	f1=[]
	f_arr=[]
	for i in DS:
		for j in DS:
			if i==j:
				continue
			else:
				MS=MS+[(i,j)]
	for DM in MS:
		#print (f,f1)
		#f1[DM[0]-1]=f1[DM[1]-1]-data[DM[1]-1]["d"]
		#f1=reset_pre(DM[0],data,CT,f1)
		data1=data
		for s in data1[DM[0]-1]["successors"]:
			if s==DM[1]:
				continue
		data1[DM[0]-1]["successors"]=data1[DM[0]-1]["successors"]+[DM[1]]
		data1[DM[1]-1]["predecessors"]=data1[DM[1]-1]["predecessors"]+[DM[0]]
		f1,ub,CT=max_npv.recursive_calculate_max_npv(activity_no,max_time,alpha,data)
		#print("f1after",f1)
		print ("-------",ub,f,DM)
		ub=calculate_ub(activity_no,data,f1,alpha)
		K1=find_resource(max_r,f1,max_time,data,activity_no)
		min_r_t=if_K_in_r(K1,max_r,max_time)
		#print(K1,min_r_t)
		if(min_r_t==-1):
			if(ub>lb):
				lb=ub
		else:
			f2,lb,data=minimal_DA(K1,lb,p,f1,ub,CT,min_r_t,data,activity_no,max_time,max_r,alpha)
			f_arr=f_arr+[{"f":f2,"lb":lb,"data":data}]
	if(f_arr):
		return_f=f_arr[0]["f"]
		return_lb=f_arr[0]["lb"]
		return_data=f_arr[0]["data"]
		for ff in f_arr:
			if(return_lb<ff["lb"]):
				return_lb=ff["lb"]
				return_f=ff["f"]
				return_data=ff["data"]
		return return_f,return_lb,return_data
	else:
		return f1,lb,data
def reset_pre(no,data,CT,f):
	#print ("__",no)
	for i in CT:
		if i[1]==no:
			f[i[0]-1]=f[no-1]-data[no-1]["d"]
			reset_pre(i[0],data,CT,f)
	#print (no,f,CT)
	return f


def calculate_ub(activity_no,data,f,alpha):
	ub=0
	#print(f)
	#print(CT)
	for i in range(1,activity_no+1):
		ub=ub+data[i-1]["c"]*(math.e**(-alpha*f[i-1]))
	return ub


branch_and_bound(9,12,0.01,5,data.data)