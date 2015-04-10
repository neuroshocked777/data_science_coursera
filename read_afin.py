def read_afin(afin_file):
    """(file open for reading) -> dict

    	Read file returns dict

    >>> read_scen(obj_file)
    {'key1': 2, 'key2': -2   
    """
    scores = {}
    for line in afin_file.readlines():
        (term, score) = line.split('\t')
        scores[term] = int(score)
    print scores.items()

filepath = 'AFFIN-111.txt'
afin_file = open(filepath, 'r')
read_afin(afin_file)
