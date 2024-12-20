import sys
import os
import zlib
import hashlib

def init():
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Initialized git directory")

def catfile():
    blob_sha = sys.argv[-1]
    dir = blob_sha[0:2]
    file = blob_sha[2:]
    file = file.strip("\r")
    file_path = f".git/objects/{dir}/{file}"
    with open(file_path, 'rb') as f_in:
        compressed_data = f_in.read()
    decompressed_data = zlib.decompress(compressed_data)
    size = decompressed_data.split(b'\x00', 1)[0]
    data = decompressed_data.split(b'\x00', 1)[1]
    data = data.decode("utf-8").strip("\n")
    print(data, end="")

def hashobject():
    if len(sys.argv) != 4:
        print("The command is missing arguments. usage: hash-object -w <file>", file=sys.stderr)
        exit()
    file_name= sys.argv[-1]
    with open(file_name, "rb") as file:
            file_content = file.read()
    header = f"blob {len(file_content)}\x00"
    store = header.encode("ascii") + file_content
    compressed_data = zlib.compress(store)
    sha = hashlib.sha1(store).hexdigest()
    dir = ".git/objects/" + sha[0:2]
    os.mkdir(dir)
    file = dir + "/" +sha[2:]
    with open(file, "wb") as file:
        file.write(compressed_data)
    print(sha)

def lstree():
    tree_sha = sys.argv[-1]
    dir = tree_sha[0:2]
    file = tree_sha[2:]
    file = file.strip("\r")
    file_path = f".git/objects/{dir}/{file}"
    with open(file_path, 'rb') as f_in:
        compressed_data = f_in.read()
    decompressed_data = zlib.decompress(compressed_data)
    size = decompressed_data.split(b'\x00', 1)[0]
    data = decompressed_data.split(b'\x00', 1)[1]
    position = 0
    i = 0
    mode = []
    name = []
    sha_hash = []
    while position < len(data):
        mode_end = data.find(b' ', position)
        mode.append(data[position:mode_end].decode("utf-8"))
        position = mode_end

        name_end = data.find(b'\x00', position)
        name.append(data[position+1:name_end].decode("utf-8"))
        position = name_end

        sha_hash.append(data[position+1:position+21].hex())
        position = position + 21

        i+=1
    names = '\n'.join(name)
    print(names)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.

    command = sys.argv[1]
    if command == "init":
        init()
    elif command == "cat-file":
        catfile()
    elif command == "hash-object":
        hashobject()
    elif command == "ls-tree":
        lstree()
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
