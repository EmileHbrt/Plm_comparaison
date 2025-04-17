# Comp_missing.py Dorian & Emile

from optparse import OptionParser
import pandas as pd
import os
import matplotlib.pyplot as plt

#==================================================================================================================

def list_creator(str_arg: str):
    """
    Converts a string into a list of substrings, handling spaces and the character 'I'.

    Args:
    str_arg: The input string.

    Returns:
    A list of substrings.
    """
    col_list = [] 
    name = ''

    for elm in str_arg:
        if elm == ' ':
            continue
        if elm == "I":
            col_list.append(name)
            name = 'I'
        else:
            name += elm
    col_list.append(name)

    return col_list

#==================================================================================================================

import matplotlib.pyplot as plt

def plot_creator(dict_id, output):
    """

    Args:
        dict_id (dict): 
        output (str): 
    """
    plt.figure(figsize=(15, 8))
    keys = list(dict_id.keys())
    values = list(dict_id.values())
    plt.bar(keys, values, color='skyblue')
    plt.xlabel('Identifiants')
    plt.ylabel('Nombre')
    plt.title("Diagramme en barres des identifiants")
    
    plt.savefig(output, format="jpeg")

    plt.close()



#==================================================================================================================

def id_score_finder(df, min_score, test_col_name, ref_col_name, col_score_name):
    """

    Args:
        df: 
        min_score: 
        test_col_name: 
        ref_col_name: 
        col_score_name: 
    """
    dict_id = {}
    list_score = []
    
    for idx, row in df.iterrows():
        ref_value = row[ref_col_name]
        test_value = row[test_col_name]
        score_value = row[col_score_name]
        print(f"ref_value :{ref_value},test_value : {test_value}, score_value : {score_value}")
        
        if ref_value in [' ', ''] and test_value not in [' ', '']:
            if float(score_value) >= float(min_score):
                id_temp_list = list_creator(test_value)
                for id_item in id_temp_list:
                    if id_item not in dict_id:
                        dict_id[id_item] = 1
                        list_score.append(score_value)
                    else:
                        dict_id[id_item] += 1
                        
    return dict_id, list_score

                 
#==================================================================================================================

def compter_comp_plot(chemin):
    fichiers = os.listdir(chemin)
    compteur = sum(1 for fichier in fichiers if "Comp_plot" in fichier) 
    return compteur

#==================================================================================================================
def main():
    usage = usage = "python Comp_only_1_method_result.py -i <input_file> -o <output_dir>  -c <score_column> -m <minimal_score> -t <test_col_name> -r <ref_col_name> \n" 
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
    dict_id,list_score = id_score_finder(df,min_score,test_col_name,ref_col_name,col_score_name)

    nb_barplot = compter_comp_plot(output_dir)
    if nb_barplot == 0 :
        output_dir +=  "\Comp_plot.jpeg"
    else :
        output_dir += f"\Comp_plot_{ nb_barplot + 1 }.jpeg"
    
    plot_creator(dict_id,output_dir)
    print(list_score)
    

#==================================================================================================================
if __name__ == "__main__":
	main()
