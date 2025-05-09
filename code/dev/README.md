# Uni_parse.py example 

This code is used to split Uniprot database to get one file (.dat) per protein with the informations of the protein.

- `<input_file>`: The path of the Uniprot file. Example: [[Uniprot file](https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz)].
- `<output_dir>`: The directory where the split Uniprot files will be saved.

```python
# Example usage of Uni_parse.py
python Uni_parse.py -i <input_file> -o <output_dir>
```

# Interpro_parse.py example
This code is used to get a mapping of InterPro Accession number with all database in InterPro

Thie code is used to parse Interpro database.
It creates, for each database in [[Interpro file](https://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro.xml.gz)] <input_file>
,a csv with Id_protein and it shortname
,as well as a csv with interpro_id and all matching database_id.
Also a csv with all interpro_id and their EC_number.
- `<input_file>`: The path to the input file containing the data to be parsed.
- `<outpu_dir>` is the direction where the split of uniprot file are going to be saved

```python
# Example usage of Interpro_parse.py
# Run the script with an input file and specify the output directory
python Interpro_parse.py -i <input_file> -o <output_dir> 
```

# Comparaison_tab.py example 

This code is used to obtain an informative csv with the best prediction of Plmsearch for each unknowed CK in Cyanorak. 

- `<bestHit_file>`: The path to the prediction of PLMsearch
- `<Mapping_CK>`: The path where the CK is correleted with SeqCluster
- `<Uprot_splited>`: The path of the folder where Uniport have been splited 
- `<output_dir>`: The path where the output file will be saved.

```python
# Example usage of Comparaison_tab.py
python Comparaison_tab.py -p <bestHit_file> -m <Mapping_CK> -u <Uprot_splited> -o <output_dir>
```
# Combine_tab.py example

This code is used to combine several tables based on a common column.

- `<list_input_file>`: A comma-separated list of all the dataset paths you want to collect.
- `<output_file>`: The path where the output file will be saved.
- `<combine_col>`: Name of the column on which we want to group the various datasets.

```python
# Example usage of Combine_tab.py
python Combine_tab.py -i <list_input_file> -o <output_file> -c <combine_col>
```
  
# Parser_tab.py example

This code is used to parse the complete tab / comparaison_tab csv 

- `<input_file>`: The path to the input file containing the data to be parsed.
- `<output_file>`: The path where the output file will be saved.
- `<score_arg>`: the minimum selection score for the output .
- `<col_list>`: A comma-separated list of column names to include in the output file.
- `<len_arg>`: the len minimal of sequences of amino-acids that will be parsed
- 
```python
# Example usage of Parser_tab.py
python Parser_tab.py -i <input_file> -o <output_file> -s <score_arg> -c <col_list> -t <len_arg>
```
