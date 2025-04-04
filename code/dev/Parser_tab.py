# Plm_comparaison Dorian & Emile 

from optparse import OptionParser
import pandas as pd

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

def IsExist(col_list : list):
	"""
	returns true if all elements of col_list are contained in the existing column list 

	args :
	"col_list" : list of names to checked 
	"""

	list_existing = ['SeqCluster','ClusterNumber','Prot_AC','score', 'RecName', 'InterPro_id', 'InterPro_describe', 'SFLD_id', 'SFLD_describe',
               'PRINTS_id', 'PRINTS_describe', 'Pfam_id', 'Pfam_describe', 'CDD_id', 'CDD_describe',
               'PROFILE_id', 'PROFILE_describe', 'NCBIFAM_id', 'NCBIFAM_describe', 'PROSITE_id', 
               'PROSITE_describe', 'HAMAP_id', 'HAMAP_describe', 'SMART_id', 'SMART_describe',
               'PIRSF_id', 'PIRSF_describe', 'PANTHER_id', 'PANTHER_describe', 'CATHGENE3D_id',
               'CATHGENE3D_describe', 'SSF_id', 'SSF_describe', 'GO_C', 'GO_F', 'GO_P']
	
	for elm in col_list:
		if elm not in list_existing:
			return False
		
	return True

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
	
	try:
		df = pd.read_csv(input_file,low_memory=False)
	except:
		print(' error with -i : correspond to the path of the dataset ')

	if options.score_arg is not None :
		score_arg = options.score_arg
		df = df.loc[df['score']>= float(score_arg) ,:]
	
	if options.col_choose is not None :
		list_brute = options.col_choose
		col_list = list_creater(list_brute)
		
		if not IsExist(col_list):
			print('error in colums names')
			
		else:
			print(col_list)
			df = df.loc[:,col_list]

	try :
		writer_tab(df, output_file)
	except:
		print(' error with -o : correspond to the parsed dataset path ')

#==================================================================================================================

if __name__ == "__main__":
	main()