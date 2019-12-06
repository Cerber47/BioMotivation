
def save_release_to_disk(filename, data):
    path = "input/" + filename

    with open(path, 'w') as f:
        f.write(data)
