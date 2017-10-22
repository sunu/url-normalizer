"""Tests for URL normalization"""
import pytest

from normalizer import normalize_url


def test_normalized_urls():
    """Already normalized URLs should not change"""
    assert normalize_url("http://example.com/") == "http://example.com/"

def test_return_type():
    """Should return string"""
    assert isinstance(normalize_url("http://example.com/"), str)

def test_append_slash():
    """Append a slash to the end of the URL if it's missing one"""
    assert normalize_url("http://example.com") == "http://example.com/"

def test_lower_case():
    """Normalized URL scheme and host are lower case"""
    assert normalize_url("HTTP://examPle.cOm/") == "http://example.com/"

def test_capitalize_escape_sequence():
    """All letters in percent encoded triplets should be capitalized"""
    assert (normalize_url("http://www.example.com/a%c2%b1b") ==
            "http://www.example.com/a%C2%B1b")

def test_unreserved_percentencoding():
    """Unreserved characters should not be percent encoded. If they are, they
    should be decoded back"""
    assert (normalize_url("http://www.example.com/%7Eusername/") ==
            "http://www.example.com/~username/")

def test_remove_dot_segments():
    """Convert the URL path to an absolute path by removing `.` and `..`
    segments"""
    assert (normalize_url("http://www.example.com/../a/b/../c/./d.html") ==
            "http://www.example.com/a/c/d.html")

def test_remove_default_port():
    """Remove the default port for the scheme if it's present in the URL"""
    assert (normalize_url("http://www.example.com:80/bar.html") ==
            "http://www.example.com/bar.html")
    assert (normalize_url("HTTPS://example.com:443/abc/") ==
            "https://example.com/abc/")

def test_remove_empty_port():
    """Remove empty port from URL"""
    assert (normalize_url("http://www.example.com:/") ==
            "http://www.example.com/")

def test_remove_extra_slash():
    """Remove any extra slashes if present in the URl"""
    # TODO: Should we actually do this?
    # TODO: See https://webmasters.stackexchange.com/questions/8354/what-does-the-double-slash-mean-in-urls/8381#8381
    assert (normalize_url("http://www.example.com/foo//bar.html") ==
            "http://www.example.com/foo/bar.html")
    assert(normalize_url("http://example.com///abc") ==
           "http://example.com/abc")
