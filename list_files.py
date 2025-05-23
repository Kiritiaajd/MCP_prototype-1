import os

def list_files(start_path, indent=0):
    for item in os.listdir(start_path):
        full_path = os.path.join(start_path, item)
        print('    ' * indent + '|-- ' + item)
        if os.path.isdir(full_path):
            list_files(full_path, indent + 1)

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    print("Project structure for:", project_root)
    list_files(project_root)
