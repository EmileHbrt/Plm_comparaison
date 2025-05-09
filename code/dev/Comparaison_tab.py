from optparse import OptionParser
import os
import csv


def main():
    usage = "python Comparaison_tab.py -p <PLM_result> -m <Mapping_CK> -u <Uprot_splited> -o <output_dir> \n"
    parser = OptionParser(usage)
    parser.add_option("-p", "--PLM_result", dest="PLM_result", help="path to the PLM result file")
    parser.add_option("-m", "--Mapping_CK", dest="Mapping_CK", help="Path for the mapping CK csv")
    parser.add_option("-u", "--Uprot_splited", dest="Uprot_splited", help="path to the folder containing Uprot split files")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="path for the folder where the csv will be saved")

    (options, args) = parser.parse_args()
    best5hits = options.PLM_result
    mapping = options.Mapping_CK
    uprot_folder = options.Uprot_splited
    output_dir  = options.output_dir
    
    # création du dictionaire des ClusterNumber: SeqCluster
    with open(mapping, "r",encoding="utf-8") as fichier_read :
        lecteur = csv.reader(fichier_read, delimiter =",")
        Cluster_association_dict={}
        for ligne in lecteur:
            ClusterNumber = ligne[1]
            SeqCluster = ligne[2]
            if ClusterNumber not in Cluster_association_dict :
                Cluster_association_dict[ClusterNumber] = SeqCluster

    #print(Cluster_association_dict)

    # Ouverture des fichiers
    with open(best5hits, "r", encoding="utf-8") as fichier_r_1, \
        open(os.path.join(output_dir, "comparaison_tab.csv"), "w", newline='', encoding="utf-8") as fichier_w:
        
        lecteur_csv_tab = csv.reader(fichier_r_1, delimiter="\t")
        writer = csv.writer(fichier_w, delimiter=",")  # Délimiteur CSV standard (virgule)

        # Écrire l'en-tête
        colones = ['SeqCluster','ClusterNumber','Prot_AC','score', 'RecName', 'InterPro_id', 'InterPro_describe', 'SFLD_id', 'SFLD_describe',
                'PRINTS_id', 'PRINTS_describe', 'Pfam_id', 'Pfam_describe', 'CDD_id', 'CDD_describe',
                'PROFILE_id', 'PROFILE_describe', 'NCBIFAM_id', 'NCBIFAM_describe', 'PROSITE_id', 
                'PROSITE_describe', 'HAMAP_id', 'HAMAP_describe', 'SMART_id', 'SMART_describe',
                'PIRSF_id', 'PIRSF_describe', 'PANTHER_id', 'PANTHER_describe', 'CATHGENE3D_id',
                'CATHGENE3D_describe', 'SSF_id', 'SSF_describe', 'GO_C', 'GO_F', 'GO_P']
        writer.writerow(colones)  # En-tête

        # Processus principal
        for res in lecteur_csv_tab:
            # Initialiser avec des listes pour accumuler les valeurs
            db_dict = {name: [] for name in colones}  
            db_dict['ClusterNumber'] = res[0]  # Initialise le Prot_id
            db_dict['score'] = res[3]
            db_dict['SeqCluster'] = Cluster_association_dict[res[0]]
            id = res[2]
            chemin = os.path.join(uprot_folder, f"{id}_protein.dat")
            
            try:
                with open(chemin, "r", encoding="utf-8") as prot:
                    prot_doc = csv.reader(prot)

                    first_DE = True
                    for ligne_d in prot_doc:
                        ligne = str(ligne_d)[2:-2]
                        if len(ligne) == 0:
                            continue
                        
                        arg_start = ligne[0:2]
                        if arg_start == 'AC':
                            AC_prot = ""
                            for elm in ligne[5:]:
                                if elm != ";":
                                    AC_prot += elm
                                else:
                                    break
                            db_dict['Prot_AC'] = [AC_prot]
                        # Gestion du RecName
                        if arg_start == 'DE' and first_DE:
                            recname = ""
                            first_DE = False
                            for elm in ligne[19:]:
                                if elm == "{":
                                    break
                                else:
                                    recname += elm
                            db_dict['RecName'] = [recname]  # Enregistrer comme une liste contenant une chaîne

                        # Gestion des colonnes DR
                        elif arg_start == 'DR':
                            ligne_elm = ["", "", ""]
                            write_num = 0
                            for elm in ligne[5:]:
                                if elm == ';':
                                    write_num += 1
                                    if write_num > 2:
                                        break
                                else:
                                    ligne_elm[write_num] += elm

                            # Vérifier si les colonnes existent
                            if (ligne_elm[0] + '_id' not in colones) and (ligne_elm[0] + '_C' not in colones):
                                continue
                            

                            if ligne_elm[0] != 'GO':
                                if db_dict[ligne_elm[0] + '_id'] ==[]:
                                    db_dict[ligne_elm[0] + '_id'].append(ligne_elm[1][1:])
                                    db_dict[ligne_elm[0] + '_describe'].append(ligne_elm[2][1:])
                                else:
                                    db_dict[ligne_elm[0] + '_id'].append(" " + ligne_elm[1][1:])
                                    db_dict[ligne_elm[0] + '_describe'].append("," + ligne_elm[2][1:])
                            else:
                                if db_dict[ligne_elm[0] + '_' + ligne_elm[2][1]] == []:
                                    db_dict[ligne_elm[0] + '_' + ligne_elm[2][1]].append(ligne_elm[1][1:]+ "," + ligne_elm[2][2:][1:])
                                else:
                                    db_dict[ligne_elm[0] + '_' + ligne_elm[2][1]].append(";" + ligne_elm[1][1:] + "," + ligne_elm[2][2:][1:])
                            
            except FileNotFoundError:
                print(f"Fichier non trouvé : {chemin}")
            except Exception as e:
                print(f"Erreur avec le fichier {chemin} : {e}")

            try:
                # Convertir les listes en chaînes pour l'écriture
                row = [" ".join(db_dict[col]) if isinstance(db_dict[col], list) else db_dict[col] for col in colones]
                #print(f"Écriture de la ligne : {row}")
                writer.writerow(row)
            except KeyError as e:
                print(f"Clé manquante : {e}")

            

#==================================================================================================================
if __name__ == "__main__":
	main()