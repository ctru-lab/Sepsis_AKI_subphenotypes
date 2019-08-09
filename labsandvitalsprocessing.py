import pandas as pd
import csv
import math
import statistics

vital_conversion = {}
df = pd.read_csv("Modified Chart Features.csv")
for name in list(df):
	for row in df[name]:
		try:
			#if name == "Misc":
			#	vital_conversion[row] = row
			if math.isnan(row):
				pass
		except:
			vital_conversion[row] = name


subjects = pd.read_csv("martin_creattime_dates.csv")
subject_ids = subjects.iloc[:,2].unique()
# features = {el:{} for el in subject_ids}
# #print(features)



itemids = []
with open("martin_akipatients_chart_extended_5.csv", "r") as f:
	reader = csv.reader(f, delimiter=" ")
	for i, line in enumerate(reader):
		if (i == 0):
			pass
		else:
			itemids.append(line[3])
f.close()
itemids = list(set(itemids))

# #items = {int(el):[] for el in itemids[20:21]}
vitalsfeatures = {int(el):{el:[] for el in itemids} for el in subject_ids}

with open("martin_akipatients_chart_extended_5.csv", "r") as f:
	reader = csv.reader(f, delimiter=" ")
	for i, line in enumerate(reader):
		if (i == 0):
			print(line)
		else:
			try:
				vitalsfeatures[int(line[0])][line[3]].append(int(line[4]))
			except:
				pass
f.close()
#print(features)
#values will be stored as mean, median, mode, std,n
import statistics
vitalscleaned_features = {el:{el:[] for el in list(df)} for el in subject_ids}

for k, v in vitalsfeatures.items():
	for k2, v2 in vitalsfeatures[k].items():
		if len(v2) == 0:
			pass
		elif len(v2) == 1:
			#mean, median, mode, std, n
			vitalscleaned_features[k][vital_conversion[k2]] = [v2[0], 'NA', 1]
		elif vitalscleaned_features[k][vital_conversion[k2]] == [] or vitalscleaned_features[k][vital_conversion[k2]][2] == 1:
			#mean, median, mode, std, n
			vitalscleaned_features[k][vital_conversion[k2]] = [statistics.median(v2), statistics.stdev(v2),len(v2)]
			
		else:
			pass

header = ['id']
for name in list(df):
	header.append(name + "_median")
	header.append(name + "_std")
	header.append(name + "_n")

with open('vitals.tsv', mode='w', newline='') as vital_file:
	writer = csv.writer(vital_file, delimiter='\t', lineterminator='\n')
	writer.writerow(header)
	for k, v in vitalscleaned_features.items():
		row = [str(k)]
		for k2, v2 in vitalscleaned_features[k].items():
			if len(v2) == 0:
				row.append('NA')
				row.append('NA')
				row.append('NA')
			else:
				row.append(v2[0])
				row.append(v2[1])
				row.append(v2[2])
		#print(row)
		writer.writerow(row)



labsids = [] 

with open("LABEVENTS.csv", "r", newline='') as f:
	reader = csv.reader(f, delimiter="\t")
	for i, line in enumerate(reader):
		if (i == 0):
			print(line)
		else:
			labsids.append(line[3])
f.close()
labsids = list(set(labsids))
print(labsids)

labfeatures = {int(el):{el:[] for el in labsids} for el in subject_ids}

with open("LABEVENTS.csv", "r") as f:
	reader = csv.reader(f, delimiter="\t", lineterminator='\n')
	for i, line in enumerate(reader):
		if (i == 0):
			print(line)
		else:
			try:
				labfeatures[int(line[1])][line[3]].append(int(line[6]))
			except:
				pass
f.close()

labcleaned_features = {el:{el:[] for el in labsids} for el in subject_ids}

for k, v in labfeatures.items():
	for k2, v2 in labfeatures[k].items():
		if len(v2) == 0:
			pass
		elif len(v2) == 1:
			#mean, median, mode, std, n
			labcleaned_features[k][k2] = [v2[0], 'NA', 1]
		elif labcleaned_features[k][k2] == [] or labcleaned_features[k][k2][2] == 1:
			#mean, median, mode, std, n
			labcleaned_features[k][k2] = [statistics.median(v2), statistics.stdev(v2),len(v2)]
			
		else:
			pass

header = ['id']
for items in labsids:
	header.append(items + "_median")
	header.append(items + "_std")
	header.append(items + "_n")

with open('labs.tsv', mode='w', newline='') as lab_file:
	writer = csv.writer(lab_file, delimiter='\t', lineterminator='\n')
	writer.writerow(header)
	for k, v in labcleaned_features.items():
		row = [str(k)]
		for k2, v2 in labcleaned_features[k].items():
			if len(v2) == 0:
				row.append('NA')
				row.append('NA')
				row.append('NA')
			else:
				row.append(v2[0])
				row.append(v2[1])
				row.append(v2[2])
		#print(row)
		writer.writerow(row)


####don't need to merge just need to save features dicts to csv then gucci