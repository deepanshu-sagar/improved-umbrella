import os
import subprocess
import ast
from multiprocessing import Pool

BIG_FILE_PATH = 'data/data.py'
NEW_DIR = 'new_data'
CMD = ["/usr/local/bin/bito", "-p", "data/prompt"]

# Check if the input file exists
if not os.path.isfile(BIG_FILE_PATH):
    raise FileNotFoundError(f"No such file: '{BIG_FILE_PATH}'")
else:
    print(f"File found: {BIG_FILE_PATH}")

# Create the directory where the new files will be stored
os.makedirs(NEW_DIR, exist_ok=True)

# Parse the big Python file
with open(BIG_FILE_PATH, 'r', encoding='utf-8') as big_file:
    big_file_content = big_file.read()

module = ast.parse(big_file_content)

# Maintain an ordered list of new file paths
new_file_paths = []

def run_cmd_on_file(new_file_path):
    # Run the command on the new Python file
    cmd_with_file = CMD + ["-f", new_file_path]
    print(f"Running command on file: {new_file_path}")
    result = subprocess.run(cmd_with_file, capture_output=True)
    return new_file_path, result.stdout.decode('utf-8')

# Separate classes and functions, and write them to individual files
for node in module.body:
    if isinstance(node, ast.ClassDef):
        class_name = node.name
        for subnode in node.body:
            if isinstance(subnode, ast.FunctionDef):
                function_name = subnode.name
                function_code = ast.unparse(subnode)

                # Create the new file with function name in the new directory
                new_file_path = os.path.join(NEW_DIR, f'{class_name}_{function_name}.py')
                new_file_paths.append(new_file_path)

                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(function_code)

    elif isinstance(node, ast.FunctionDef):
        function_name = node.name
        function_code = ast.unparse(node)

        # Create the new file with function name in the new directory
        new_file_path = os.path.join(NEW_DIR, f'{function_name}.py')
        new_file_paths.append(new_file_path)

        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(function_code)

print("Finished creating individual files.")

# Create a multiprocessing pool and run the command on all new files in parallel
with Pool(processes=8) as p:
    print("Starting parallel execution...")
    results = p.map(run_cmd_on_file, new_file_paths)

# results is a list of tuples. Each tuple contains the new_file_path and the corresponding output of CMD
# You can use these results to combine the files again.
outputs = {new_file_path: output for new_file_path, output in results}

print("Finished parallel execution.")

# Now let's combine all the small Python files into a new Python file
combined_file_path = os.path.join(NEW_DIR, 'combined.py')
with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
    # Iterate over each file in the new directory
    for new_file_path in new_file_paths:
        if os.path.isfile(new_file_path):
            with open(new_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            combined_file.write(outputs[new_file_path] + '\n\n')

print("Finished combining files.")
