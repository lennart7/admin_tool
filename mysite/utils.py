def map_guidebox_keys(record):
    """Map guidebox keys to our local keys"""
    record = {key: value for key, value in record.items()
              if not key.endswith('_id')}
    key_map = {'alternate_titles': 'alternative_titles',
               'id': 'guidebox_id'}
    mapped_record = {}
    for key, val in record.items():
        mapped_record[key_map.get(key, key)] = val
    return mapped_record
