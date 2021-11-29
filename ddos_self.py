import subprocess as sp
import csv
import time
import datetime


while(True):
	st1 = time.time()
	output = ""
	no_of_ports = set()
	print("getting flows from switches for 5 secs")
	for x in range(5):
		output = sp.getoutput('ovs-ofctl dump-flows s1')
		output += sp.getoutput('ovs-ofctl dump-flows s2')
		output += sp.getoutput('ovs-ofctl dump-flows s3')
		time.sleep(1)

	dt1 = time.time()	
	print(dt1-st1)
	time_taken = dt1-st1
	print ("gettings flows from switches for 5 secs is done--------------------")

	#nlines = output.count('\n')

	#header for csv file
	header = ['TimeStamp','Duration of flow','no of packets','no of bytes','ports','src_ip','dst_ip']

	with open('flows.csv', 'a+', encoding='UTF8') as f:
		writer = csv.writer(f)
		#writer.writerow(header)
		duration_of_flows = []
		packets_of_flows = []
		bytes_of_flows = []
		lines = output.split('\n')
		final_list = []
		temp_str = ""
		list1 = []
		list2 = []
		list3 = []
		list4 = []
		src = ""
		dst = ""
		for i in range(1,len(lines)):
			st = datetime.datetime.now()
			temp_list = []
			temp_list.append(st)
			temp = lines[i].split(",")
			#for j in range(len(temp)):
			if temp.count('icmp') > 0 :
				temp_split = temp[1].split("=")
				temp_str = temp_split[-1]
				if(temp_str[-1] == 's'):
					temp_str = temp_str[:-1]
				else:
					temp_str = temp_str.split(".",1)
				temp_list.append(temp_str[0])
				duration_of_flows.append(temp_str[0])
				temp_split = temp[3].split("=")
				temp_list.append(temp_split[-1])
				packets_of_flows.append(temp_split[-1])
				temp_split = temp[4].split("=")
				temp_list.append(temp_split[-1])
				bytes_of_flows.append(temp_split[-1])
				temp_split = temp[9].split("=")
				temp_list.append(temp_split[-1])
				no_of_ports.add(temp_split[-1])
				temp_split = temp[-4].split("=")
				src = temp_split[-1]
				temp_list.append(temp_split[-1])
				temp_split = temp[-5].split("=")
				dst = temp_split[-1]
				temp_list.append(temp_split[-1])
				list1.append(src)
				list2.append(dst)
				final_list.append(temp_list)
				writer.writerow(temp_list)
				
				
	#------------------------------------------------------------------------------------------------------------------------------
		
		feature_list = []
		no_of_flows = len(duration_of_flows)
		print(f'No of flows are {no_of_flows}')
		avg_duration = 0
		total_duration = 0
		for k in duration_of_flows:
			total_duration += int(k)
		print(no_of_flows)
		if (no_of_flows % 2 == 0):
			#avg_duration = (((total_duration/no_of_flows)*(no_of_flows/2)) + ((total_duration/no_of_flows)*((no_of_flows+1)/2)))/2
			#avg_duration = total_duration*((no_of_flows+1)/2)
			avg_duration = total_duration/no_of_flows
		else:
			#avg_duration = total_duration*((no_of_flows+1)/2)
			avg_duration = total_duration/no_of_flows
		print(avg_duration)
		#print(final_list)
		feature_list.append(avg_duration)
	#---------------------------------------------------------------------------------------------------------------------------------


		avg_packets = 0
		total_packets = 0
		for k in packets_of_flows:
			total_packets += int(k)
		avg_packets = total_packets/no_of_flows
		print(avg_packets)
		feature_list.append(avg_packets)
	#---------------------------------------------------------------------------------------------------------------------------------

		avg_bytes = 0
		total_bytes = 0
		for k in bytes_of_flows:
			total_bytes += int(k)
		avg_bytes = total_bytes/no_of_flows
		print(avg_bytes)
		feature_list.append(avg_bytes)
		
	#---------------------------------------------------------------------------------------------------------------------------------
		count_match = 0
		#list3 = list2
		#list4 = list1
		#for i,j in zip(list1,list2):
		#	temp_add_list = i +' '+j
		#	for a,b in zip(list3,list4):
		#		temp_add_list_check = a +' '+b
		#		if (temp_add_list == temp_add_list_check):
		#			count_match += 1
		#			list3.remove(a)
		#			list4.remove(b)
		#count_match = count_match/2
		#print(f'The value of pair flows is {count_match}.')
		#percentage_of_pair_flows = (2*count_match)/no_of_flows
		#print(f'The value of pair flows is {percentage_of_pair_flows}.')
		#print(list1,list2,list3,list4)
		feature_list.append(0)
	#------------------------------------------------------------------------------------------------------------------------------------

		twice_of_flows = 2*count_match
		gsf = (no_of_flows - twice_of_flows)/time_taken
		print(gsf)
		feature_list.append(gsf)
	#------------------------------------------------------------------------------------------------------------------------------------

		#print(len(no_of_ports))
		gdp = len(no_of_ports)/time_taken
		print(f'Growth of different ports {gdp}.')
		feature_list.append(gdp)
		feature_list.append(1)
		with open('ddos_flows.csv', 'a+', encoding='UTF8') as featureSet:
			writeFeature = csv.writer(featureSet)
			writeFeature.writerow(feature_list)
		time.sleep(10)
