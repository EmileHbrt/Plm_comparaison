import os
import csv
import pandas as pd
import xml.etree.ElementTree as ET

from optparse import OptionParser


def main():
    usage = "python Interpro_parse.py -i <input_file> -o <output_folder> \n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="path for the Interpro dataset")
    parser.add_option("-o", "--output_folder", dest="output_folder", help="path to the folder where the data will be saved")

    (option, args) = parser.parse_args()
    input_file = option.input_file
    output_file = option.output_file

    try:
        xml = open(input_file, "r", encoding='utf-8')
    except:
        print(' error with -i : correspond to the path of the dataset ')

    # version code perso create_db
    all_db = {} # {db = [[id,name], ...], ...} avec le shortname pour interpro

    # version perso create_map_db
    map_interpro = {} # {Interpro_id = ['', '', '', ...]
                      # db = ['', '', '', ...] 
                      # ... }
    
    # version perso create_ec
    ec_number = {} # { Interpro_id = [ec_1, ec_2, ...], ...}



#==================================================================================================================
if __name__ == "__main__":
	main()