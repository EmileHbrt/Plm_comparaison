# Analyse_Plot.py Dorian et Emile
from optparse import OptionParser
import pandas as pd
import os 
import numpy as np
import matplotlib.pyplot as plt

#==================================================================================================================

def bar_plot_graph(df, output_dir : str, cond :str , cas : str ,col_score_name :str):
    """
    
    """

    min_score = min(df[col_score_name])
    df_clean = df.dropna(subset=[col_score_name, cond])

    min_score = min(df_clean[col_score_name])
    thresholds = np.arange(0.5, 1.0, 0.05) 




    cumulative_counts = [(df_clean[col_score_name] >= thr).sum() for thr in thresholds]
    nb_seq = cumulative_counts[0]

    plt.figure(figsize=(10, 6))

    plt.bar(thresholds, cumulative_counts, width=0.03, align='center', color='skyblue')
    plt.xlabel("Seuil de score")
    plt.ylabel("Nombre de séquences annotées (score ≥ seuil)")
    plt.title(f"Distribution des scores obtenus par PlmSearch, aspect : {cas} , cas : {cond}")
    plt.annotate(f"Score minimal : {min_score:.2f}",
                xy=(0.75, 0.85), xycoords='axes fraction',
                fontsize=12, color='red',
                horizontalalignment='left', verticalalignment='top')
    plt.annotate(f"nombre total de séquence : {nb_seq}",
                xy=(0.62, 0.95), xycoords='axes fraction',
                fontsize=12, color='red',
                horizontalalignment='left', verticalalignment='top')
    plt.xticks(thresholds, [f"{thr:.2f}" for thr in thresholds])
    output_name = output_dir + f"\\barplot_{cas}_{cond}.jpeg"
    plt.savefig(os.path.abspath(output_name), format="jpeg")
    plt.close()

#==================================================================================================================

def tab_filter( tab , col_score_name : str ):
    """
    Return a panda table with only sequences with result from ref and test method. 
    args:
    - tab : a csv table 
    - col_score_name : name of the score column in str
    """
    df = pd.DataFrame(tab)
    df[col_score_name] = df[col_score_name].replace('', np.nan)
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df = df.dropna(subset=['score'])
    return df

#==================================================================================================================

def error_plot_graph(df , output_dir : str, mod : str,col_score_name : str):
    """
    
    """

    df_clean = df.dropna(subset=[col_score_name, 'relation','Grand_cas','enrichissement'])


    df_grouped = df_clean.groupby(mod)[col_score_name].agg(["mean", "std"]).reset_index()

    df_grouped["std_truncated"] = np.clip(df_grouped["std"], 0, 1 - df_grouped["mean"])


    plt.figure(figsize=(6, 5))
    plt.errorbar(df_grouped[mod], df_grouped["mean"], yerr=df_grouped["std_truncated"], fmt='.', capsize=15,capthick = 100,ms =20,mew= 5,elinewidth = 3,color = 'black')

    plt.xlabel(mod)
    plt.ylabel("Score")
    plt.title(f"Score moyen et écart-type suivant {mod}")

    plt.grid(True)
    plt.style.use('default')
    plt.xticks(df_grouped[mod], df_grouped[mod], ha='center') 
    plt.margins(x=0.2)  

    ax = plt.gca()  
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False)  
    ax.spines['left'].set_visible(True)  
    ax.spines['bottom'].set_visible(True) 
    ax.spines['left'].set_linewidth(2) 
    ax.spines['bottom'].set_linewidth(2) 
    output_name = output_dir + f"\\errorplot_{mod}.jpeg"
    plt.savefig(os.path.abspath(output_name), format="jpeg")

    plt.close()

#==================================================================================================================

def list_creator_cell(cell : str):
    """
    Return a python list from a str list separeted with "," or "|" .

    args:
    - cell : a str corresponding to a cell from the table
    """
    cell = cell.strip()  
    if '|' in cell:
        return cell.split('|')
    else:
        return cell.split()

#==================================================================================================================

def classify_relation(row):
    """
    Return the relation between the two result cell.

    args:
    - row : a row of the dataframe
    """
    set_test = set(row['test_list'])
    set_ref  = set(row['ref_list'])
    
    if not set_test and not set_ref:
        return None
    if set_test == set_ref:
        return "identique"
    if set_test.issubset(set_ref):
        return "sous-ensemble-test"
    if set_ref.issubset(set_test):
        return "sous-ensemble-ref"
    if set_test.intersection(set_ref):
        return "différent-intersection"
    return "différents-sans-intersection"

#==================================================================================================================

def get_categories(name):
    """
    Return the realtion categories.

    args:
    - name : the relation name
    """
    if name == "identique" :
        return "identique"
    elif (name == "sous-ensemble-test") or (name == "sous-ensemble-ref") :
        return "sous-ensemble"
    elif (name == "différent-intersection") or (name == "différents-sans-intersection"):
        return "différent"

#==================================================================================================================

def get_enrichissement(name):
    """
    Return the enrichment status.

    args:
    - name : the relation name
    """
    if (name == "sous-ensemble-ref") or (name == "différents-sans-intersection"):
        return "enrichi"
    else :
        return "non-enrichi"

#==================================================================================================================

def classify(df):
    """
    Return the data frame with 3 more columns, one for relations , one for categories and a last one for enrichement status

    args:
    - df : a pandas dataframe
    """
    df['relation'] = df.apply(classify_relation, axis=1)
    df = df[df['relation'].notnull()]
    df["Grand_cas"] = df['relation'].apply(get_categories)
    df["enrichissement"] = df['relation'].apply(get_enrichissement)
    return df

#==================================================================================================================

def create_all_graph(df,output_dir,col_score_name) :
    """
    """
    relation_list = ["identique","sous-ensemble-test","sous-ensemble-ref","différent-intersection","différents-sans-intersection"]
    categories_list = ["identique","sous-ensemble","différent"]
    enrichi_list = ["enrichi","non-enrichi"]
    graph_dict = {'relation' : relation_list , 'Grand_cas' : categories_list , 'enrichissement' : enrichi_list}
    
    for type,name_list in graph_dict.items():
        for elm in name_list :
            bar_plot_graph(df , output_dir = output_dir ,cond = type ,cas=elm , col_score_name= col_score_name)
        error_plot_graph(df , output_dir,type,col_score_name)



#==================================================================================================================
# 											main
#==================================================================================================================
def main():
    usage = "python Analyse_plot.py -i <input_file> -o <output_dir> -t <test_col_name> -r <ref_col_name> -s <score_col_name> \n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="path for the folder where the PlmSearch result is")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="path for the folder where all the plots will be saved")
    parser.add_option("-t", "--test_col_name", dest="test_col_name", help="the name of the colum of the test method result")
    parser.add_option("-r", "--ref_col_name", dest="ref_col_name", help="the name of the colum of the reference method result")
    parser.add_option("-s", "--score_col_name", dest="score_col_name", help="the name of the colum of the reference method result")


    (options, args) = parser.parse_args()
    input_file = options.input_file
    output_dir = options.output_dir
    test_col_name  = options.test_col_name
    ref_col_name  = options.ref_col_name
    
    if options.score_col_name is not None:
        score_col_name  = options.score_col_name
    else : 
        score_col_name = 'score'

    try :
        data = pd.read_csv(os.path.abspath(input_file))
    except:
        print('error : input file not found')

    df = tab_filter(data,score_col_name) 
    df['test_list'] = df[test_col_name].apply(list_creator_cell)
    df['ref_list']  = df[ref_col_name].apply(list_creator_cell)
    df = df[df['ref_list'].apply(lambda x: len(x) > 0)]
    df = df[df['test_list'].apply(lambda x: len(x) > 0)]

    df = classify(df)
    create_all_graph(df, output_dir,score_col_name)

#==================================================================================================================
if __name__ == "__main__":
	main()