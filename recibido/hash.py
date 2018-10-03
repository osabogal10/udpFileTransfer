import hashlib

hasher = hashlib.md5()
with open('newfile1.jpg', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
print(hasher.hexdigest())