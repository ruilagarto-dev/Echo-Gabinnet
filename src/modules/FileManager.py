from typing import Optional, Union, List, Any
import shutil
import json
import os



class FileManager:
    """
    @class FileManager
    @brief Utility class for managing file and directory operations.

    This class provides methods for reading, writing, creating, moving,
    and deleting files and directories, including support for JSON files.
    """

    def __init__(self, base_dir: Optional[str] = None):
        """
        @brief Initializes the FileManager with a base directory.
        @param base_dir Optional base directory for relative path resolution.
        If not provided, defaults to the parent directory of the project folder.
        """

        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = os.path.abspath(base_dir) if base_dir else os.path.dirname(project_dir)


    def _resolve_path(self, path: str) -> str:
        """
        @brief Converts a relative path to an absolute path.
        @param path The path to resolve.
        @return Absolute path.
        """
        return path if os.path.isabs(path) else os.path.join(self.base_dir, path)


    def file_exists(self, fileDir: str) -> bool:
        """
        @brief Checks if a file exists.
        @param filepath Path to the file.
        @return True if the file exists, False otherwise.
        """
        return os.path.isfile(self._resolve_path(fileDir))


    def dir_exists(self, path_dir: str) -> bool:
        """
        @brief Checks if a directory exists.
        @param dirpath Path to the directory.
        @return True if the directory exists, False otherwise.
        """
        return os.path.isdir(self._resolve_path(path_dir))


    def path_exists(self, path):
        """
        @brief Checks if a path (file or directory) exists.
        @param path Path to check.
        @return True if the path exists, False otherwise.
        """
        return os.path.exists(self._resolve_path(path))
    

    def create_dir(self, dir_path: str) -> None:
        """
        @brief Creates a directory, creating any parent directories if necessary.
        @param dirpath Path to the directory.
        If a file exists at the path, it is renamed with a .bak extension.
        """
        resolved_path = self._resolve_path(dir_path)

        if os.path.exists(resolved_path) and not os.path.isdir(resolved_path):
            backup_path = resolved_path + ".bak"
            shutil.move(resolved_path, backup_path)

        os.makedirs(resolved_path, exist_ok=True)

    def delete_dir(self, dir_path: str) -> None:
        """
        @brief Deletes a directory and its contents.
        @param dirpath Path to the directory.
        @throws FileNotFoundError if the directory does not exist.
        """
        resolved_path = self._resolve_path(dir_path)

        if os.path.exists(resolved_path):
            shutil.rmtree(resolved_path)
        else:
            raise FileNotFoundError(f"Directory '{resolved_path}' does not exist.")
        

    def create_file(self, file_path: str, content: Optional[str] = None) -> None:
        """
        @brief Creates a new file with optional initial content.
        @param filepath Path to the file.
        @param content Optional string content to write into the file.
        """
        resolved_path = self._resolve_path(file_path)

        if not self.file_exists(resolved_path):
            os.makedirs(os.path.dirname(resolved_path), exist_ok=True)
            with open(resolved_path, 'w', encoding='utf-8') as file:
                if content:
                    file.write(content)


    def delete_file(self, file_path: str) -> None:
        """
        @brief Deletes a file.
        @param filepath Path to the file.
        @throws FileNotFoundError if the file does not exist.
        """
        resolved_path = self._resolve_path(file_path)

        if self.file_exists(resolved_path):
            os.remove(resolved_path)
        else:
            raise FileNotFoundError(f"File '{resolved_path}' does not exist.")


    def copy_file(self, src: str, dest: str) -> None:
        """
        @brief Copies a file to a new destination.
        @param src Source file path.
        @param dest Destination file path.
        @throws FileNotFoundError if the source file does not exist.
        """

        src_path = self._resolve_path(src)
        dest_path = self._resolve_path(dest)

        if self.fileExists(src_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
        else:
            raise FileNotFoundError(f"Source file '{src_path}' does not exist.")
        


    def move_file(self, src: str, dest: str) -> None:
        """
        @brief Moves a file to a new destination.
        @param src Source file path.
        @param dest Destination file path.
        @throws FileNotFoundError if the source file does not exist.
        """

        src_path = self._resolve_path(src)
        dest_path = self._resolve_path(dest)

        if self.file_exists(src_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok = True)
            shutil.move(src_path, dest_path)
        else:
            raise FileNotFoundError(f"Source file '{src_path}' does not exist.")


    def __read_json_file(self, filepath: str) -> Optional[Union[dict, list]]:
        """
        @brief Reads a JSON file and returns its content.
        @param filepath Path to the JSON file.
        @return Parsed JSON content, or None on failure.
        """

        resolved_path = self._resolve_path(filepath)

        try:
            with open(resolved_path, 'r', encoding = 'utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None


    def read_file(self, filepath: str) -> Optional[Union[str, dict, list]]:
        """
        @brief Reads a file's content (text or JSON).
        @param filepath Path to the file.
        @return File content, or None if file doesn't exist.
        """
        resolved_path = self._resolve_path(filepath)
        
        if not self.file_exists(resolved_path):
            return None
        
        ext = os.path.splitext(resolved_path)[1].lower()

        if ext == '.json':
            return self.__read_json_file(resolved_path)
        else:
            try:
                with open(resolved_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except IOError as e:
                raise IOError(f"Error reading file '{resolved_path}': {e}")
    
    
    def __write_json_file(self, filepath: str, content: Union[dict, list]) -> None:
        """
        @brief Writes or updates content in a JSON file.
        If the file already exists, updates entries based on matching dictionary keys.
        @param filepath Path to the JSON file.
        @param content Dictionary or list of dictionaries to write.
        """
        resolved_path = self._resolve_path(filepath)
        existing = self.__read_json_file(resolved_path) or []


        if not isinstance(existing, list):
            existing = [existing]

        if not isinstance(content, list):
            content = [content]

        for new_item in content:
            if not isinstance(new_item, dict):
                existing.append(new_item)
                continue

            keys_new = set(new_item.keys())
            updated = False

            for i, existing_item in enumerate(existing):
                if isinstance(existing_item, dict) and set(existing_item.keys()) == keys_new:
                    existing[i] = new_item
                    updated = True
                    break
            if not updated:
                existing.append(new_item)
        
        with open(resolved_path, 'w', encoding='utf-8') as file:
            json.dump(existing, file, ensure_ascii=False, indent=4)
       


    def write_file(self, filepath: str, content: Union[str, dict, list], mode: str = 'a') -> None:
        """
        @brief Writes content to a file.
        Supports both text and JSON content. JSON files are merged intelligently.
        @param filepath Path to the file.
        @param content Content to write (str, dict or list).
        @param mode File write mode, default is append ('a').
        @throws TypeError if non-string content is provided for non-JSON files.
        @throws IOError if the write operation fails.
        """
        resolved_path = self._resolve_path(filepath)
        
        if not self.file_exists(resolved_path):
            initial_content = '' if mode == 'a' else content if isinstance(content, str) else ''
            self.create_file(resolved_path, initial_content)

            if isinstance(content, (dict, list)):
                self.__write_json_file(resolved_path, content)
            elif isinstance(content, str) and mode == 'w':
                with open(resolved_path, 'w', encoding='utf-8') as file:
                    file.write(content)
            return

        ext = os.path.splitext(resolved_path)[1].lower()
        if ext == '.json':
            self.__write_json_file(resolved_path, content)
        else:
            try:
                with open(resolved_path, mode, encoding='utf-8') as file:
                    if isinstance(content, str):
                        file.write(content)
                    else:
                        raise TypeError("Content must be a string when writing non-JSON files.")
            except IOError as e:
                raise IOError(f"Error writing file '{resolved_path}': {e}")
       
