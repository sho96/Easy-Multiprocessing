import subprocess
import sys
import pickle
from threading import Thread, Lock
import inspect
import ast
import tempfile
import os

mutex = Lock()
processResults = {}

python_executable = sys.executable

importStatements = ""

def importLibraries(underbarUnderbarfileUnberbarUnderbar):
    global importStatements
    with open(underbarUnderbarfileUnberbarUnderbar, "r") as f:
        imports = get_import_statements(f.read())
    importStatements = "\n".join(imports)
def get_import_statements(script_text):
    try:
        tree = ast.parse(script_text)
        import_statements = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "mp":
                        continue
                    import_statements.append(f"import {alias.name}")
                    if alias.asname:
                        import_statements[-1] += f" as {alias.asname}"
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""
                for alias in node.names:
                    if alias.name == "mp":
                        continue
                    statement = f"from {module} import {alias.name}"
                    if alias.asname:
                        statement += f" as {alias.asname}"
                    import_statements.append(statement)

        return import_statements
    except Exception as e:
        print(f"Error parsing the script: {e}")
        return []

def runProcessThread(processID, imports, function, args):
    global processResults
    source = inspect.getsource(function)
    pickled_args = pickle.dumps(args)
    
    # Create a temporary file to store the script
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py') as temp_file:
        code_to_run = f"""\
import pickle

{imports}

{source}

args = pickle.loads({pickled_args})
output = {function.__name__}({"" if len(inspect.signature(function).parameters) == 1 else ""}args)
print(pickle.dumps(output))
"""
        temp_file.write(code_to_run)
        temp_file_name = temp_file.name
    
    try:
        output_str = subprocess.check_output([python_executable, temp_file_name], universal_newlines=True)
        output = pickle.loads(eval(output_str))
        
        with mutex:
            processResults[processID] = output
    finally:
        os.remove(temp_file_name)

def process(function, args, imports=""):
    global importStatements
    global processResults

    if importStatements != "":
        imports = importStatements

    threads = []
    for i, arg in enumerate(args):
        thread = Thread(target=runProcessThread, args=(i, imports, function, arg))
        thread.start()
    while len(processResults) < len(args):
        pass
    results = []
    for i in range(len(args)):
        results.append(processResults[i])
    processResults = {}
    return results