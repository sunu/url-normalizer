from urllib.parse import _coerce_args, unquote_to_bytes


def _parse_qsl(qs, keep_blank_values=False, strict_parsing=False):
    """Modify `urllib.parse.parse_qsl` to handle percent-encoded characters
    properly. `parse_qsl` replaces percent-encoded characters with
    replacement character (U+FFFD) (if errors = "replace") or drops them (if 
    errors = "ignore") (See https://docs.python.org/3/howto/unicode.html#the-string-type).
    Instead we want to keep the raw bytes. And later we can percent-encode them
    directly when we need to.

    Code from https://github.com/python/cpython/blob/73c4708630f99b94c35476529748629fff1fc63e/Lib/urllib/parse.py#L658
    with `unquote` replaced with `unquote_to_bytes`
    """
    qs, _coerce_result = _coerce_args(qs)
    pairs = [s2 for s1 in qs.split('&') for s2 in s1.split(';')]
    r = []
    for name_value in pairs:
        if not name_value and not strict_parsing:
            continue
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            if strict_parsing:
                raise ValueError("bad query field: %r" % (name_value,))
            # Handle case of a control-name with no equal sign
            if keep_blank_values:
                nv.append('')
            else:
                continue
        if len(nv[1]) or keep_blank_values:
            name = nv[0].replace('+', ' ')
            name = unquote_to_bytes(name)
            name = _coerce_result(name)
            value = nv[1].replace('+', ' ')
            value = unquote_to_bytes(value)
            value = _coerce_result(value)
            r.append((name, value))
    return r
