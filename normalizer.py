"""This module contains functions to help normalize URLs"""
from os.path import normpath
import string
from urllib.parse import (
    urlparse, urlunparse, unquote, quote, urlencode, parse_qsl
)

# Reserved delimeters from https://tools.ietf.org/html/rfc3986#section-2.2
GEN_DELIMS = ":/?#[]@"
SUB_DELIMS = "!$&'()*+,;="
RESERVED_CHARS = GEN_DELIMS + SUB_DELIMS

# Unreserved characters from https://tools.ietf.org/html/rfc3986#section-2.3
UNRESERVED_CHARS = string.ascii_letters + string.digits + "-._~"

SAFE_CHARS = RESERVED_CHARS + UNRESERVED_CHARS + '%'

# TODO: Add more schemes may be
DEFAULT_PORTS = {
    "http": 80,
    "https": 443
}

def normalize_url(url, query_args=None):
    """Normalize a url to its canonical form.

    Parameters
    ----------
    url: str
        URL to be normalize
    query_args: list of 2-element tuples, optional
        A list of tuples with further query arguments that need to be appended
        to the URL

    Returns
    -------
    str
        A normalized url with supplied extra query arguments
    """
    parts = urlparse(url)
    scheme, netloc, path, params, query, fragment = (
        parts.scheme, parts.netloc, parts.path, parts.params, parts.query,
        parts.fragment
    )

    # unquote and quote the path so that any non-safe character is
    # percent-encoded and already percent-encoded triplets are upper cased.
    unquoted_path = unquote(path)
    path = quote(unquoted_path, SAFE_CHARS) or "/"
    # Use `os.path.normpath` to normalize paths i.e. remove duplicate `/` and
    # make the path absolute when `..` or `.` segments are present.
    # But `normpath` gets rid of trailing slashes if it's not in the beginning
    # of the path. For example `/abc/` becomes `/abc'. This makes sense in
    # for a file system but not for URLs. We want the trailing slashes to stay.
    # TODO: Should we remove duplicate slashes?
    # TODO: See https://webmasters.stackexchange.com/questions/8354/what-does-the-double-slash-mean-in-urls/8381#8381
    has_trailing_slash = (path[-1] == "/")
    path = normpath(path)
    if has_trailing_slash and path[-1] != "/":
        path += "/"

    # normalize to lowercase and strip empty port if any
    netloc = netloc.lower().rstrip(":")
    # strip default port
    if parts.port and DEFAULT_PORTS.get(scheme) == parts.port:
        netloc = netloc.rstrip(":"+str(parts.port))

    # Percent-encode and sort query arguments.
    queries_list = parse_qsl(query)
    queries_list.sort()
    query = urlencode(queries_list, safe=SAFE_CHARS)

    # Put the url back together
    url = urlunparse((scheme, netloc, path, params, query, fragment))
    return url

__all__ = ["normalize_url"]
