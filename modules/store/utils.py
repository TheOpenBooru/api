from modules import settings

def generate_generic_url(filename:str) -> str:
    return f"/media/{filename}"


def to_absolute_url(url: str) -> str:
    if not url.startswith("/"):
        return url
    else:
        return get_hostname() + url


def get_hostname():
    hostname, port = settings.HOSTNAME, settings.PORT
    if not settings.SSL_ENABLED:
        if port == 80:
            return f"http://{hostname}"
        else:
            return f"http://{hostname}:{port}"
    else:
        if port == 443:
            return f"https://{hostname}"
        else:
            return f"https://{hostname}:{port}"
