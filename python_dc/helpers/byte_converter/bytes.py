def convert_bytes(size):
    for formats in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, formats)
        size /= 1024.0
    return size