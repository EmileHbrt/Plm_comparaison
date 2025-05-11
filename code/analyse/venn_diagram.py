import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import pandas as pd
import xlsxwriter
from optparse import OptionParser
from filtered_size import filtre_size, join_col

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
               'CATHGENE3D_describe', 'SSF_id', 'SSF_describe', 'GO_C', 'GO_F', 'GO_P','Interpro_result','Pfam_result', 'GO_result']
	
	for elm in col_list:
		if elm not in list_existing:
			return False
		
	return True

#==================================================================================================================
# 											main
#==================================================================================================================

def main():
    usage = "python venn_diagram.py -i <input_file> -o <output_dir> -c <col_list> -n <cluster_number> -s <size_sequence>\n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="path for the Interpro dataset")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="path for the folder where the csv will be saved")
    parser.add_option("-c", "--col_list", dest="col_list", help="list of columns selected to be used")
    parser.add_option("-n", "--cluster_number", dest="cluster_number", help="create a venn diagram with this SeqCluster")
    parser.add_option("-s", "--size_sequence", dest="size_sequence", help="size minimal of sequences to be analyzed")

    (options, args) = parser.parse_args()
    input_file = options.input_file
    output_dir  = options.output_dir
    col_list = options.col_list
    cluster_number = options.cluster_number
    size_seq = options.size_sequence

    try:
        tab = pd.read_csv(input_file)
    except:
        print(' error with -i : correspond to the path of the dataset ')
    
    if size_seq is not None: 
        fasta = input("Copier le chemin de votre fichier fasta :")
        seq_dict = filtre_size(fasta, int(size_seq))
        tab = tab[tab['ClusterNumber'].isin(seq_dict.keys())]

        if output_dir is not None:
            tab.to_csv(output_dir + f"/{'250AA.csv'}")
            print(f"Filtered data saved to filtered_tab_by_250AA.csv")
        else:
            print("Output directory not provided. Skipping save operation.")
    
    col_list = list_creater(col_list)

    if not IsExist(col_list):
        print('error in colums names')
        print(tab.columns)
        print(col_list)
    else:
        print(col_list)


        if col_list[-1] == 'GO_result':
            tab = join_col(input_file, ['GO_C', 'GO_F', 'GO_P'])
            col_list[-2] = 'GO_joined'
        
    
        filtered_tab = tab.loc[:, col_list]
        filtered_tab = filtered_tab[filtered_tab['ClusterNumber'].str.startswith('CK')]

        print(filtered_tab.head())

        count_plmIsSubset = 0
        count_otherIsSubset = 0
        count_plm_empty = 0
        count_other_empty = 0
        count_nothing = 0
        count_plm_completed_by_other= 0
        count_other_completed_by_plm = 0
        count_noIntersection = 0
        count_same = 0

        for index, row in filtered_tab.iterrows():  

            plm = row[col_list[-2]]
            other = row[col_list[-1]]

            other = other.replace('|', '  ')

            other_set = set(other.split())
            plm_set = set(plm.split())

            # Create a Venn diagram
            if cluster_number is not None:
                if row['ClusterNumber'] == str(cluster_number):
                    plt.figure(figsize=(8, 8))
                    venn2([plm_set, other_set], ('PLM', str(col_list[-1])))
                    plt.title(f"Venn Diagram for {row['ClusterNumber']}")
                    plt.savefig(output_dir + f"/venn_diagram_{row['ClusterNumber']}.png")
                    plt.close()

            if output_dir is None:
                print("Please provide a valid output directory.")

            # Create a new Excel file with multiple sheets (only once, outside the loop)
            elif 'workbook' not in locals():
                workbook = xlsxwriter.Workbook(output_dir + "/" +  str(col_list[-2]) + "_venn_analysis.xlsx")

                worksheet1 = workbook.add_worksheet("PLM_Subset")
                worksheet2 = workbook.add_worksheet(str(col_list[-1])+"_Subset")
                worksheet3 = workbook.add_worksheet("PLM_Empty")
                worksheet4 = workbook.add_worksheet(str(col_list[-1])+"_Empty")
                worksheet5 = workbook.add_worksheet("Nothing")
                worksheet6 = workbook.add_worksheet("Plm_completed_by")
                worksheet7 = workbook.add_worksheet("completed_by_PLM")
                worksheet8 = workbook.add_worksheet("NoIntersection")
                worksheet9 = workbook.add_worksheet("Same")

                # Write the column headers to each worksheet
                headers = filtered_tab.columns.tolist()

                for i in range(1, 10):
                    locals()[f'worksheet{i}'].write_row(0, 0, headers)
                    

            if len(plm_set) == 0 and len(other_set) == 0:
                count_nothing += 1
                worksheet5.write_row(count_nothing, 0, row.values.tolist())

            elif len(plm_set) == 0:
                count_plm_empty += 1
                worksheet3.write_row(count_plm_empty, 0, row.values.tolist())

            elif len(other_set) == 0:
                count_other_empty += 1
                worksheet4.write_row(count_other_empty, 0, row.values.tolist())
            
            elif plm_set == other_set:
                count_same += 1
                worksheet9.write_row(count_same, 0, row.values.tolist())
            
            else:
                 
                if plm_set.issubset(other_set):
                    count_plmIsSubset += 1
                    worksheet1.write_row(count_plmIsSubset, 0, row.values.tolist())

                elif other_set.issubset(plm_set):
                    count_otherIsSubset += 1
                    worksheet2.write_row(count_otherIsSubset, 0, row.values.tolist())

                else:

                    if len(plm_set.intersection(other_set)) != 0:

                        if len(plm_set) >= len(other_set):
                            count_other_completed_by_plm += 1  
                            row_with_jaccard = row.values.tolist()
                            worksheet7.write_row(count_other_completed_by_plm, 0, row_with_jaccard)

                        elif len(other_set) > len(plm_set):
                            count_plm_completed_by_other += 1
                            worksheet6.write_row(count_plm_completed_by_other, 0, row.values.tolist())
                    else:
                        count_noIntersection += 1
                        worksheet8.write_row(count_noIntersection, 0, row.values.tolist())

        workbook.close()

        tot = count_plmIsSubset + count_otherIsSubset + count_plm_empty + count_other_empty + count_nothing  + count_noIntersection + count_plm_completed_by_other + count_other_completed_by_plm + count_same
        sous_tot = count_plmIsSubset + count_same+count_otherIsSubset + count_plm_completed_by_other + count_other_completed_by_plm+count_noIntersection

        # Create a visual representation of the subsets
        labels = [
            "Subset = PLM",
            "Subset = db",
            "No intersection",
            "Same",
            "Intersection"

        ]

        values = [
            count_plmIsSubset,
            count_otherIsSubset,
            count_noIntersection,
            count_same,
            count_plm_completed_by_other + count_other_completed_by_plm
        ]

        # Create a pie chart
        plt.figure(figsize=(10, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(f"Résulat comparatif de PLM et db = " + str(col_list[-2]) + " sur " + str(sous_tot) + " clusters")
        plt.legend(labels, bbox_to_anchor=(1.09, 0), loc="lower right", fontsize="small", title="Categories")
        plt.savefig(output_dir + f"/" + str(col_list[-2]) + "_distribution.png")
        plt.close()
        
        print("#####################################################################")
        print("Processing completed.")
        print("#####################################################################")
        print("Number of PLM is susbset of " + col_list[-1] + ": ", count_plmIsSubset)
        print("Number of " + col_list[-1] + " is subset of PLM: ", count_otherIsSubset)
        print("Number of PLM empty: ", count_plm_empty)
        print("Number of " + col_list[-1] + " empty: ", count_other_empty)
        print("Number of nothing: ", count_nothing)
        print("Number of no intersection: ", count_noIntersection)
        print(f"Number of PLM completed by " + col_list[-1] + ": ", count_plm_completed_by_other)
        print(f"Number of " + col_list[-1] + " completed by PLM: ", count_other_completed_by_plm)
        print("Number of same: ", count_same)
        print("#####################################################################")
        print("Résultat total :")
        print("Somme total des CK analysé", tot)
        print("Somme total des CK analysé avec prédictions existantes", sous_tot, "soit :", round((sous_tot / tot * 100),2), "%")
        print("#####################################################################")

#==================================================================================================================

if __name__ == "__main__":
	main()