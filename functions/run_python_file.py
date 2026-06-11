import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if valid_target_file == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith("py") == False:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output = ""
        if result.returncode != 0:
            output += "Process exited with code X\n"
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            output += "No output produced"
        else:
            output += f"STDOUT:{result.stdout}\n"
            output += f"STDERR:{result.stderr}\n"

        return output
        
    
    except Exception as e:
        return f"Error executing file {file_path}: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file in a specified path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to run the the python file.",
                items=types.Schema(type=types.Type.STRING),
            )
        },
    ),
)
