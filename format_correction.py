# Correction Function
def correction_formatter(offset, kalimat, replacement):
    correction = {
        'offset': offset,
        'deleteCount': kalimat,
        'replacement': replacement
    }

    return correction