# Comp_missing.py Dorian & Emile

from optparse import OptionParser
import pandas as pd
import os
#==================================================================================================================
def list_creator(df, min_score, test_col_name, ref_col_name, col_score_name):
    """
    """
    list_id = []
    list_score =[]

    for i in range(len(df)):
        
         


#==================================================================================================================

def main():
    usage = usage = "python Comp_only_1_method_result.py -i <input_file> -o <output_dir>  -c <score_column> -m <minimal_score> -t <test_col_name> -r <ref_col_name>\n" 
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="The path to the results table of a method in csv format, with at least a score column and a row for each CK ")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="Path for the bar plot in jpeg format")
    parser.add_option("-c", "--score_column", dest="score_column", help="Name of the score column")
    parser.add_option("-m", "--minimal_score", dest="minimal_score", help="The minimum score to be entered in the plot (a multiple a 0.1) ")
    parser.add_option("-r","--ref_col_name",dest="ref_col_name",help="")
    parser.add_option("-t", "--test_col_namel", dest="test_col_name", help="The name of the column containing the annotations, if the argument is not given, all rows will be considered as annotated")

    (options, args) = parser.parse_args()
    input_file = options.input_file
    output_dir = options.output_dir 
    col_score_name = options.score_column
    min_score = options.minimal_score
    test_col_name = options.test_col_name
    ref_col_name = options.ref_col_name

    if col_score_name is None :
        col_score_name = 'score'
    if min_score is None :
        min_score = 0.5

    df = pd.read_csv(input_file,low_memory=False)


#==================================================================================================================
if __name__ == "__main__":
	main()
