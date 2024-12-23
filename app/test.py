# import os

# def get_mode(path):
#     """Determine the mode for a given path."""
#     if os.path.isdir(path):
#         return "40000"  # Directory
#     elif os.path.islink(path):
#         return "120000"  # Symbolic link
#     elif os.path.isfile(path):
#         if os.access(path, os.X_OK):
#             return "100755"  # Executable file
#         else:
#             return "100644"  # Regular file
#     else:
#         raise ValueError(f"Unknown file type for path: {path}")

# for entry in os.scandir(os.getcwd()):
#     print(entry.path)



# #------------------------
# def wrtree():
#     cwd = os.getcwd()  # Current working directory
#     tree_content = bytes()  # To store the serialized tree data

#     # Serialize files in the current directory
#     for entry in os.scandir(cwd):
#         mode = get_mode(entry.path)
#         if entry.is_file():
#             # Compute the blob hash for the file
#             file_sha = hashobject(["hash-object", "-w", entry.name])
#             # Add the file's mode, name, and hash to the tree
#             tree_content += f"{mode} {entry.name}\0".encode("utf-8") + bytes.fromhex(file_sha)
#         elif entry.is_dir():
#             os.chdir(entry.name)  # Enter the subdirectory
#             sub_tree_sha = wrtree()  # Recursively generate the tree object for the subdirectory
#             os.chdir("..")  # Return to the parent directory
#             # Add the directory's mode, name, and tree hash to the tree
#             tree_content += f"{mode} {entry.name}\0".encode("utf-8") + bytes.fromhex(sub_tree_sha)

#     # Create the tree object header
#     header = f"tree {len(tree_content)}\0".encode("utf-8")
#     tree_object = header + tree_content

#     # Compute the tree's SHA-1 hash
#     tree_sha = hashlib.sha1(tree_object).hexdigest()

#     # Store the tree object in the Git object database
#     compressed_tree = zlib.compress(tree_object)
#     dir_path = f".git/objects/{tree_sha[:2]}"
#     file_path = f"{dir_path}/{tree_sha[2:]}"
#     os.makedirs(dir_path, exist_ok=True)
#     with open(file_path, "wb") as f:
#         f.write(compressed_tree)

#     return tree_sha
# #--------------------------------

# #----------------------------
# for entry in os.scandir(cwd):
#     mode = get_mode(entry.path)
#     if entry.is_file():
#         # Compute the blob hash for the file
#         file_sha = hashobject(["hash-object", "-w", entry.name])
#         # Add the file's mode, name, and hash to the tree
#         tree_content += f"{mode} {entry.name}\0".encode("utf-8") + bytes.fromhex(file_sha)
#     elif entry.is_dir():
#         os.chdir(entry.name)  # Enter the subdirectory
#         sub_tree_sha = wrtree()  # Recursively generate the tree object for the subdirectory
#         os.chdir("..")  # Return to the parent directory
#         # Add the directory's mode, name, and tree hash to the tree
#         tree_content += f"{mode} {entry.name}\0".encode("utf-8") + bytes.fromhex(sub_tree_sha)

# #------------------------------

import os 
print(os.listdir(os.getcwd()))