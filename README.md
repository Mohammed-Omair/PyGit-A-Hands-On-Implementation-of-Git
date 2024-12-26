# PyGit: A Hands-On Implementation of Git

A Python-based project that replicates core Git functionalities such as initializing repositories, writing trees, committing changes, and cloning remote repositories. This hands-on implementation provides an in-depth understanding of Git's internal mechanics and data structures.

## Features

- **Repository Initialization (`init`)**: Create a `.git` directory with essential subdirectories and metadata.
- **Object Management (`hash-object`)**: Hash and store blob objects in a zlib-compressed format.
- **Tree Management (`write-tree`, `ls-tree`)**: Serialize and store directory structures as tree objects.
- **Commit Creation (`commit-tree`)**: Generate commit objects with author, committer, and parent details.
- **File Inspection (`cat-file`)**: Inspect and decompress stored Git objects.
- **Repository Cloning (`clone`)**: Clone a remote repository using Git's Smart HTTP protocol and render the contents.

## Installation

Ensure you have Python 3.7+ installed. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Mohammed-Omair/PyGit-A-Hands-On-Implementation-of-Git.git
cd PyGit-A-Hands-On-Implementation-of-Git/app
pip install -r requirements.txt
```
## Usage

### Initialize a Repository

```bash
python3 main.py init
```

### Hash and Store a File

```bash
python3 main.py hash-object -w <file>
```

### Display the Contents of an Object

```bash
python3 pygit.py cat-file <SHA-1 hash>
```

### Write a Tree

```bash
python3 main.py write-tree
```

### List Tree Contents

```bash
python3 pygit.py ls-tree <tree-sha>
```

### Create a Commit

```bash
python3 main.py commit-tree <tree-sha> -m "Commit message"
```

### Clone a Repository

```bash
python3 main.py clone <repo_url> <target_dir>
```

## Key Takeaways

- **In-Depth Understanding of Git Internals**:
  - Explored the architecture and functionality of Git, including objects (blobs, trees, and commits), hashing mechanisms, and storage structure.
  - Learned how Git manages references, packfiles, and protocols for remote communication.
- **Practical Experience with Low-Level Concepts**:
  - Implemented the SHA-1 hashing algorithm and understood how it uniquely identifies Git objects.
  - Used zlib compression to efficiently store and retrieve objects, mimicking Git's storage mechanisms.
  - Simulated Git’s file modes (`100644`, `100755`, `40000`, etc.) and understood their significance.
- **HTTP and Git Protocols**:
  - Gained exposure to Git’s Smart HTTP protocol and its role in remote interactions.
  - Implemented packet-based communication to fetch refs and objects using custom HTTP requests.
- **Recursive Tree Rendering and Object Serialization**:
  - Built a recursive system to render Git trees and manage nested directories.
  - Serialized tree objects and understood their role in representing file hierarchy.
- **Practical Python Skills**:
  - Strengthened understanding of Python modules like `os`, `sys`, `zlib`, `hashlib`, and `urllib`.
  - Managed errors gracefully using exception handling and designed reusable functions for modularity.
- **System Design and Optimization**:
  - Designed a mini Git system from scratch, improving understanding of how version control systems optimize storage and performance.
  - Balanced simplicity and scalability in implementation, preparing for potential future extensions.
- **Time and Space Efficiency**:
  - Applied delta encoding and object reuse techniques to mimic Git's efficiency when handling similar or duplicate files.

## Acknowledgments

- [Pro Git by Scott Chacon](https://git-scm.com/book/en/v2) for foundational knowledge.
- The [Git Documentation](https://git-scm.com/docs) for detailed insights.
- The [CodeCrafters Git Challenge](https://app.codecrafters.io/catalog) for inspiring this project.
