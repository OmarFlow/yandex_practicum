import json

def create_error_msg(field, error):
    return {
        'field': field,
        'error': error
    }



def validator(data):
    try:
        int(data.get('limit'))
    except ValueError as e:
        return json.dumps(create_error_msg('limit', e))