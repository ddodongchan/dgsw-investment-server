from urllib.parse import urlparse, parse_qs

from pydantic import HttpUrl

def extract_code_from_location(location: HttpUrl) -> str | None:
    parsed_url = urlparse(str(location))
    query_params = parse_qs(parsed_url.query)
    code_list = query_params.get("code")
    return code_list[0] if code_list else None