def replace_zipcode(postcode): 
    mapping = {
        'c': '73069'
    }
    if postcode in mapping.keys():
        return mapping[postcode]
    return postcode
