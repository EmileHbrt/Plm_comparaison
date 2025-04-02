# Combine_tab.py Dorian & Emile

from optparse import OptionParser
import pandas as pd

#==================================================================================================================

def writer_tab(df, output : str ):
	"""
	writes the panda table as a csv in the output file

	args:
	"df" : the panda table that you need to write
	"output" : path for the outuput 
	"""
	df.to_csv(output,index=False)	
      
#==================================================================================================================

def list_lecter(str_arg :str ):
    """
    returns, from a list in str form, a list of arrays read with panda 

    arg :
    "str_arg" : list of path in str form 
    """
    tab_list = [] 
    path = ''

    for elm in str_arg:
        if elm == "," :
            try:
                tab = pd.read_csv( path , low_memory=False)
            except:
                print(' error with -i : comma-separated list of all the dataset paths you want to collect')
				
            tab_list.append(tab)
            path = ''
        else :
            path += elm
    try:
        tab = pd.read_csv( path , low_memory=False)
    except:
        print(' error with -i : comma-separated list of all the dataset paths you want to collect')        
    tab_list.append(tab)

    return  tab_list
#==================================================================================================================

def merge_tab(tab_list : list , shared_col : str) : 
    """
    returns a single array from a list of panda table

    args:
    "tab_list" : a list of panda table
    "shared_col" : name of the shared column 
    """
    rep = tab_list[0]
	
    for tab in tab_list[1:] :
        rep = pd.merge( rep, tab , on = shared_col , how = "outer")

    rep = rep.fillna(' ')

    return rep   

#==================================================================================================================

def main():
    usage = usage = "python Combine_tab.py -i <list_input_file> -o <output_file> -c <combine_col> \n" 
    parser = OptionParser(usage)
    parser.add_option("-i", "--list_input_file", dest="list_input_file", help="comma-separated list of all the dataset paths you want to collect")
    parser.add_option("-o", "--output_file", dest="output_file", help="path for the file combine")
    parser.add_option("-c", "--combine_col", dest="combine_col", help="name of the column on which we want to group the various datasets")
	
    (options, args) = parser.parse_args()
    input_list = options.list_input_file
    output_file = options.output_file 
    shared_col = options.combine_col

    tab_list = list_lecter(input_list)

    if len(tab_list) <= 1:
        raise ValueError("problem with list_input_file is empty or of len 1")

    result = merge_tab(tab_list, shared_col) 

    try :
        writer_tab(result, output_file)
    except:
        print(' error with -o : correspond to the parsed dataset path ')



#==================================================================================================================
if __name__ == "__main__":
	main()