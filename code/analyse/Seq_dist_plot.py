from optparse import OptionParser
import matplotlib.pyplot as plt
from filtered_size import filtre_size
from collections import Counter

#==================================================================================================================

def sequence_distribution(filtered_sequences, min_bin, max_bin):
    """
    Plot a barplot focusing on the shortest sequences grouped by bins of 50.
    """
    bins = [length // 50 * 50 for length in filtered_sequences.values()]
    bin_counts = Counter(bins)

    sorted_bins = sorted(bin_counts.keys())
    counts = [bin_counts[b] for b in sorted_bins]

    filtered_bins = [b for b in sorted_bins if min_bin <= b <= max_bin]
    filtered_counts = [bin_counts[b] for b in filtered_bins]
    filtered_bins.append(max_bin)
    filtered_counts.append(sum(bin_counts[b] for b in sorted_bins if b > max_bin))

    return filtered_bins, filtered_counts

#==================================================================================================================

def plot_bar(filtered_bins, filtered_counts, min_bin, max_bin):
    plt.bar(filtered_bins, filtered_counts, width=40, align='center',color = "black" ,edgecolor='white')
    plt.ylabel("Nombre de séquences")
    plt.xticks(
        filtered_bins, 
        labels=[
            f"{b}" if (b % 250 == 0 and b <= max_bin) else (r"$\geq$" + str(b) if b == max_bin else "") 
            for b in filtered_bins
        ]
    )
    
    plt.text(max(filtered_bins) / 2, -max(filtered_counts) * 0.1, "Taille de la séquence en acides aminés", 
             ha='center', va='center', fontsize=plt.gca().yaxis.label.get_size(), color='black')

    plt.title("Répartition des séquences selon leur nombre d'acides aminés")
    plt.show()


#==================================================================================================================
# 											main
#==================================================================================================================


def main():
    usage = "python Seq_dist_plot.py -i <input_file> -l <seq_length>"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="input the fasta sequences file")
    parser.add_option("-l", "--seq_length", dest="seq_length", help="specify the sequence length threshold")
    parser.add_option("-s","--small", dest="small", help="focus on small sequences")
    parser.add_option("-t", dest="threshold", help="focus on great sequences")

    (options, args) = parser.parse_args()
    fasta = options.input_file
    threshold = options.seq_length

    if fasta is None:
        print(' error with -i : please provide a fasta file')
    if threshold is None: 
        print('error with -l : please provide a length threshold')
        
    min = int(options.small) if options.small else 0
    max = int(options.threshold) if options.threshold else 2200
        
    
    filtered_sequences = filtre_size(fasta, int(threshold))    
    filtered_bins, filtered_sequences = sequence_distribution(filtered_sequences, min, max)

    plot_bar(filtered_bins, filtered_sequences, min, max)
  

#==================================================================================================================
if __name__ == "__main__":
	main()