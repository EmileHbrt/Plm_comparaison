# Plm_comparaison Dorian & Emile 

from optparse import OptionParser
import pandas as pd

#==================================================================================================================

def writer_tab(df, output):
	df.to_csv(output,index=False)	 

#==================================================================================================================
# 											main
#==================================================================================================================
def main():
	usage = usage = "python Parser_tab.py -i <input_file> -o <output_file> -s <score_arg> \n"
	parser = OptionParser(usage)
	parser.add_option("-i", "--input_file", dest="input_file", help="path for the dataset")
	parser.add_option("-o", "--output_file", dest="output_file", help="path for the file parsed")
	parser.add_option("-s", "--score_arg", dest="score_arg", help="desired score limit")
	
	(options, args) = parser.parse_args()
	input_file = options.input_file
	output_file = options.output_file
	
	
	df = pd.read_csv(input_file,low_memory=False)

	if options.score_arg is not None :
		score_arg = options.score_arg
		df = df.loc[df['score']>=score_arg,:]
	
	writer_tab(df)

#==================================================================================================================

if __name__ == "__main__":
	main()