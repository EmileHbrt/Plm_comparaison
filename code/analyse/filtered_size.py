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
    filtered_sequences = {k.split()[0]: v for k, v in sequences.items() if v > treshhold}    
    return filtered_sequences

