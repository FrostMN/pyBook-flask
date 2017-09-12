def ISBN(raw):
    if len(raw) > 0:
        if '-' in raw:
            stripped = raw.replace("-", "")
        else:
            stripped = raw

        stripped = stripped.rjust(10, '0')

        if len(stripped) == 10 or len(stripped) == 13:
            if stripped.isdigit():
                return stripped
        return False
    return False
