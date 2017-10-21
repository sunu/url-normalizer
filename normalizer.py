"""This module contains functions to help normalize URLs"""

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
    return url

__all__ = ["normalize_url"]
