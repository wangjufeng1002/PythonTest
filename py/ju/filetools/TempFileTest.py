import tempfile

directory = tempfile.TemporaryDirectory()
print(directory.name)

file = tempfile.TemporaryFile(dir=directory.name)
print(file.name)


