# BarPlot_score.py example

This code displays the bar plot of the number of annotated CKs that have at least one such score.

- `<input_file>`: The path of a table with one row per CK, a score column and possibly an annotation column. Other columns may also be present.
- `<output_dir>`: The path of a folder in which to save the plot in jpeg format.
- `<score_column>`: The name a the score column in str
- `<minimal_score>` : The minimal score to be considered on the plot, if missing the minimal score will be considered as 0.5.
- `<annotation_col>` : The colonne containig the method annotations, if missing all row will be considered as annoted. 

```python
# Example usage of Parser_tab.py
python BarPlot_score.py -i <input_file> -o <output_dir>  -c <score_column> -m <minimal_score> -a <annotation_col> 
```

# venn_diagram.py example

This code display the venn diagram of the db that you want to compare with plm result and it gives the number of venn analysis 
- `<input_file>`: The path of combine_tab or a table which contains SeqCluster, ClusterNumber, db_id (plm result) and db_result (that you want to compare) 
- `<output_dir>`: The path of a folder in which to save the plot in png format and to save the xlsx.
- `<col_list>` : The str separated by commas of columns that you want to keep in the xlsx output. The last two must be the result that you've need to compare. See an example in Plm_comparaison/example/README.md
- `<cluster_number>` : The SeqCluster that you want to create a venn diagram of comparaison of the last two result in <col_list>
- `<size_sequence>` : A str of the length maximal of sequences that will be saved (requirement : fasta file and treshold, we encoded that in filtered_size.py automatically

The xlsx file will contain the following worksheets : 
- PLM_Subset
- db_result_Subset
- PLM_empty
- db_result_empty
- nothing
- Plm_completed_by
- completed_by_plm
- No_intersection


Le cas où nous avons aucune donnée pour PLM et InterPro. (“Nothing”)
Le cas où les résultats d’Interpro sont vides. “Interpro_result_empty)
Où PLM est vide : PLM_empty
Le cas où, il y a une intersection, mais Interpro contient plus de résultat que PLM → PLM_completed_by
Le cas où PLM contient plus de résultat que InterPro → completed_by_PLM
Et dans le cas où, il n’y a pas d’intersection, mais bien 2 prédictions différentes. NoInterception.

```python
python venn_diagram.py -i <input_file> -o <output_dir> -c <col_list> -n <cluster_number> -s <size_sequence>
```
