
def filter_none_data(data:dict):
    for k,v in data.items():
        if v is None:
            del data[k]
    
    return data


