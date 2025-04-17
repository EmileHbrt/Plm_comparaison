import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import pandas as pd
import xlsxwriter

tab = pd.read_csv(r"C:\Users\dodol\Documents\GitHub\Plm_comparaison\example\Output\combine_example_tab.csv")

filtered_tab = tab.iloc[:,[0,1,5,36]]

filtered_tab = filtered_tab[filtered_tab['ClusterNumber'].str.startswith('CK')]

count_plmIsSubset = 0
count_interproIsSubset = 0
count_plm_empty = 0
count_interpro_empty = 0
count_nothing = 0
count_plm_completed_by_interpro = 0
count_interpro_completed_by_plm = 0
count_noIntersection = 0

for index, row in filtered_tab.iterrows():

    plm = row['InterPro_id']
    interpro = row['Most represented functional category_x']

    interpro = interpro.replace('|', '  ')

    interpro_set = set(interpro.split())
    plm_set = set(plm.split())

    # Create a new Excel file with multiple sheets (only once, outside the loop)
    if 'workbook' not in locals():
        workbook = xlsxwriter.Workbook(r"C:\Users\dodol\Desktop\test_folder\output_analysis.xlsx")
        worksheet1 = workbook.add_worksheet("PLM_Subset")
        worksheet2 = workbook.add_worksheet("InterPro_Subset")
        worksheet3 = workbook.add_worksheet("PLM_Empty")
        worksheet4 = workbook.add_worksheet("InterPro_Empty")
        worksheet5 = workbook.add_worksheet("Nothing")
        worksheet6 = workbook.add_worksheet("Plm_completed_by_InterPro")
        worksheet7 = workbook.add_worksheet("InterPro_completed_by_PLM")
        worksheet8 = workbook.add_worksheet("NoIntersection")

        # Write the column headers to each worksheet
        headers = filtered_tab.columns.tolist()
        worksheet1.write_row(0, 0, headers)
        worksheet2.write_row(0, 0, headers)
        worksheet3.write_row(0, 0, headers)
        worksheet4.write_row(0, 0, headers)
        worksheet5.write_row(0, 0, headers)
        worksheet6.write_row(0, 0, headers)
        worksheet7.write_row(0, 0, headers)
        worksheet8.write_row(0, 0, headers)

    if len(plm_set) == 0 and len(interpro_set) == 0:
        count_nothing += 1
        worksheet5.write_row(count_nothing, 0, row.values.tolist())

    elif len(plm_set) == 0:
        count_plm_empty += 1
        worksheet3.write_row(count_plm_empty, 0, row.values.tolist())

    elif len(interpro_set) == 0:
        count_interpro_empty += 1
        worksheet4.write_row(count_interpro_empty, 0, row.values.tolist())

    elif plm_set.issubset(interpro_set):
        count_plmIsSubset += 1
        worksheet1.write_row(count_plmIsSubset, 0, row.values.tolist())

    elif interpro_set.issubset(plm_set):
        count_interproIsSubset += 1
        worksheet2.write_row(count_interproIsSubset, 0, row.values.tolist())

    else:
        if len(plm_set.intersection(interpro_set)) != 0:
            if len(plm_set) >= len(interpro_set):
                count_interpro_completed_by_plm += 1  
                worksheet7.write_row(count_interpro_completed_by_plm, 0, row.values.tolist())
            elif len(interpro_set) > len(plm_set):
                count_plm_completed_by_interpro += 1
                worksheet6.write_row(count_plm_completed_by_interpro, 0, row.values.tolist())

        else:
            count_noIntersection += 1
            worksheet8.write_row(count_noIntersection, 0, row.values.tolist())

workbook.close()
   
print(f"Number of PLM is subset of InterPro: {count_plmIsSubset}")
print(f"Number of InterPro is subset of PLM: {count_interproIsSubset}")
print("Number of PLM empty: ", count_plm_empty)
print("Number of InterPro empty: ", count_interpro_empty)
print("Number of nothing: ", count_nothing)
print("Number of no intersection: ", count_noIntersection)
print(f"Number of PLM completed by InterPro: {count_plm_completed_by_interpro}")
print(f"Number of InterPro completed by PLM: {count_interpro_completed_by_plm}")

print(count_plmIsSubset + count_interproIsSubset  + count_plm_completed_by_interpro + count_interpro_completed_by_plm + count_plm_empty + count_nothing + count_interpro_empty+ count_noIntersection)
print(len(filtered_tab))

