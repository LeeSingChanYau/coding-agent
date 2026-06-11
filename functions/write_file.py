import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if valid_target_file == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            f'Error: Cannot write to "{file_path}" as it is a directory'
        
        target_dir = os.path.dirname(target_file)
        os.makedirs(target_dir, exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing file {file_path}: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write file in a specified path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into file."
            )
        },
    ),
)