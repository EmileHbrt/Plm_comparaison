from optparse import OptionParser
import matplotlib.pyplot as plt
from filtered_size import filtre_size, join_col
from collections import Counter
import pandas as pd
import requests

#==================================================================================================================

def fetch_go_term_details(go_term):
    """
    Fetch details for a given GO term from the QuickGO API.

    Args:
        go_term (str): The GO term to fetch details for (e.g., 'GO:0016020').

    Returns:
        tuple: A tuple containing the name and aspect of the GO term, or (None, None) if not found.
    """
    url = f'https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{go_term}/complete'
    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        if 'results' in response_json and len(response_json['results']) > 0:
            name = response_json['results'][0].get('name', None)
            aspect = response_json['results'][0].get('aspect', None)
            return name, aspect
    return None, None

#==================================================================================================================


def plot_top_go_terms(tab, column_name, a, top_n, GO):
    """
    Extract values from the specified column, count occurrences, and plot the top N most frequent terms.
    
    Args:
        tab (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to extract values from.
        top_n (int): The number of most common terms to plot (default is 10).
    """

    go_joined_list = '|'.join([val for val in tab[column_name].tolist() if val.strip() != ""])
    go_joined_list = go_joined_list.replace('|', ',').split(',')

    go_counts = Counter(go_joined_list)
    
    most_common_go = go_counts.most_common(100)
    go_terms, counts = zip(*most_common_go)

    go_details = {go_term: [fetch_go_term_details(go_term), counts[go_terms.index(go_term)]] for go_term in go_terms}
    #print(go_details)
    go_detail = {}

    i = top_n
    for k, v in go_details.items():
        
        if v[0][1]== GO:
            go_detail[k] = [v[0][0], v[1]]
            i -= 1
        if i == 0:
            break

    print(go_detail, len(go_detail))

    labels = [k for k in go_detail.keys()]
    counts = [v[1] for v in go_detail.values()]


    bars = plt.barh(labels, counts, color='lightblue', edgecolor='black')
    
    top_3_counts = sorted(counts, reverse=True)[:a]

    for bar, go_term in zip(bars, go_detail.keys()):
        detail = go_detail[go_term][0] if go_detail[go_term][0] else "N/A"
        if bar.get_width() in top_3_counts:
            plt.text(bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, detail,
                     ha='center', va='center', fontsize=7, color='black')
        else:
            plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, detail,
                     ha='left', va='center', fontsize=7, color='black')

    plt.xlabel("Occurences")
    plt.ylabel("GO Terms")
    plt.title(f"Les 10 {column_name} les plus prédits") 

#==================================================================================================================
# 											main
#==================================================================================================================

def main():
    usage = "python Most_common_plot.py -i <input_file> -f <fasta>"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="input the parsed_tab.csv path")
    parser.add_option("-f", "--fasta", dest="fasta", help="input your fasta file path")

    (options, args) = parser.parse_args()

    input_file = options.input_file if options.input_file is not None else print("error with -i : please provide a parsed_tab.csv")
    fasta = options.fasta if options.fasta is not None else print("error with -f : please provide a fasta file")

    tab = pd.read_csv(input_file)

    seq_dict = filtre_size(fasta, 250)

    tab = join_col(input_file, ['GO_C', 'GO_F', 'GO_P'])
    tab = tab[tab['ClusterNumber'].isin(seq_dict.keys())]
        
    plt.figure(figsize=(18, 6))

    # Subplot for molecular_function (GO_joined)
    plt.subplot(2, 3, 1)
    plot_top_go_terms(tab, 'GO_joined', 5, 5, 'molecular_function')
    plt.title("Top 5 PLM - Molecular Function GO_terms")

    # Subplot for cellular_component (GO_joined)
    plt.subplot(2, 3, 2)
    plot_top_go_terms(tab, 'GO_joined', 5, 5, 'cellular_component')
    plt.title("Top 5 PLM - Cellular Component GO_terms")

    # Subplot for biological_process (GO_joined)
    plt.subplot(2, 3, 3)
    plot_top_go_terms(tab, 'GO_joined', 3, 5, 'biological_process')
    plt.title("Top 5 PLM - Biological Process GO_terms")

    # Subplot for molecular_function (G_result)
    plt.subplot(2, 3, 4)
    plot_top_go_terms(tab, 'GO_result', 2, 5, 'molecular_function')
    plt.title("Top 5 InterProScan - Molecular Function GO_terms")

    # Subplot for cellular_component (G_result)
    plt.subplot(2, 3, 5)
    plot_top_go_terms(tab, 'GO_result', 1, 5, 'cellular_component')
    plt.title("Top 5 InterProScan - Cellular Component GO_terms")

    # Subplot for biological_process (G_result)
    plt.subplot(2, 3, 6)
    plot_top_go_terms(tab, 'GO_result', 1, 5, 'biological_process')
    plt.title("Top 5 InterProScan - Biological Process GO_terms")

    plt.tight_layout()
    plt.show()


#==================================================================================================================
if __name__ == "__main__":
	main()



