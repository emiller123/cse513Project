#!/usr/bin/python

# EXAMPLE FORMAT
# 
# State: 51 variables: one for each state plus the District of Columbia
# Sex: 2 variables: one for male, one for female.
# Race: 6 variables: White alone, Black/African American alone, 
#		American Indian/Alaska Native alone, Asian alone, 
#		Native Hawaiian/Other Pacific Islander alone, two or more races
# Age: 86 variables: one for each of ages 0-84, and 85+
# 
# | State     |	Sex 		| Race 		 | Age 			|
# | [x0 - x50]| [x51 - x52]	| [x53 - x58]| [x59 - x144] |

import census_reader
import random


class Oracle:
	def __init__(self):
		self.posteriors = census_reader.compute_posteriors()
		attrfile = open('census_attributes', 'rb')
		self.attributes = dict((line.split("\t")[0], line.rstrip().split("\t")[1]) for line in attrfile.readlines() if "#" not in line)
		attrfile.close()
	# Returns partial example given by masking_function
	def partial_example(self, masking_function, param):
 		return masking_function(self.example(), param)

 	# Returns example of the form <# true attributes> <true attr index 1> <true attr index 2> ...
 	# Examples are generated from the distributions on state, sex, race, and age from the 2015 
 	# census records.
 	def example(self):
 		
 		rand = random.random()
 		upto = 0.0
 		for state, data in self.posteriors.items():
 			if state != "pop":
 				if upto + float(data["post"]) >= rand:
 					example_state = state
 					example_state_attr = self.attributes["STATE_{0}".format(state)]
 					break
 				upto += float(data["post"])

 		rand = random.random()
 		upto = 0.0
 		for sex, data in self.posteriors[example_state].items():
 			if sex != "pop" and sex != "post":
 				if upto + float(data["post"]) >= rand:
 					example_sex = sex
 					example_sex_attr = self.attributes["SEX_{0}".format(sex)]
 					break
 				upto += float(data["post"])

 		rand = random.random()
 		upto = 0.0
 		for race, data in self.posteriors[example_state][example_sex].items():
 			if race != "pop" and race != "post":
 				if upto + float(data["post"]) >= rand:
 					example_race = race
 					example_race_attr = self.attributes["RACE_{0}".format(race)]
 					break
 				upto += float(data["post"])

 		rand = random.random()
 		upto = 0.0
 		for age, data in self.posteriors[example_state][example_sex][example_race].items():
 			if age != "pop" and age != "post":
 				if upto + float(data["post"]) >= rand:
 					example_age = age
 					example_age_attr = self.attributes["AGE_{0}".format(age)]
 					break
 				upto += float(data["post"])
 		example = list("0" for i in range(0,145))
 		example[int(example_state_attr)] = "1"
 		example[int(example_sex_attr)]= "1"
 		example[int(example_race_attr)] = "1"
 		example[int(example_age_attr)] = "1"
 		return example

# MASKING FUNCTIONS

# Returns the original example without any attribute masking. Param not used.
def mask_full_example(example, param):
	return "".join(example)

# Obscures an attribute with [0,1] probability given by param 
def mask_random(example, param):
	if param < 0 or param > 1:
		print "Invalid parameter given"
		return None
	for indx, attr in enumerate(example):
		if random.random() < param:
			example[indx] = "*"
	return "".join(example)

# Obscures the entire state, sex, race, or age field with [0,1] probability given by param.
def mask_random_attr(example, param):
	if param < 0 or param > 1:
		print "Invalid parameter given"
		return None

	# State
	if random.random() < param:
		for i in range(0,51):
			example[i] = "*"
	# Sex
	if random.random() < param:
		for i in range(51,53):
			example[i] = "*"

	# Race
	if random.random() < param:
		for i in range(53, 59):
			example[i] = "*"

	# Age
	if random.random() < param:
		for i in range(59, 145):
			example[i] = "*"

	return "".join(example)

# Obscures the entire state, sex, race, or age field, as dictated by param, which takes values 0-3,
# corresponding to the fields in the given order.
def mask_attr(example, param):
	# State
	kb = open('KB', 'a')
	if param == 0:
		for i in range(0,51):
			example[i] = "*"
			# kb.write(str(i))
			for j in range(i,51):
				if j != i:
					kb.write(str(-(i+1)))
					kb.write(" ")
					kb.write(str(-(j+1)))
					kb.write(" ")
					kb.write(str(0))
					kb.write("\n")
	# Sex
	elif param == 1:
		for i in range(51,53):
			example[i] = "*"
			for j in range(i,53):
				if j != i:
					kb.write(str(-(i+1)))
					kb.write(" ")
					kb.write(str(-(j+1)))
					kb.write(" ")
					kb.write(str(0))					
					kb.write("\n")			
	# Race
	elif param == 2:
		for i in range(53, 59):
			example[i] = "*"
			for j in range(i,59):
				if j != i:
					kb.write(str(-(i+1)))
					kb.write(" ")
					kb.write(str(-(j+1)))
					kb.write(" ")
					kb.write(str(0))					
					kb.write("\n")			
	# Age
	elif param == 3:
		for i in range(59, 145):
			example[i] = "*"
			for j in range(i,145):
				if j != i:
					kb.write(str(-(i+1)))
					kb.write(" ")
					kb.write(str(-(j+1)))
					kb.write(" ")
					kb.write(str(0))					
					kb.write("\n")			

	else:
		print "Invalid paramater given"
		return None
	return "".join(example)


def main():
	oracle = Oracle()
	f = open('workfile', 'w')
	for i in range(1,2):
		# print oracle.partial_example(mask_attr, 0)
		f.write(oracle.partial_example(mask_attr, 3))
		f.write("\n")




if __name__=="__main__":
	main()