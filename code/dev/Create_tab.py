import csv 
import pandas as pd
import re
from optparse import OptionParser


#==================================================================================================================
def writter_tab(dict, output):
    '''Create tab.csv '''
    with open(output + '/informative_tab.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=dict.keys())
        if file.tell() == 0:  # Write header only if the file is empty
            writer.writeheader()
        writer.writerow(dict)

#==================================================================================================================
# 											main
#==================================================================================================================

def main():
    usage = "python Create_tab.py -p <bestHit_file> -d <input_dir> -o <output_dir> \n"
    parser = OptionParser(usage)
    parser.add_option("-p", "--bestHit_file", dest="bestHit_file", help="path for the folder where the PlmSearch result is")
    parser.add_option("-d", "--input_dir", dest="input_dir", help="path for the folder where the Uniport database have been splited")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="path for the folder where the csv will be saved")

    (options, args) = parser.parse_args()
    bestHit_file = options.bestHit_file
    input_dir = options.input_dir
    output_dir  = options.output_dir

    try:
        bestHit_file = open(bestHit_file)
    except:
        print(' error with -p : correspond to the path of the PlmSearch result')

    i = 0

    for line in bestHit_file:
        dico = {
            'Protein_ID' : '',
            'AC' : '',
            'Score' : '',
            'RecName' : '',
            'InterPro' : '',
            'InterPro_Description' : '',
            'ANTIFAM' : '',
            'ANTIFAM_Description' : '',
            'CATHGENE3D' : '',
            'CATHGENE3D_Description' : '',
            'CDD' : '',
            'CDD_Description' : '',
            'HAMAP' : '',
            'HAMAP_Description' : '',
            'NCBIFAM' : '',
            'NCBIFAM_Description' : '',
            'PANTHER' : '',
            'PANTHER_Description' : '',
            'Pfam' : '',
            'Pfam_Description' : '',
            'PIRSF' : '',
            'PIRSF_Description' : '',
            'PRINTS' : '',
            'PRINTS_Description' : '',
            'PROFILE' : '',
            'PROFILE_Description' : '',
            'PROSITE' : '',
            'PROSITE_Description' : '',
            'SUPFAM' : '',
            'SUPFAM_Description' : '',
            'Go_terms biological_process' : '',
            'Go_terms cellular_component' : '',
            'Go_terms molecular_function' : ''
            }
        CK = line.split()[0]
        AC = line.split()[2]
        score = float(line.split()[3])
        dico['Protein_ID'] = CK
        dico['AC'] = AC
        dico['Score'] = score

        try: 
            protein_file = open(input_dir + '\\'+ AC + "_protein.dat")
        except:
            print('error with -i : a protein file is missing :' , AC + "_protein.dat in the folder where the Uniprot database have been splited" , i )
            i += 1
            
            continue
    
        for li in protein_file:
            if li.startswith('DE') and 'RecName' in li:
                dico['RecName'] = re.search(r"RecName: Full=(.*?);", li).group(1)

                for li in protein_file:
                    if li.startswith('DR'):
                        parts = li.split(";")
                        db_name = parts[0].split()[1]

                        if db_name in dico:
                            dico[db_name] += parts[1].split()[0] + " "
                            if len(parts) > 2:
                                dico[f"{db_name}_Description"] += parts[2].split()[0] + ","
                            print(db_name)
                        if db_name == 'GO':
                            go_terms = parts[1].split(':')[1].strip()
                            go_category = parts[2].split(':')[0].strip()
                            go_description = parts[2].split(':')[1].strip()
                            print(go_terms, go_description)

                            if go_category == 'P':
                                dico['Go_terms biological_process'] += 'GO:'+ go_terms + ' ' + go_description + ','
                            elif go_category == 'C':
                                dico['Go_terms cellular_component'] += 'GO:' + go_terms + ' ' + go_description + ','
                            elif go_category == 'F':
                                dico['Go_terms molecular_function'] += ' GO:' + go_terms + ' ' + go_description + ','
        for key in dico:
            if key.endswith('_Description'):
                dico[key] = dico[key][:-1]

        writter_tab(dico, output_dir)
        
#==================================================================================================================
if __name__ == "__main__":
	main()