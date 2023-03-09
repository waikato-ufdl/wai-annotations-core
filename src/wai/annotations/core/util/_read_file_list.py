from typing import Iterator


def read_file_list(filename: str) -> Iterator[str]:
    """
    Reads a list of file-names from a file.

    :param filename:
                The name of the file containing the file-names.
    :return:
                An iterator over the file-names.
    """
    with open(filename, 'r') as file:
        for line in file.readlines():
            # Strip any leading/trailing whitespace
            line = line.strip()

            # Remove comments and empty lines
            if line.startswith("#") or line == "":
                continue

            yield line
