import sys
import os
import zlib
import hashlib

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
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
    elif command == "hash-object":
        if len(sys.argv) != 4:
            print("The command is missing arguments. usage: hash-object -w <file>", file=sys.stderr)
            exit()
        file_name= sys.argv[-1]
        with open(file_name, "rb") as file:
                file_content = file.read()
        header = f"blob {len(file_content)}\x00"
        store = header.encode("ascii") + file_content
        sha = hashlib.sha1(store).hexdigest()
        print(sha)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
