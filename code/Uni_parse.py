# Uni_parse Dorian & Emile

from optparse import OptionParser

def main():

    usage = usage = "python Uni_parse.py -i <input_file> -o <output_file> \n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="path for the Uniprot dataset")
    parser.add_option("-o", "--output_file", dest="output_file", help="path for the folder of results")

    (options, args) = parser.parse_args()
    input_file = options.input_file
    output_file = options.output_file

    Uni_db = open(input_file, "r", encoding='utf-8')
    
    txt = ''
    file_name = ''

    for ligne in Uni_db:
        arg_start = ligne[0:2]

        if arg_start == 'AC':
            name = ""
            for elm in ligne[5:]:
                if elm == ';':
                    break
                else:
                    name += elm
            file_name = output_file + '\\' + name + ".dat"
            txt += ligne

        elif arg_start in ['ID', 'DE', 'OC', 'DR','SQ','  ']:
            txt += ligne   
        elif arg_start == '//':   
            with open(file_name, 'w') as fichier:
                fichier.write(txt)
            txt = ''    

#==================================================================================================================

if __name__ == "__main__":
	main()
