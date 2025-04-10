import os

def print_directory_tree(start_path, indent=""):
    for item in sorted(os.listdir(start_path)):
        path = os.path.join(start_path, item)
        if os.path.isdir(path):
            print(indent + "📁 " + item)
            print_directory_tree(path, indent + "    ")
        else:
            print(indent + "📄 " + item)

# Replace '.' with the root folder of your project if needed
print_directory_tree(".")
