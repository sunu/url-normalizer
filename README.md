URL-NORMALIZER
==============

[![Build Status](https://travis-ci.org/sunu/url-normalizer.svg?branch=master)](https://travis-ci.org/sunu/url-normalizer)

Normalizes URL by doing the following:

- Lower casing the hostname and scheme
- Uppercasing percent-encoded characters
- Encoding to bytes using utf-8 encoding and only performing percent-encoding when necessary
- Converting path to its absolute form and getting rid of dot segments
- Dropping default port
- Appending "/" to hostname
- Providing "http" as default scheme when a scheme is missing
- Converting international domain names to their ASCII form
- Getting rid of trailing `.` or `:` from the address
- Dropping fragments
- Sorting query arguments
- Dropping trailing `?` in case of empty query string
- Stripping redundant `/` in the path

# Python version

For now, Python 3 only.

# Installation

Install using `pip`

```console
$ pip install git+https://github.com/sunu/url-normalizer
```
or clone and install using `python setup.py install`

# Usage

Pass a url to the `normalize_url` function as a `str` type to normalize it. 

```pycon
In [1]: from normalizer import normalize_url

In [2]: normalize_url("hello.com")
Out[2]: 'http://hello.com/'

In [3]: normalize_url("http://example.com")
Out[3]: 'http://example.com/'

In [4]: normalize_url("http://example.com/?b=2&a=1")
Out[4]: 'http://example.com/?a=1&b=2'
```

`normalize_url` has 2 optional arguments; `extra_query_args` (defaults to `None`) and `drop_fragments`
(defaults to `True`).

You can add extra query arguments to the url by passing in a list of tuples containing
the key and value as `str`

```pycon
In [6]: normalize_url("http://example.com/?b=2&a=1", extra_query_args=[("c", "33")])
Out[6]: 'http://example.com/?a=1&b=2&c=33'
```

By default, fragments are dropped.

```pycon
In [8]: normalize_url("http://example.com/?b=2#footer")
Out[8]: 'http://example.com/?b=2'
```

Pass `drop_fragments=False` to the function to keep them

```pycon
In [9]: normalize_url("http://example.com/?b=2#footer", drop_fragments=False)
Out[9]: 'http://example.com/?b=2#footer'
```

International domain names are converted to their ASCII form

```pycon
In [11]: normalize_url("http://Яндекс.рф")
Out[11]: 'http://xn--d1acpjx3f.xn--p1ai/'
```

Unicode characters in path or query arguments are utf-8 encoded and converted to percent-encoded characters.

```pycon
In [12]: normalize_url("http://example.com/résumé/?file=résumé.pdf")
Out[12]: 'http://example.com/r%C3%A9sum%C3%A9?file=r%C3%A9sum%C3%A9.pdf'
```

If a passed url is not of `str` type or doesn't look like a valid url, `None` is returned

```pycon
In [14]: repr(normalize_url(""))
Out[14]: 'None'

In [15]: repr(normalize_url("abcde"))
Out[15]: 'None'

In [16]: repr(normalize_url(b"http://abcde.com/"))
Out[16]: 'None'

In [17]: repr(normalize_url(None))
Out[17]: 'None'

In [18]: repr(normalize_url(1234))
Out[18]: 'None'
```

# Tests

Run tests by using `python setup.py test`

# License

MIT