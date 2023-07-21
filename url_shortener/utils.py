import uuid
from .models import ShortenedURL


def generate_short_code(length=10):
    """Generate a unique short code."""
    # 62^10 = 839299365868340224 combinations 26 upper+ 26lower + 10digits = 62
    short_code = str(uuid.uuid4().hex)[:length]
    if ShortenedURL.objects.filter(short_code=short_code).exists():
        return generate_short_code()
    return short_code


def generate_short_url(original_url):
    """Generate a short url."""
    while True:
        short_code = generate_short_code()
        # IF it doesn't exist, create the short url
        if not ShortenedURL.objects.filter(short_code=short_code).exists():
            ShortenedURL.objects.create(
                original_url=original_url, short_code=short_code
            )
            return short_code
