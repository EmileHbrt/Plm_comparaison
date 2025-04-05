import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import pandas as pd

tab = pd.read_csv(r"C:\Users\dodol\Documents\GitHub\Plm_comparaison\example\Output\combine_example_tab.csv")


# Filter the DataFrame to keep only the specified columns
filtered_tab = tab.iloc[:,[0,1,5,36]]
# print(filtered_tab)

# Select rows where the 'ClusterNumber' column starts with 'CK'
filtered_tab = filtered_tab[filtered_tab['ClusterNumber'].str.startswith('CK')]
#print(filtered_tab)

# Save the filtered DataFrame to a new CSV file
#filtered_tab.to_csv(r"C:\Users\dodol\Documents\GitHub\Plm_comparaison\example\Output\filtered_tab_interpro.csv", index=False)

# Iterate through the rows of the filtered DataFrame
for index, row in filtered_tab.iterrows():
    # Create a new figure for each row to avoid memory issues
    fig, ax = plt.subplots(figsize=(8, 4))

    # Extract the relevant columns for the current row
    plm = row['InterPro_id']
    interpro = row['Most represented functional category_x']

    # Replace '|' with ' ' in the 'interpro' variable
    interpro = interpro.replace('|', '  ')

    # Convert 'interpro' and 'plm' into sets
    interpro_set = set(interpro.split())
    plm_set = set(plm.split())

    # Create a Venn diagram with labels showing the elements of the sets
    venn = venn2([plm_set, interpro_set], ('PlmSearch', 'InterPro'), ax=ax)
    plt.show()
    break






