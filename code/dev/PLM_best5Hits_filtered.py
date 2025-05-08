import os
import pandas as pd
from optparse import OptionParser


def main():
    usage = "python PLM_best5Hits_filtered.py -i <input_file> -o <output_dir>\n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--best5Hits_file", dest="best5Hits_file", help="path for the file where the PlmSearch result has been registered")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="path where the file filtered will be saved")


    (options, args) = parser.parse_args()
    best5Hits_file = options.best5Hits_file
    output_dir = options.output_dir
   

    try:
        file = open(best5Hits_file)
    except:
        print(' error with -p : correspond to the path of the PlmSearch result')

    
    part = open(os.path.join(output_dir, "PLMSearch_bestHit.out"), "w")

    res = ''

    for ligne in file:
        if ligne.split()[0] != res:
            res = ligne.split()[0]
            part.write(ligne)
    part.close()

#==================================================================================================================
if __name__ == "__main__":
	main()