import os

project_name = "PDF-Ingestion-Parsing"

# Define the project structure
file_tree = {
    project_name: {
        "app": {
            "__init__.py": "",
            "main.py": "",
            "core": {
                "__init__.py": "",
                "models.py": "",
                "parser.py": "",
                "utils.py": ""
            },
            "services": {
                "__init__.py": "",
                "file_storage.py": ""
            }
        },
        "frontend": {
            "app.py": ""
        },
        "scripts": {
            "export_training_corpus.py": ""
        },
        ".env": "",
        ".gitignore": "",
        "README.md": "",
        "requirements.txt": ""
    }
}

def create_directory_structure(base_path, tree):
    """Recursively creates the directory and file structure."""
    for name, content in tree.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")
            create_directory_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)
            print(f"Created file: {path}")

# Create the project structure
create_directory_structure(os.getcwd(), file_tree)

# Define initial content for key files
requirements_content = """
fastapi
uvicorn
python-multipart
pymupdf
tesseract
opencv-python
scikit-learn # For langdetect
numpy
pandas
pydantic
streamlit
langdetect
"""

gitignore_content = """
# Python
__pycache__/
*.pyc
.env
.venv/
# IDEs
.idea/
.vscode/
"""

readme_content = """
# PDF-Ingestion-Parsing

This project is a modular pipeline for ingesting, parsing, and chunking PDFs into a training-ready JSONL format.
"""

# Write content to files
with open(os.path.join(project_name, "requirements.txt"), "w") as f:
    f.write(requirements_content.strip())

with open(os.path.join(project_name, ".gitignore"), "w") as f:
    f.write(gitignore_content.strip())

with open(os.path.join(project_name, "README.md"), "w") as f:
    f.write(readme_content.strip())

print("\nProject structure created successfully!")
print("Next steps:")
print(f"1. Navigate into the directory: cd {project_name}")
print("2. Create a virtual environment: python -m venv .venv")
print("3. Activate it: source .venv/bin/activate (or .venv\\Scripts\\activate on Windows)")
print("4. Install dependencies: pip install -r requirements.txt")
print("5. Start coding in the new files!")