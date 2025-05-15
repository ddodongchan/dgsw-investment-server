from uuid import UUID

def convert_to_redis_compatible(data: dict) -> dict:
    new_data = {}
    for k, v in data.items():
        if isinstance(v, UUID):
            new_data[k] = str(v)
        elif isinstance(v, (int, float, str)):
            new_data[k] = v
        else:
            new_data[k] = str(v)
    return new_data
