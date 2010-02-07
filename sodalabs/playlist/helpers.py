def ordered_unique(seq, idfun=None): # Alex Martelli ******* order preserving
    """
    This is mainly for taking a tracks list and ensuring it contains a unique set of tracks.
    """
    if idfun is None:
        def idfun(x): 
            return x['artist'] + x['name']

    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker not in seen:
            seen[marker] = 1
            result.append(item)
            
    return result


