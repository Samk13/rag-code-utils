import ast
import os


class CodeExtractor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.definitions = set()

    def visit_Import(self, node):
        self.imports.add(ast.unparse(node).strip())

    def visit_ImportFrom(self, node):
        self.imports.add(ast.unparse(node).strip())

    def visit_FunctionDef(self, node):
        self.definitions.add(ast.unparse(node).strip())

    def visit_ClassDef(self, node):
        self.definitions.add(ast.unparse(node).strip())
        return node.name, [
            base.id for base in node.bases if isinstance(base, ast.Name)
        ]  # Collect base classes

    def visit_AsyncFunctionDef(self, node):
        self.definitions.add(ast.unparse(node).strip())


def parse_file(file_path, target):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source = file.read()
    except UnicodeDecodeError:
        print(f"Skipped file due to encoding issue: {file_path}")
        return None, None, None, []  # Return empty list for bases if decode fails

    try:
        tree = ast.parse(source)
        extractor = CodeExtractor()
        extractor.visit(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == target:
                code = ast.unparse(node)
                _, bases = extractor.visit_ClassDef(node)  # Get base classes
                return code, extractor.imports, extractor.definitions, bases
    except SyntaxError:
        pass  # Ignore files with syntax errors

    return None, None, None, []


def extract_code(base_path, target):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                code, imports, definitions, bases = parse_file(file_path, target)
                if code:
                    return code, imports, definitions, bases, file_path
    return None, None, None, None, None


def recursive_write(base_path, target, output_file, already_written, venv_path=None):
    code, imports, definitions, bases, file_path = extract_code(base_path, target)
    if code:
        if target not in already_written:
            already_written.add(target)  # Mark this target as written
            with open(
                output_file,
                "a" if os.path.exists(output_file) else "w",
                encoding="utf-8",
            ) as f:
                if file_path:
                    f.write(f"# Code for {target}\n# from {file_path}\n")
                if imports:
                    f.write("\n".join(imports) + "\n\n")
                f.write(code + "\n\n")
    else:
        if venv_path:
            code, imports, definitions, bases, file_path = extract_code(
                venv_path, target
            )
            if code and target not in already_written:
                already_written.add(target)
                with open(output_file, "a", encoding="utf-8") as f:
                    if file_path:
                        f.write(f"# Code for {target}\n# from {file_path}\n")
                    # if imports:
                    #     f.write("\n".join(imports) + "\n\n")
                    f.write(code + "\n\n")

    for base in bases:  # Process base classes recursively
        recursive_write(base_path, base, output_file, already_written, venv_path)


def mine_context(REPO_PATH, TARGET, OUTPUT_FILE, VENV_PATH):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    open(OUTPUT_FILE, "w").close()  # Clear the file initially
    already_written = set()
    recursive_write(REPO_PATH, TARGET, OUTPUT_FILE, already_written, VENV_PATH)
