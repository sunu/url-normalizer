"""Tests for URL normalization"""
import pytest

from ..normalizer import normalize_url

# TODO: parametrize test cases

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
    assert normalize_url("http://example.com/A") == "http://example.com/A"

def test_strip_trailing_period():
    assert normalize_url("http://example.com.") == "http://example.com/"
    assert normalize_url("http://example.com./") == "http://example.com/"

def test_capitalize_escape_sequence():
    """All letters in percent-encoded triplets should be capitalized"""
    assert (normalize_url("http://www.example.com/a%c2%b1b") ==
            "http://www.example.com/a%C2%B1b")

def test_path_percent_encoding():
    """All non-safe characters should be percent-encoded"""
    assert (normalize_url("http://example.com/hello world{}") ==
            "http://example.com/hello%20world%7B%7D")

def test_unreserved_percentencoding():
    """Unreserved characters should not be percent encoded. If they are, they
    should be decoded back; except in case of `/`, `?` and `#`"""
    assert (normalize_url("http://www.example.com/%7Eusername/") ==
            "http://www.example.com/~username")
    assert (normalize_url('http://example.com/foo%23bar') ==
            'http://example.com/foo%23bar')
    assert (normalize_url('http://example.com/foo%2fbar') ==
            'http://example.com/foo%2Fbar')
    assert (normalize_url('http://example.com/foo%3fbar') ==
            'http://example.com/foo%3Fbar')

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
            "https://example.com/abc")

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

def test_query_string():
    """Query strings should be handled properly"""
    assert (normalize_url("http://example.com/?a=1") ==
            "http://example.com/?a=1")
    assert (normalize_url("http://example.com?a=1") ==
            "http://example.com/?a=1")
    assert (normalize_url("http://example.com/a?b=1") ==
            "http://example.com/a?b=1")
    assert (normalize_url("http://example.com/a/?b=1") ==
            "http://example.com/a?b=1")

def test_dont_percent_encode_safe_chars_query():
    """Don't percent-encode safe characters in querystring"""
    assert (normalize_url("http://example.com/a/?face=(-.-)") ==
            "http://example.com/a?face=(-.-)")

def test_query_sorting():
    """Query strings should be sorted"""
    assert (normalize_url('http://example.com/a?b=1&c=2') ==
            'http://example.com/a?b=1&c=2')
    assert (normalize_url('http://example.com/a?c=2&b=1') ==
            'http://example.com/a?b=1&c=2')

def test_query_string_spaces():
    """Spaces should be handled properly in query strings"""
    assert (normalize_url("http://example.com/search?q=a b&a=1") ==
            "http://example.com/search?a=1&q=a+b")
    assert (normalize_url("http://example.com/search?q=a+b&a=1") ==
            "http://example.com/search?a=1&q=a+b")
    assert (normalize_url("http://example.com/search?q=a%20b&a=1") ==
            "http://example.com/search?a=1&q=a+b")

def test_drop_trailing_questionmark():
    """Drop the trailing question mark if no query string present"""
    assert normalize_url("http://example.com/?") == "http://example.com/"
    assert normalize_url("http://example.com?") == "http://example.com/"
    assert normalize_url("http://example.com/a?") == "http://example.com/a"
    assert normalize_url("http://example.com/a/?") == "http://example.com/a"

def test_percent_encode_querystring():
    """Non-safe characters in query string should be percent-encoded"""
    assert (normalize_url("http://example.com/?a=hello{}") ==
            "http://example.com/?a=hello%7B%7D")

def test_normalize_percent_encoding_in_querystring():
    """Percent-encoded querystring should be uppercased"""
    assert (normalize_url("http://example.com/?a=b%c2") ==
            "http://example.com/?a=b%C2")

def test_unicode_query_string():
    """Unicode query strings should be converted to bytes using uft-8 encoding
    and then properly percent-encoded"""
    assert (normalize_url("http://example.com/?file=résumé.pdf") ==
            "http://example.com/?file=r%C3%A9sum%C3%A9.pdf")

def test_unicode_path():
    """Unicode path should be converted to bytes using utf-8 encoding and then
    percent-encoded"""
    assert (normalize_url("http://example.com/résumé") ==
            "http://example.com/r%C3%A9sum%C3%A9")

def test_idna():
    """International Domain Names should be normalized to safe characters"""
    assert (normalize_url("http://ドメイン.テスト") ==
            "http://xn--eckwd4c7c.xn--zckzah/")
    assert (normalize_url("http://Яндекс.рф") ==
            "http://xn--d1acpjx3f.xn--p1ai/")

def test_dont_change_username_password():
    """Username and password shouldn't be lowercased"""
    assert (normalize_url("http://Foo:BAR@exaMPLE.COM/") ==
            "http://Foo:BAR@example.com/")

def test_normalize_ipv4():
    """Normalize ipv4 URLs"""
    assert normalize_url("http://192.168.0.1/") == "http://192.168.0.1/"
    assert (normalize_url("http://192.168.0.1:8080/a?b=1") ==
            "http://192.168.0.1:8080/a?b=1")
    assert normalize_url("192.168.0.1") == "http://192.168.0.1/"
    assert (normalize_url("192.168.0.1:8080/a/b/c") ==
            "http://192.168.0.1:8080/a/b/c")

def test_normalize_ipv6():
    """Normalize ipv6 URLs"""
    assert normalize_url("[::1]") == "http://[::1]/"
    assert normalize_url("http://[::1]") == "http://[::1]/"
    assert normalize_url("[::1]:8080") == "http://[::1]:8080/"
    assert normalize_url("http://[::1]:8080") == "http://[::1]:8080/"

def test_strip_leading_trailing_whitespace():
    """Strip leading and trailing whitespace if any"""
    assert normalize_url("   http://example.com  ") == "http://example.com/"
    assert normalize_url("http://example.com/a  ") == "http://example.com/a"
    assert normalize_url("   http://example.com/") == "http://example.com/"

def test_non_ideal_inputs():
    """Not the ideal input; but we should handle it anyway"""
    assert normalize_url("example.com") == "http://example.com/"
    assert normalize_url("example.com/abc") == "http://example.com/abc"
    assert normalize_url("//example.com/abc") == "http://example.com/abc"

def test_additional_query_args():
    """Add any additional query arguments to the URL"""
    assert (normalize_url("http://example.com?c=d", [("a", "b")]) ==
            "http://example.com/?a=b&c=d")
    assert (normalize_url("http://example.com", [("a", "b")]) ==
            "http://example.com/?a=b")
    assert (normalize_url("http://example.com", [("résumé", "résumé")]) ==
            "http://example.com/?r%C3%A9sum%C3%A9=r%C3%A9sum%C3%A9")

def test_non_urls():
    """If a non-URL string is passed, return None"""
    assert normalize_url("") is None
    assert normalize_url("abc xyz") is None
    assert normalize_url("asb#abc") is None
    assert normalize_url("Яндекс.рф") is not None
    assert normalize_url("google.blog") is not None
    assert normalize_url("http//google.com") is None
    assert normalize_url("http://user@pass:example.com") is None

def test_drop_fragments():
    """Drop or keep fragments based on the option passed"""
    assert (normalize_url("http://example.com/a?b=1#frag")
            == "http://example.com/a?b=1")
    assert (normalize_url("http://example.com/a?b=1#frag", drop_fragments=False)
            == "http://example.com/a?b=1#frag")

def test_non_string_input():
    """Non-string input should produce None as result"""
    assert normalize_url(None) is None
    assert normalize_url([]) is None
    assert normalize_url(123) is None
