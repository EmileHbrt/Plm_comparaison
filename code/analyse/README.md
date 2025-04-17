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
