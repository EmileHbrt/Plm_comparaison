# Plm_comparaison Dorian & Emile 

from optparse import OptionParser
#==================================================================================================================

def filtre_score(score_column, score_limit):
	list_idx_save=[]
	for idx in range(len(score_column)):
		if score_column[idx] >= score_limit:
			list_idx_save.append(idx)
	return list_idx_save

#==================================================================================================================

def main():
	usage = usage = "python Parser_tab.py -i <input_file> -o <output_file> -s <score_arg> \n"
	parser = OptionParser(usage)
	parser.add_option("-i", "--input_file", dest="input_file", help="path for the dataset")
	parser.add_option("-o", "--output_file", dest="output_file", help="path for the file parsed")
	parser.add_option("-s", "--score_arg", dest="score_arg", help="desired score limit")
	
	(options, args) = parser.parse_args()
	
	


#==================================================================================================================

if __name__ == "__main__":
	main()