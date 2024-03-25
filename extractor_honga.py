#------------------------------------------------------------------------------
#This extractor is used to extract the Total War unit statistics from
#http://www.honga.net/totalwar/
#
#It currently works for the following game pages:
#Three Kingdoms
#Britannia
#Attila
#Rome II
#Shogun 2
#
#Still need to work on the following:
#Napoleon / Empire (very different input)
#
#------------------------------------------------------------------------------

import copy
import csv
import datetime
import glob
import numpy
import os
import pandas
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


def appendIncNumToStr(list1, list2, list3, dict1, dict2, index):
	list1.append(list2[index] + ' ' + str(dict1.get(dict2[list3[0]])))

def appendSoupValuesToList(list, input_data):
	for x in range(len(input_data)):
		list.append(input_data[x].text)
	#[input_data[x].text for x in range(len(input_data))]

def checkForKey(dict, key):
	if key in dict.keys():
		value = True
	else:
		value = False
	return value

def checkListForDuplicates(list):
	value = False
	if len(list) == len(set(list)):
		pass
	else:
		value = True
	return value

def convertListValuesToInt(list):
	for x in range(len(list)):
		list[x] = int(list[x])

def generateArrayForUnitStats(length, entries, array):
	array_begin = 0
	length_each_entry_temp = length
	for iterations in range(entries):
		working_array = [*range(array_begin, length_each_entry_temp)][2:]
		array_begin += length
		length_each_entry_temp += length
		array.append(working_array)

def getDictKey(dict, index):
	value = list(dict.keys())[index]
	return value

def getDictKeyAndValue(dict, index):
	value = list(dict.items())[index]
	return value

def getDictValue(dict, index):
	value = dict.get(list(dict.keys())[index])
	return value

def listRange(index, input):
	value = list(range(index,len(input)))
	return value

def printAsList(input, index):
	print('\t' + str(index+1) + '. ' + input[index])

def printSoupAsList(text, list):
	print('\n' + text + ':')
	for x in range(len(list)):
		print (list[x].text)

def removeCharactersFromString(list, characters):
	for x in characters:
		for y in range(len(list)):
			list[y] = list[y].replace(x, '')

def unitStatisticsToList(array, entries, list, stats):
	stat_array_single_length = len(array[0])
	for x in range(stat_array_single_length):
		for i in range(entries):
			list[i][x] = (stats[list[i][x]].text)

def getIndexofDupKey(dict, list1, index):
	x = list(dict.items())
	value = [idx for idx, key in enumerate(x) if key[0] == str(list1[index])]
	return value


#------------------------------------------------------------------------------
#STEP 0: Set conditions for extraction
#------------------------------------------------------------------------------


print('\nThis extractor is used to extract Total War unit statistics from')
print('http://www.honga.net/totalwar/')
print('\nIt currently works for the following game pages:')
print('Three Kingdoms\nBritannia\nAttila\nRome II\nShogun 2')
print('\nSelect Game:')
print('Options: 3k, britannia, attila, rome2, shogun2')

while True:
	game_selection = input('Selection: ').lower()
	if game_selection not in ('3k', 'britannia', 'attila', 'rome2', 'shogun2'):
		print('\nERROR: Invalid entry. Please input a valid entry')
		print('Valid entries: 3k, britannia, attila, rome2, shogun2')
	else:
		break

if game_selection == '3k':
	soupselect_unit_class = ('th[colspan="23"]')
	soupselect_unit_name = ('td[colspan="21"] a')
	soupselect_unit_attributes = ('thead th')
elif game_selection in ('britannia', 'attila', 'rome2', 'shogun2'):
	soupselect_unit_class = ('th[colspan="19"]')
	soupselect_unit_name = ('td[colspan="17"] a')
	soupselect_unit_attributes = ('thead th')


#------------------------------------------------------------------------------
#STEP 1: Find data source
#------------------------------------------------------------------------------

#Extract from URL directly
url = str(input('Target URL: '))
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

"""
#Find all files of specified type
#file_ext = str(input(
#	'\nSet file extension to search for (do not include dot): '))
file_ext = str('htm')
directory = os.getcwd()
files = glob.glob(directory + '/*' + file_ext)
files_list_length = listRange(1, files)

#Extract file names from full file address
files_name_only = [os.path.basename(files[0])]
for f in files_list_length:
	files_name_only.append(os.path.basename(files[f]))
	pass

#List out all data files found in folder
print('\n' + str(len(files)) + ' file(s) found: ')
files_list_length = listRange(0, files)
for names in files_list_length:
	printAsList(files_name_only, names)
"""

#------------------------------------------------------------------------------
#STEP 2: Extract data from source
#------------------------------------------------------------------------------

#Begin data extraction
#for x in files_list_length:
#	filename = files_name_only[x]

	#Read and parse file name
#	imported_file = open(filename, encoding="utf8")
#	content = imported_file.read()
#	soup = BeautifulSoup(content, 'html.parser')

#---------------------------------------------------------------------------
#STEP 2a: Search for Unit Class data
#---------------------------------------------------------------------------

#Search for the relevant data (Unit Class)
unit_class = soup.select(soupselect_unit_class)
#printSoupAsList('Unit Class(es)', unit_class)

#Convert unit class data into a list
#unit_class_list = []
#appendSoupValuesToList(unit_class_list, unit_class)
unit_class_list = [unit_class[x].text for x in range(len(unit_class))]


#Search for unit class amounts (number of entries per unit class)
unit_class_amount = soup.select('p.long_descr + ul li')
#printSoupAsList('Unit Class Amounts', unit_class_amount)

#Convert unit class amounts data into a list
#unit_class_amount_list = []
#appendSoupValuesToList(unit_class_amount_list, unit_class_amount)
unit_class_amount_list = [unit_class_amount[x].text for x in range(
	len(unit_class_amount))]

#Extract only the numbers and convert to integers 
chars_to_remove = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X',
'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
'(', ')']
removeCharactersFromString(unit_class_amount_list, chars_to_remove)
convertListValuesToInt(unit_class_amount_list)

#Modify any existing duplicates in unit class data list
duplicates = checkListForDuplicates(unit_class_list)
if duplicates == True:
	seen = []
	seen_dict = {}
	for z in range(len(unit_class_list)):
		#Add initial key to list and dict of seen (existing) items
		if z == 0:
			seen.append(unit_class_list[z])
			seen_dict[unit_class_list[z]] = seen.count(
				unit_class_list[z])

		#Add subsequent items to list and dict of seen items
		elif z < len(unit_class_list):
			if unit_class_list[z] in seen:
				#Check if key already exists in dictionary
				key_in_dict = checkForKey(
					seen_dict, unit_class_list[z])
				if key_in_dict == False:
					#First add the duplicate key + value to dict
					seen_dict[unit_class_list[z]] = (seen.count(
					unit_class_list[z])+1)						

					#Grab the index of the duplicate key
					dup_index = getIndexofDupKey(
						seen_dict, unit_class_list, z)

					#Grab the value of the key based on its index
					temp_dict = list(seen_dict)		

					#Add number to end of duplicate based on how many exist
					appendIncNumToStr(seen, unit_class_list, dup_index,
						seen_dict, temp_dict, z)
				else:
					#Update the duplicate key index
					seen_dict[unit_class_list[z]] += 1			

					#Grab the index of the duplicate key
					dup_index = getIndexofDupKey(
						seen_dict, unit_class_list, z)

					#Grab the value of the key based on its index
					temp_dict = list(seen_dict)		

					#Add number to end of duplicate based on how many exist
					appendIncNumToStr(seen, unit_class_list, dup_index,
						seen_dict, temp_dict, z)
			else:
				seen.append(unit_class_list[z])
		else:
			break
	unit_class_list = seen

#Pair up unit class names with corresponding number of entries per class
unit_class_dict = dict(zip(unit_class_list, unit_class_amount_list))


#---------------------------------------------------------------------------
#STEP 2b: Search for Unit Name data
#---------------------------------------------------------------------------

#[2]Search for the relevant data (Unit Names)
unit_name = soup.select(soupselect_unit_name)
#printSoupAsList('Unit Name(s)', unit_name)


#---------------------------------------------------------------------------
#STEP 2c: Search for Unit Attribute data
#---------------------------------------------------------------------------

#[3]Search for unit attributes
unit_attributes = soup.select(soupselect_unit_attributes)
#printSoupAsList('Unit Attribute(s)', unit_attributes)

#Convert unit atributes into a list
#unit_attributes_list = []
#appendSoupValuesToList(unit_attributes_list, unit_attributes)
unit_attributes_list = [unit_attributes[x].text for x in range(
	len(unit_attributes))]
unit_attributes_list.pop(0)

if game_selection == '3k':
	for item in range(len(unit_attributes_list)):
		#Grab first two letters and split based on reoccurence of those
		unit_attributes_list[item] = unit_attributes_list[item].strip()
		upper_two = (unit_attributes_list[item][:2]).upper()
		word_only = unit_attributes_list[item].split(upper_two)

		#Repeat the above but with the first two letters of second word
		second_word = unit_attributes_list[item].split(" ")	
		if len(second_word) > 1:
			upper_two = (second_word[1][:2]).upper()
		else:
			upper_two = (unit_attributes_list[item][:2]).upper()
		word_only = word_only[0].split(upper_two)

		#Save the extracted word by itself
		unit_attributes_list[item] = word_only[0]
else:
	pass

#---------------------------------------------------------------------------
#STEP 2d: Search for Unit Statistics data
#---------------------------------------------------------------------------

#[4]Search for unit statistics
unit_statistics1 = soup.select('tr[class=""] td')
unit_statistics2 = soup.select('tr[class="tr2"] td')

#Generate array #1 of indices used to pull unit statistics
total_length1 = len(unit_statistics1)
length_each_entry = int(len(unit_attributes) / len(unit_class))
number_of_entries1 = int(total_length1 / length_each_entry)
stat_arrays1 = []
generateArrayForUnitStats(
	length_each_entry, number_of_entries1, stat_arrays1)

#Generate array #2 of indices used to pull unit statistics
total_length2 = len(unit_statistics2)
length_each_entry = int(len(unit_attributes) / len(unit_class))
number_of_entries2 = int(total_length2 / length_each_entry)
stat_arrays2 = []
generateArrayForUnitStats(
	length_each_entry, number_of_entries2, stat_arrays2)

#Convert unit statistics into a list
unit_statistics_list1 = copy.deepcopy(stat_arrays1)
unitStatisticsToList(stat_arrays1, number_of_entries1, \
	unit_statistics_list1, unit_statistics1)
unit_statistics_list2 = copy.deepcopy(stat_arrays2)
unitStatisticsToList(stat_arrays2, number_of_entries2, \
	unit_statistics_list2, unit_statistics2)

#Add unit names to the corresponding statistics
for units in range(number_of_entries1):
	unit_statistics_list1[units].insert(
		0, unit_name[int(units*2)].text)
	if units < number_of_entries2:
		unit_statistics_list2[units].insert(
			0, unit_name[int((units*2)+1)].text)
	else:
		pass


#---------------------------------------------------------------------------
#STEP 3: Build arrays from extracted data
#---------------------------------------------------------------------------

#Build and combine data arrays
dataframe1 = pandas.DataFrame(
	unit_statistics_list1, columns=unit_attributes_list[
	:len(stat_arrays1[0])+1])
dataframe2 = pandas.DataFrame(
	unit_statistics_list2, columns=unit_attributes_list[
	:len(stat_arrays2[0])+1])
combined_dataframe = pandas.concat(
	[dataframe1, dataframe2]).sort_index(kind='merge')

#Set dataframe index column name
combined_dataframe = combined_dataframe.reset_index(drop=True)
index = combined_dataframe.index
index.name = "No."
combined_dataframe.index +=1

combined_dataframe['Unit_'] = combined_dataframe['Unit']

with pandas.option_context('display.max_rows', None):  
    print(combined_dataframe)

"""
#Print out tables divided by class
print('\nTable Output:')
row_start = combined_dataframe.index[0]
row_stop = getDictValue(unit_class_dict, 0)
for x in range(len(unit_class_list)):
	print(getDictKeyAndValue(unit_class_dict, x))
	print(combined_dataframe.loc[row_start:row_stop])
	row_start += getDictValue(unit_class_dict, x)
	if x+1 < len(unit_class_list):
		row_stop += getDictValue(unit_class_dict, x+1)
	else:
		break
"""


#---------------------------------------------------------------------------
#STEP 4: Write arrays to csv
#---------------------------------------------------------------------------

#Generate csv file and write data
out_ext = 'csv'
#output_file_name = files_name_only[x][:-len(file_ext)] + out_ext
output_file_name = str(soup.select('title')[0].text)
output_file_name = output_file_name[:20] + '.' + out_ext
row_start = combined_dataframe.index[0]
row_stop = getDictValue(unit_class_dict, 0)
initial_write = True
for x in range(len(unit_class_list)):
	if initial_write == True:
		with open(output_file_name, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([getDictKey(unit_class_dict, 0)])
		combined_dataframe.loc[row_start:row_stop].to_csv(
			output_file_name, mode='a')
		row_start += getDictValue(unit_class_dict, x)
		initial_write = False
		if x+1 < len(unit_class_list):
			row_stop += getDictValue(unit_class_dict, x+1)
		else:
			break
	elif initial_write == False:
		with open(output_file_name, 'a', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow("")
			writer.writerow([getDictKey(unit_class_dict, x)])		
		combined_dataframe.loc[row_start:row_stop].to_csv(
			output_file_name, mode='a')
		row_start += getDictValue(unit_class_dict, x)
		if x+1 < len(unit_class_list):
			row_stop += getDictValue(unit_class_dict, x+1)
		else:
			break


#---------------------------------------------------------------------------
#STEP 4-2: Write arrays to ods
#---------------------------------------------------------------------------
"""
#Generate ods file and write data
csv_input = pandas.read_csv('output.csv')
with pandas.ExcelWriter('output.ods', engine='odf') as writer:
	csv_input.to_excel(writer)
"""

print('SUCCESS: Data extracted and saved')
