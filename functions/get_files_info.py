import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))

        if (
            os.path.commonpath([working_directory_abs, target_dir])
            != working_directory_abs
        ):
            return f'Error: Cannot list "{directory}", as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        target_dir_contents = os.listdir(target_dir)
        contents_str = ""
        for item in target_dir_contents:
            item_abs = os.path.join(target_dir, item)
            contents_str += f"- {item_abs}: file_size={os.path.getsize(item_abs)}, is_dir={os.path.isdir(item_abs)}\n"
        return contents_str

    except Exception as e:
        return f"Error: listing files: {e}"
