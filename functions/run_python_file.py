import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))

        if (
            os.path.commonpath([working_directory_abs, file_path_abs])
            != working_directory_abs
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]
        if args != None:
            command.extend(args)

        completed_process = subprocess.run(
            args=command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30.0,
        )

        output = ""
        if completed_process.returncode != 0:
            output += "Process exited with code X"
        if (completed_process.stdout) == "" and (completed_process.stderr == ""):
            output += "No output produced"
        else:
            if completed_process.stdout != "":
                output += f"STDOUT: {completed_process.stdout}"
            if completed_process.stderr != "":
                output += f"STDERR: {completed_process.stderr}"
        return output

    except Exception as e:
        f"Error: executing Python file: {e}"
