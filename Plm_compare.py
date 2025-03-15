# Plm_comparaison Dorian & Emile 

from optparse import OptionParser
import pandas as pd

#==================================================================================================================

def writer_tab(df, output):
	df.to_csv(output,index=False)	 

#==================================================================================================================

def list_creater(str_arg):
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
	usage = usage = "python Parser_tab.py -i <input_file> -o <output_file> -s <score_arg> -c <col_list> \n"
	parser = OptionParser(usage)
	parser.add_option("-i", "--input_file", dest="input_file", help="path for the dataset")
	parser.add_option("-o", "--output_file", dest="output_file", help="path for the file parsed")
	parser.add_option("-s", "--score_arg", dest="score_arg", help="desired score limit")
	parser.add_option("-c", "--col_choose", dest="col_choose", help="list of colone for the output")

	(options, args) = parser.parse_args()
	input_file = options.input_file
	output_file = options.output_file
	
	
	df = pd.read_csv(input_file,low_memory=False)

	if options.score_arg is not None :
		score_arg = options.score_arg
		df = df.loc[df['score']>= float(score_arg) ,:]
	
	if options.col_choose is not None :
		list_brute = options.col_choose
		col_list = list_creater(list_brute)
		
		# mettre le is_existing() ~~ try/ expect 

		print(col_list)
		df = df.loc[:,col_list]

	writer_tab(df, output_file)

#==================================================================================================================

if __name__ == "__main__":
	main()