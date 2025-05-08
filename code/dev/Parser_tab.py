# Plm_comparaison Dorian & Emile 

from optparse import OptionParser
import pandas as pd
import os

#==================================================================================================================

def writer_tab(df, output : str ):
	"""
	writes the panda table as a csv in the output file

	args:
	"df" : the panda table that you need to write
	"output" : path for the outuput 
	"""
	df.to_csv(output,index=False)	 

#==================================================================================================================

def list_creater(str_arg : str):
	"""
	returns from a comma-separated str list, a python list of str 

	args:
	"str_arg" : the comma-separated str list
	"""
	col_list = [] 
	name = ''

	for elm in str_arg:
		if elm == "," :
			col_list.append(name)
			name = ''
		else :
			name += elm
	col_list.append(name)

	return col_list

#==================================================================================================================
# 											main
#==================================================================================================================
def main():

	usage = usage = "python Parser_tab.py -i <input_file> -o <output_file> -s <score_arg> -c <col_list> -t <len_arg> \n" 
	parser = OptionParser(usage)
	parser.add_option("-i", "--input_file", dest="input_file", help="path for the dataset")
	parser.add_option("-o", "--output_file", dest="output_file", help="path for the file parsed")
	parser.add_option("-s", "--score_arg", dest="score_arg", help="desired score limit")
	parser.add_option("-c", "--col_choose", dest="col_choose", help="list of colone for the output")
	parser.add_option("-t", "--len_arg", dest="len_arg", help="desired sequence lenght limit")

	(options, args) = parser.parse_args()
	input_file = options.input_file
	output_file = options.output_file
	
	try:
		df = pd.read_csv(os.path.abspath(input_file),low_memory=False)
	except:
		print(' error with -i : correspond to the path of the dataset ')

	if options.score_arg is not None :
		score_arg = options.score_arg
		df['score'] = pd.to_numeric(df['score'].str.strip(), errors='coerce')
		df = df.loc[df['score'].astype(float) >= float(score_arg) ,:]

	if options.len_arg is not None :
		len_arg = options.len_arg
		df['taille'] = pd.to_numeric(df['taille'].str.strip(), errors='coerce')
		df = df.loc[df['taille'].astype(float) >= float(len_arg) ,:]

	if options.col_choose is not None :
		list_brute = options.col_choose
		col_list = list_creater(list_brute)
			
		print(col_list)
		df = df.loc[:,col_list]

	try :
		writer_tab(df, output_file)
	except:
		print(' error with -o : correspond to the parsed dataset path ')

#==================================================================================================================

if __name__ == "__main__":
	main()