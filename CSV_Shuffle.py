import random
fid = open("features.csv", "r")
li = fid.readlines()
fid.close()
print(li)

random.shuffle(li)
print(li)

fid = open("shuffled_features.csv", "w")
fid.writelines(li)
fid.close()