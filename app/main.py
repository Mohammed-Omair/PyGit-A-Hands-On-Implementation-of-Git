import sys
import os
import zlib

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
        print(data.decode("utf-8"))

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
