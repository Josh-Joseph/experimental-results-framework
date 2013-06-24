
import json

#----------------------------------------------------------------------------

def is_hashable( obj ):
    """Returns true iff the given object is hashable.
       This computes the hash itself, so it works every time :-)"""
    
    try:
        hash( obj )
    except TypeError:
        return False
    return True


#----------------------------------------------------------------------------

##
## Description:
## A global list of registered podify transformation.
## This list is ordered, and each element is a tuple with
## ( predicate,  transfrom, name ) where the first two are functions.
##
## predicte: python object -> True if tranform should be applied
## transform: python object -> POD object
## name: a string
_registered_podify_transforms = []


#----------------------------------------------------------------------------

def register_podify_transform( predicate, transform, name="" ):
    """Register a podify transform with an optional name.
       Returns a trasnform token useful to remove the transform later on
       if wanted.
       
       Arguments:
       predicate -- A one-argument function which returns true iff the given 
                    tranform function should be applied to podify an object.
       transform -- A one-argument function which *must* return A POD version
                    of any object which passes the predicate.
       name (optiona) -- A name for this transform (mostly for debugging)
       """
    
    _registered_podify_transforms.append( (predicate, transform, name ) )
    return len( _registered_podify_transforms ) - 1


#----------------------------------------------------------------------------

def unregister_podify_transform( transform_token ):
    """Removes the given trasnform token (as returned by 
       register_podify_transform) form the transforms used by podify."""
    
    del _registered_podify_transforms[ transform_token ]


#----------------------------------------------------------------------------

def _try_podify_transforms( obj ):
    """Iterates over all registered podify transforms and uses the first one
       whoose predicate returns true for the given object.
       Returns two values: ( transform-result, found )
       where found is True if a transform was run, and the resutls of the
       transform are returned in the first value.
       The second result is used to determine whetehr a transform was run and
       returned None."""
    
    for pred,trans,name in _registered_podify_transforms:
        if pred( obj ):
            return trans( obj ), True
    return None, False

#----------------------------------------------------------------------------

def podify( obj, use_transforms=True ):
    """Returns a "Plain-0l-Datatype" version of the given object.
       This means that the returned object comporises only of the
       following:
         dict
         list
         int
         float
         string
       This method recusively calls podify in a structured object to make
       sure the above types are the only ones used. Mainly it calls str()
       on any object which is not the above type :-).
       
       Also of note, one can register a "podify transform" with the module.
       Transforms include a predicate determinig whether it should be applied,
       and are assumed to return a valid POD type once called with an object.
       You can of course recourse podify(...) inside a transform, but make sure
       you do not cause infinite loops (or call with use_transforms=False )"""

    # First, check if we are using transforms and there are any that match
    if use_transforms and _registered_podify_transforms:
        pod_obj, found = _try_podify_transforms( obj )
        if found:
            return pod_obj
    
    # Either no trasnforms registerd for this object, or we are not using them
    # Try a fixed ordering for podify types
    if isinstance( obj, str ):
        return obj
    if isinstance( obj, int ):
        return obj
    if isinstance( obj, float ):
        return obj
    if isinstance( obj, list ):
        return map( podify, obj )

    # dictionaries are special, we first check each item to see if a transform
    # is registered, if not then we podify key and value separately
    if isinstance( obj, dict ):
        pod_t = {}
        for k,o in obj.iteritems():
            found = False
            if use_transforms and _registered_podify_transforms:
                (tk,to), found = _try_podify_transforms( (k,o) )
            if not found:
                tk = podify( k )
                if not is_hashable( tk ):
                    tk = str(tk)
                to = podify( o )
            pod_t[ tk ] = to
        return pod_t
    if isinstance( obj, tuple ):
        return podify( list( obj ) )
    if isinstance( obj, type ):
        return str( obj.__name__ )
    return str(obj)

#----------------------------------------------------------------------------

def to_json( obj ):
    """Return a JSON represetation of the given python object as a string.
       This method first calls podify( obj ) and then transform the now
       POD object into JSON encoding."""
    
    return json.dumps( podify( obj ), separators=(',',':') )

#----------------------------------------------------------------------------

def from_json( json_str ):
    """Load JSON encoded object from the given string into a python object.
       The JSON string will have only POD types, hence the returned python
       object will be a POD object as well."""

    return json.loads( json_str )

#----------------------------------------------------------------------------

def parse_json_dict(dict_as_json_str):
    """Attempt to parse a json string representation of a dictionary and gracefully handle 'None's.

    This function will raise a ValueError if the json string cannot be parsed into a dict.

    Parameters
    ----------
    dict_as_json_str : string or None
        A json string representation of a dictionary.

    Returns
    -------
    parsed_dict : dict
        Returns a new dictionary with all elements parsed as json if possible or an empty dictionary if
        dict_as_json_str is None.
    """
    if dict_as_json_str is None:
        return {}
    parsed_dict = json.loads(dict_as_json_str)
    if type(parsed_dict) is not dict:
        raise ValueError('The string ' + dict_as_json_str + ' was not parsed into a dictionary.')
    return parsed_dict

#----------------------------------------------------------------------------

def try_to_parse_dict_values_json(raw_dict):
    """Attempt to parse each element of the dictionary using json.loads

    Parameters
    ----------
    raw_dict : dict
        The dictionary to be parsed.

    Returns
    -------
    parsed_dict : dict
        Returns a new dictionary with all elements parsed as json if possible.
    """
    parsed_dict = dict()
    for key, value in raw_dict:
        try:
            parsed_value = json.loads(value)
        except (ValueError, TypeError):
            parsed_value = value
        parsed_dict[key] = parsed_value
    return parsed_dict


#-----------------------------------------------------------------------------

def structured_key_to_list( skey, separator="." ):
    """Returns a list representation of the strucutred key.
       This splits "a.b.c" into [ "a", "b", "c" ].
       The optional separator to use to define sturctured keys (default .)"""
    
    return skey.split( separator )

#-----------------------------------------------------------------------------

def structure_has( skey, d, separator="."  ):
    """Returns true iff the given structure key is inside the dictionary.
       Each element of the structure is treated as a subdictionary.
       Optionaly, give the spearator to use for structured keys."""

    klist = structured_key_to_list( skey, separator )
    subd = d
    for k in klist:
        if not k in subd:
            return False
        subd = subd[k]
    return True

#-----------------------------------------------------------------------------

def structure_get( skey, d, separator=".", default=None  ):
    """Returns the element at the sturctured key in hte dictionary.
       Each element of the structure is treated as a subdictionary.
       Optionally, give the separator to use for structured keys."""

    klist = structured_key_to_list( skey, separator )
    subd = d
    for k in klist:
        if not k in subd:
            return default
        subd = subd[k]
    return subd

#-----------------------------------------------------------------------------

def structure_put( skey, val, d, separator="." ):
    """Puts a given value into a sturcutred key.
       This creates subdictionaries as needed for the structured key."""
    
    klist = structured_key_to_list( skey, separator )
    subd = d
    for k in klist[:-1]:
        if not k in subd:
            subd[k] = {}
        subd = subd[k]
    subd[klist[-1]] = val
    return d

