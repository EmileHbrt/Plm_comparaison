# Uni_parse.py example 

This code is used to split Uniprot database to get one file (.dat) per protein with the informations of the protein.

- `<input_file>`: The path of the Uniprot file. Example: [[Uniprot file](https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz)].
- `<output_dir>`: The directory where the split Uniprot files will be saved.

```python
# Example usage of Uni_parse.py
# Run the script with an input file and specify the output directory
python Uni_parse.py -i <input_file> -o <output_dir>
```

# Interpro_parse.py example

Thie code is used to parse Interpro database.
It creates, for each database in [[Interpro file](https://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro.xml.gz)] (.xml) <input_file> 
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

# Informative_csv example 

This code is used to obtain an informative csv with the best prediction of Plmsearch for each unknowed CK in Cyanorak. 


# Plm_compare.py example

This code is used to parse the informative csv 

- `<input_file>`: The path to the input file containing the data to be parsed.
- `<output_file>`: The path where the output file will be saved.
- `<score_arg>`: the minimum selection score for the output .
- `<col_list>`: A comma-separated list of column names to include in the output file.

```python
# Example usage of Plm_compare.py
python Parser_tab.py -i <input_file> -o <output_dir> -s <score_arg> -c <col_list>
```
