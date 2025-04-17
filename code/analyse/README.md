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
- `<col_list>` : The str separated by commas of columns that you want to keep in the xlsx output. The last two must be the result that you've need to compare. See an example in Plm_comparaison/example/output/README.md
- `<cluster_number>` : The SeqCluster that you want to create a venn diagram of comparaison of the last two result in <col_list>

```python
python venn_diagram.py -i <input_file> -o <output_dir> -c <col_list> -n <cluster_number>
```
