# Example of programme use 

NB: some programs directly use the name of the file that will be created in the output path (such as Combine_tab.py or Parser_tab.py), others simply require the path where a new file will be created (such as Interpro_parse.py , BarPlot_score.py or Create_tab.py)

## Input folder

The 'Input' file contains :
 - 'example_interpro.xml' is an example of an xml file constructed in the same way as the interpro.xml file, but which contains only 3 iterpro_ids. 
 - 'example_uniprot.txt' is an example of an txt file constructed in the same way as the uniprot_sprot.dat file, but which contains only 3 proteins.

## Output folder

The 'Output' file contains : 
 - 'File_Interpro_example' is a folder containing the results obtained using Interpro_parse.py on the example_interpro.xml file.
 - 'parsed_example_tab.csv' is a csv file obtained by parsing comparison_tab.csv from data(see next).
 - 'File_Uniprot_example' is a folder containing the results obtained using Uni_parse.py on the example_uniprot.txt file. 
 
## How to use Dev codes

###  Interpro_parse.py

```python
python code\dev\Interpro_parse.py -i example\Input\example_interpro.xml -o example\Output\File_Interpro_example
```
You can know see the results in Example\Output\File_Interpro_example !

### Parser_tab.py 

```python
python code\dev\Parser_tab.py -i data\comparaison_tab.csv -o example\Output\parsed_example_tab.csv -s 0.8 -c SeqCluster,Prot_AC,score,RecName
```
You can now see a csv in the folder, with the four columns indicated and only scores above 0.8 !

### Uni_parse.py 

```pyhton
python code\dev\Uni_parse.py -i example\Input\example_uniprot.txt -o example\Output\File_Uniprot_example
```
You can know see the results in example\Output\File_Uniprot_example !

### Create_tab.py
```pyhton
python code\dev\Create_tab.py -p "example\Input\example_PLMSearch_bestFirstHits.out" -o example\Output\File_Uniprot_example
```

### Combine_tab.py

```python
python code\dev\Combine_tab.py -i data\comparaison_tab.csv,data\Interpros.filtered.csv,data\Pfam.filtered.csv,data\GoTerms_filtered_for_cyanorak.csv -o example\Output\combine_example_tab.csv -c SeqCluster
```

## How to use Analyse codes

### BarPlot_score.py
```python
python code\analyse\BarPlot_score.py -i example\Output\combine_example_tab.csv -o example\Output -c score -m 0.5 -a Prot_AC
```