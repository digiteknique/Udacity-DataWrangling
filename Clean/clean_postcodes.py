def replace_zipcode(postcode): 
    mapping = {
        'c': '73069'
    }
    if postcode in mapping.keys():
        return mapping[postcode]
    if len(postcode) > 5:
        postcode = postcode[:5]
    return postcode
