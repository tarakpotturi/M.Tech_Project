import csv
reader = csv.reader(open("features_normal.csv"))
reader1 = csv.reader(open("ddos_flows.csv"))
f = open("features.csv", "w")
writer = csv.writer(f)

for row in reader:
    writer.writerow(row)
for row in reader1:
    writer.writerow(row)
f.close()