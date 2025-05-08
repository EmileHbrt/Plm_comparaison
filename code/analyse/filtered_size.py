import pandas as pd

def read_Fasta(fasta):
    """
    Read a FASTA file and return a dictionary with sequence IDs as keys and the length of the sequences as values.
    """
    sequences = {}

    with open(fasta, 'r') as f:
        seq_id = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if seq_id is not None:
                    sequences[seq_id] = len(''.join(seq))
                seq_id = line[1:]
                seq = []
            else:
                seq.append(line)
        if seq_id is not None:
            sequences[seq_id] = len(''.join(seq))
    return sequences



def filtre_size(fasta, treshhold):
    """
    Filter sequences based on a given threshold.
    """
    sequences = read_Fasta(fasta)
    filtered_sequences = {k.split()[0]: v for k, v in sequences.items() if v >= treshhold}    
    return filtered_sequences

### Annexe pour la réunion de GO termes - GO_C GO_F GO_P 

def join_col(tab, col):
    """
    Joint les colonnes du tableaux 
    """
    table = pd.read_csv(tab)

    headers = table.columns.tolist()

    for elm in col :
        if elm not in headers:
            return "error with headers doesn't match" 

    table['GO_joined'] = table[col].apply(
        lambda row: '|'.join([elm.split(',')[0] for elm in ';'.join(row.dropna().astype(str)).strip(';').split(';') if elm.startswith('GO:')]),
        axis=1
    )

    return table


