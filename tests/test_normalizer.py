"""Tests for URL normalization"""
import pytest

from normalizer import normalize_url


def test_normalized_urls():
    """Already normalized URLs should not change"""
    assert normalize_url("http://example.com/") == "http://example.com"

def test_return_type():
    """Should return string"""
    assert isinstance(normalize_url("http://eample.com/"), str)

def test_append_slash():
    """Append a slash to the end of the URL if it's missing one"""
    assert normalize_url("http://example.com") == "http://example.com/"

def test_lower_case():
    """Normalized URL scheme and host are lower case"""
    assert normalize_url("HTTP://examPle.cOm/") == "http://example.com/"
