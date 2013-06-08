
import json



def to_json( obj ):
    return json.dumps( obj, separators=(',',':') )


def from_json( json_str ):
    return json.loads( json_str )

