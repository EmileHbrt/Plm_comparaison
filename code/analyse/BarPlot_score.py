# BarPlot_score Dorian & Emile

import os
import pandas as pd
import matplotlib.pyplot as plt
from optparse import OptionParser

#==================================================================================================================
def counting_method_None(tab,col_score_name,min_score):
    """
      Retrun a list of with 1 element for each score interval (of 0.1) which correspond to the number of CK annoted for at least this score interval  
      
    args :
    "tab" : a panda dataset with at least one score column and in which each row correspond to a CK
    "col_score_name" : the name of the score columm in str
    "min_score" : the minimal score to be entered in the plot (a multiple a 0.1)
    """

    y_abs = [0 for i in range(int((1 - float(min_score))*10)+1)]
    list_score = tab[col_score_name]

    for i in range(len(list_score)):
        score = list_score[i]
        if (score != ' ') and (score != '') :
            idx = int( ( float(score) - float(min_score) )* 10 +1 ) 
            for add in range(idx):
                y_abs[add] += 1
    return y_abs

#==================================================================================================================

def counting_method_Arg(tab,col_score_name,min_score,annotation_col):
    """
      Retrun a list of with 1 element for each score interval (of 0.1) which correspond to the number of CK annoted for at least this score interval  
      
    args :
    "tab" : a panda dataset with at least one score column and in which each row correspond to a CK
    "col_score_name" : the name of the score columm in str
    "min_score" : the minimal score to be entered in the plot (a multiple a 0.1)
    "annotation_col" : the name of the column containig the annotation
    """

    y_abs = [0 for i in range(int((1 - float(min_score))*10)+1)]
    list_score = tab[col_score_name]
    list_anno = tab[annotation_col]

    for i in range(len(list_score)):
        score = list_score[i]
        annot = list_anno[i]
        if (score != ' ') and (score != '') and (annot != '') and (annot != ' '):
            idx = int( ( float(score) - float(min_score) )* 10 +1 ) 
            for add in range(idx):
                y_abs[add] += 1
    return y_abs

#==================================================================================================================

def compter_barplot(chemin):
    fichiers = os.listdir(chemin)
    compteur = sum(1 for fichier in fichiers if "Barplot" in fichier) 
    return compteur

#==================================================================================================================

def plot_save(output,y_abs):
    """
    Create and save the plot in jpeg format to the output file

    args : 
    "output" : Path for the bar plot in jpeg format
    "y_abs" : a list of number of annotation by score
    """
    
    x_abs = [str(1 - (i*0.1)) for i in range(len(y_abs))]
    x_abs = x_abs[::-1]

    plt.bar(x_abs,y_abs)
    plt.ylabel('Number of annotated CK')
    plt.xlabel('Score')
    plt.title('Bar plot of the number of annotated CK as a function of score ')
    plt.savefig(output,format = "jpeg")

#==================================================================================================================

def main():
    usage = usage = "python BarPlot_score.py -i <input_file> -o <output_file>  -c <score_column> -m <minimal_score> -a <annotation_col> \n" 
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="The path to the results table of a method in csv format, with at least a score column and a row for each CK ")
    parser.add_option("-o", "--output_file", dest="output_file", help="Path for the bar plot in jpeg format")
    parser.add_option("-c", "--score_column", dest="score_column", help="Name of the score column")
    parser.add_option("-m", "--minimal_score", dest="minimal_score", help="The minimum score to be entered in the plot (a multiple a 0.1) ")
    parser.add_option("-a", "--annotation_col", dest="annotation_col", help="The name of the column containing the annotations, if the argument is not given, all rows will be considered as annotated")

    (options, args) = parser.parse_args()
    input_list = options.input_file
    output_file = options.output_file 
    col_score_name = options.score_column
    min_score = options.minimal_score
    annotation_col = options.annotation_col

    nb_barplot = compter_barplot(output_file)
    if nb_barplot == 0 :
        output_file +=  "\Barplot.jpeg"
    else :
        output_file += f"\Barplot_{ nb_barplot + 1 }.jpeg"

    df = pd.read_csv(input_list,low_memory=False)
    if annotation_col is None:
        y_abs = counting_method_None(df,col_score_name,min_score)
    else :
        y_abs = counting_method_Arg(df,col_score_name,min_score,annotation_col)
    plot_save(output_file,y_abs)

#==================================================================================================================
if __name__ == "__main__":
	main()
     