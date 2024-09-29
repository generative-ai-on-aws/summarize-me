def save_to_file(content, file_path):
    """
    Save content to a file.

    This function opens the specified file in write mode and writes the provided content to it.
    If the file doesn't exist, it will be created. If it does exist, it will be overwritten.

    Args:
        content (str): The content to be saved to the file.
        file_path (str): The path to the output file.

    Raises:
        IOError: If there's an error writing to the file (e.g., permission denied, disk full).
    """
    with open(file_path, 'w') as f:
        f.write(content)