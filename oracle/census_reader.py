#!/usr/bin/python

# The format for records from census.csv can be found here:
# https://www.census.gov/popest/data/state/asrh/2015/files/SC-EST2015-ALLDATA6.pdf


import sys

csv_infile_path = "./census.csv"
csv_has_header = 1

# Processes 
class CSVReader:

	def __init__(self, infile, headerflag):
		self.file = open(infile, 'rb')
		self.headerflag = headerflag
		# If CSV has a format header at the top, ignore it
		if self.headerflag:
			self.file.readline()



def compute_posteriors():

	posteriors = {"pop":0}
	global csv_infile_path
	global csv_has_header
	reader = CSVReader(csv_infile_path, csv_has_header)

	if reader.file:
		line = "empty"
		# Read csv file and put useful fields in dictionary
		while line:
			line = reader.file.readline()
			if line:
				record = line.split(",")
				state = record[3]
				sex = record[5]
				race = record[7]
				age = record[8]
				
				# Ignore the aggregate records for sexes and origin
				if sex == "0" or record[6] == "0":
					continue
				population_2015 = float(record[16])
				#print "{0}\t{1}\t{2}\t{3}\t{4}\n".format(state, sex, race, age, population_2015)
				if state not in posteriors:
					posteriors[state] = {"post":0, "pop":0}
				if sex not in posteriors[state]:
					posteriors[state][sex] = {"post":0, "pop":0}
				if race not in posteriors[state][sex]:
					posteriors[state][sex][race] = {"post":0, "pop":0}
				if age not in posteriors[state][sex][race]:
					posteriors[state][sex][race][age] = {"post":0, "pop":0}
				posteriors[state][sex][race][age]["pop"] += population_2015

		reader.file.close()
		# Fill in aggregate population data
		total_population_state = 0.0
		for state, sex_dict in posteriors.items():
			if state != "post" and state != "pop":
				total_population_sex = 0.0
				for sex, race_dict in sex_dict.items():
					if sex != "post" and sex != "pop":
						total_population_race = 0.0
						for race, age_dict in race_dict.items():
							if race != "post" and race != "pop":
								total_population_age = 0.0
								for age, stats in age_dict.items():
									if age != "post" and age != "pop":
										total_population_age += stats["pop"]
								age_dict["pop"] = total_population_age
								total_population_race += total_population_age
						race_dict["pop"] = total_population_race
						total_population_sex += total_population_race
				sex_dict["pop"] = total_population_sex
				total_population_state += total_population_sex
		posteriors["pop"] = total_population_state
					
		# Generate posterior distributions from dictionary
		for state, sex_dict in posteriors.items():
			if state != "post" and state != "pop":
				for sex, race_dict in sex_dict.items():
					if sex != "post" and sex != "pop":
						for race, age_dict in race_dict.items():
							if race != "post" and race != "pop":
								for age, stats in age_dict.items():
									if age != "post" and age != "pop":
										stats["post"] = stats["pop"]/age_dict["pop"]
								age_dict["post"] = age_dict["pop"]/race_dict["pop"]
						race_dict["post"] = race_dict["pop"]/sex_dict["pop"]
				sex_dict["post"] = sex_dict["pop"]/posteriors["pop"]

		return posteriors
	else:
		print "Invalid file path"


if __name__=="__main__":
	compute_posteriors()