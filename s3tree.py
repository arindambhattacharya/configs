import awswrangler as wr
import sys
from collections import defaultdict


def nested_dict():
    """Helper function to create a nested dictionary."""
    return defaultdict(nested_dict)


def add_to_tree(tree, path_parts, suffix):
    """Recursively adds directories to the tree and counts files with the given suffix."""
    if len(path_parts) == 1:  # We are at the file level
        # If the file matches the suffix, increment the count in the current directory
        if path_parts[0].endswith(suffix):
            tree["file_count"] = tree.get("file_count", 0) + 1
    else:  # We are at a directory level
        # Recursively add to the nested structure
        add_to_tree(tree[path_parts[0]], path_parts[1:], suffix)


def list_s3_directories_with_file_counts_tree(s3_path, suffix):
    # Initialize a nested dictionary to hold the directory structure
    directory_tree = nested_dict()

    # List all objects recursively in the given S3 path
    objects = wr.s3.list_objects(s3_path)

    # Traverse each object to build the tree structure
    for obj in objects:
        # Split the object path into its component parts
        path_parts = obj.replace(s3_path, "").split("/")
        add_to_tree(directory_tree, path_parts, suffix)

    return directory_tree


def print_tree(tree, suffix, level=0):
    """Recursive function to print the tree structure."""
    for key, value in tree.items():
        if key == "file_count":
            print("  " * level + f"{value} {suffix} files")
        else:
            print("  " * level + f"{key}/")
            print_tree(value, suffix, level + 1)


# def list_s3_directories_with_file_counts(s3_path, suffix):
#     # Ensure the s3_path ends with a forward slash
#     if not s3_path.endswith("/"):
#         s3_path += "/"
#
#     # Initialize a dictionary to hold directories and file counts
#     directory_counts = {}
#
#     # List all objects recursively in the given S3 path
#     objects = wr.s3.list_objects(s3_path)
#
#     # Traverse through each object and count files with the specified suffix
#     for obj in objects:
#         # Get directory path (without file name) and file name
#         directory = "/".join(obj.split("/")[:-1])
#
#         # Initialize the directory in dictionary if not present
#         if directory not in directory_counts:
#             directory_counts[directory] = 0
#
#         # Check if the file matches the suffix and increment count if true
#         if obj.endswith(suffix):
#             directory_counts[directory] += 1
#
#     # Display results
#     for directory, count in directory_counts.items():
#         print(
#             f"Directory: {directory[len(s3_path):]} - {count} files with suffix '{suffix}'"
#         )


if __name__ == "__main__":
    s3path = sys.argv[1] if sys.argv[1].startswith("s3://") else "s3://" + sys.argv[1]
    if len(sys.argv) == 3:
        suffix = sys.argv[2]
    else:
        suffix = ".parquet"

    # list_s3_directories_with_file_counts(s3path, suffix)
    print_tree(list_s3_directories_with_file_counts_tree(s3path, suffix), suffix)
