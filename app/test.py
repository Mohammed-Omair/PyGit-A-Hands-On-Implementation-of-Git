tree_sha = "9b1f92a8fbd45a8d6faade15c03419e29d0d3c33"
parent_sha = "7d3b491b837adc8cd0d3d9f2c601c9906bbd80e3"
author = "John Doe <johndoe@example.com>"
timestamp = "1690001234"
timezone = "-0500"
message = "Initial commit"

commit_content = (
    f"tree {tree_sha}\n"
    f"parent {parent_sha}\n"
    f"author {author} {timestamp} {timezone}\n"
    f"committer {author} {timestamp} {timezone}\n"
    f"\n"
    f"{message}\n"
)

print(commit_content)
print(type(commit_content))