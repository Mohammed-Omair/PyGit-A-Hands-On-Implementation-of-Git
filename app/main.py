import sys
import os
import zlib
import hashlib
import time
from datetime import datetime, timezone

# Store the absolute path to the .git directory
GIT_DIR = os.path.join(os.getcwd(), ".git")
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

def hashobject(command_list):
    if len(command_list) < 3:
        print("The command is missing arguments. usage: hash-object <optional flag> <file>", file=sys.stderr)
        exit()
    file_name= command_list[-1]
    with open(file_name, "rb") as file:
            file_content = file.read()
    header = f"blob {len(file_content)}\x00"
    store = header.encode("ascii") + file_content
    compressed_data = zlib.compress(store)
    sha = hashlib.sha1(store).hexdigest()
    if command_list[-2] == "-w":
        dir = GIT_DIR + "/objects/" + sha[0:2]
        try:
            os.mkdir(dir)  # Create the directory
        except FileExistsError:
            pass  # Ignore error if directory already exists
        file = dir + "/" +sha[2:]
        with open(file, "wb") as file:
            file.write(compressed_data)
        return sha
    else:
        return sha

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

def wrtree():
    cwd = os.getcwd()  # Current working directory
    tree_content = bytes()  # To store the serialized tree data

    # Serialize files in the current directory
    entries = sorted(os.scandir(cwd), key=lambda entry: entry.name)
    for entry in entries:
        if entry.name == ".git":
            continue
        mode = get_mode(entry.path)
        if entry.is_file():
            # Compute the blob hash for the file
            file_sha = hashobject(["hash-object", "-w", entry.name])
            # Add the file's mode, name, and hash to the tree
            tree_content += f"{mode} {entry.name}\0".encode("utf-8") + bytes.fromhex(file_sha)
        elif entry.is_dir():
            os.chdir(entry.name)  # Enter the subdirectory
            sub_tree_sha = wrtree()  # Recursively generate the tree object for the subdirectory
            os.chdir("..")  # Return to the parent directory
            # Add the directory's mode, name, and tree hash to the tree
            tree_content += f"{mode} {entry.name}\0".encode("utf-8") + bytes.fromhex(sub_tree_sha)

    # Create the tree object header
    header = f"tree {len(tree_content)}\0".encode("utf-8")
    tree_object = header + tree_content

    # Compute the tree's SHA-1 hash
    tree_sha = hashlib.sha1(tree_object).hexdigest()

    # Store the tree object in the Git object database
    compressed_tree = zlib.compress(tree_object)
    dir_path = f".git/objects/{tree_sha[:2]}"
    file_path = f"{dir_path}/{tree_sha[2:]}"
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(compressed_tree)

    return tree_sha
        

def get_mode(path):
    """Determine the mode for a given path."""
    if os.path.isdir(path):
        return "40000"  # Directory
    elif os.path.islink(path):
        return "120000"  # Symbolic link
    elif os.path.isfile(path):
        if os.access(path, os.X_OK):
            return "100755"  # Executable file
        else:
            return "100644"  # Regular file
    else:
        raise ValueError(f"Unknown file type for path: {path}")

def cmtree():
    msg = sys.argv[-1]
    
    tree_sha = sys.argv[2]
    name = "Mohammed Omair Mohiuddin"
    email = "mohammedomair07@gmail.com"
    epoch_time = int(time.time())
    timezone_offset = get_timezone_offset()
    if "-p" in sys.argv:
        parent_commit_sha = sys.argv[-3]
        commit_content = (
            f"tree {tree_sha}\n"
            f"parent {parent_commit_sha}\n"  # Omit if there's no parent commit
            f"author {name} {epoch_time} {timezone_offset}\n"
            f"committer {name} {epoch_time} {timezone_offset}\n"
            f"\n"
            f"{msg}\n"
        )
    else:
        commit_content = (
            f"tree {tree_sha}\n"
            f"author {name} {epoch_time} {timezone_offset}\n"
            f"committer {name} {epoch_time} {timezone_offset}\n"
            f"\n"
            f"{msg}\n"
        )
    commit_content_bytes = commit_content.encode("utf-8")
    header = f"commit {len(commit_content_bytes)}\0".encode("utf-8")
    full_content = header + commit_content_bytes

    #Compute the SHA-1 hash
    sha1_hash = hashlib.sha1(full_content).hexdigest()

    #Compress the content
    compressed_content = zlib.compress(full_content)

    #Save the compressed content in .git/objects
    dir_path = f".git/objects/{sha1_hash[:2]}"
    file_path = f"{dir_path}/{sha1_hash[2:]}"
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(compressed_content)

    return sha1_hash
    
def get_timezone_offset():
    # Get the current time with UTC offset
    now = datetime.now()
    if now.utcoffset() is None:
        # If no timezone info, assume local timezone
        now = datetime.now(timezone.utc).astimezone()
    
    # Get the offset in seconds from UTC
    offset_seconds = now.utcoffset().total_seconds()
    
    # Calculate hours and minutes
    hours, remainder = divmod(abs(offset_seconds), 3600)
    minutes = remainder // 60
    
    # Determine the sign of the offset
    sign = '+' if offset_seconds >= 0 else '-'
    
    # Format as ±HHMM
    return f"{sign}{int(hours):02d}{int(minutes):02d}"


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.

    command = sys.argv[1]
    if command == "init":
        init()
    elif command == "cat-file":
        catfile()
    elif command == "hash-object":
        command_list = sys.argv
        result = hashobject(command_list)
        print(result)
    elif command == "ls-tree":
        lstree()
    elif command == "write-tree":
        result = wrtree()
        print(result)
    elif command == "commit-tree":
        result = cmtree()
        print(result)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
