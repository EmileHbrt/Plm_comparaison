# Plm_comparaison Dorian & Emile 

from optparse import OptionParser

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
	score_arg = options.score_arg
	print('input :' , input_file)
	print('output :' , output_file)
	print('score :' , score_arg)
	
#==================================================================================================================

if __name__ == "__main__":
	main()