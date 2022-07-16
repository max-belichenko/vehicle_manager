def get_file_extension(filename: str) -> str:
    """ Возвращает расширение файла. """
    splitted_filename = filename.rsplit('.', maxsplit=1)

    if len(splitted_filename) == 1:
        extension = ''
    else:
        extension = splitted_filename[1]

    return extension
