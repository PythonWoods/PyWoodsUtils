import shutil
from typing import Dict, List, Optional, Union
import os


class FileManager:
    """
    This class provides a comprehensive suite of methods for managing files and directories within a specified root directory.

    Key functionalities include:

    * **Root Path Management:**
        - Sets and retrieves the root path used as the base directory for all file operations.
        - Ensures all paths provided by the user are absolute by:
            - Expanding relative paths (e.g., "subfolder") to their full paths relative to the root path.
            - Handling tilde (~) notation, which typically refers to the user's home directory.
    * **File and Directory Operations:**
        - `create_folder(path)`: Creates a new directory at the specified path relative to the root path.
        - `checkPathPermissions(path)`: Verifies and potentially corrects permissions for the specified path (file or directory) relative to the root path.
        - `create_file(file_path, sub_folder=None)`: Creates empty files at the specified paths, optionally within a subfolder relative to the root path.
    * **File Information Retrieval:**
        - `get_file_list(directory: str, extension=None, recursive=False, include_dir=False) -> list:` Retrieves a list of files within a directory (relative to the root path), optionally filtered by extension, searched recursively within subdirectories, or including directory names in the results.
        - `get_files_by_extension(self, directory: str, extension: str = None) -> list:` Retrieves a list of files within a directory, optionally filtered by a specific extension (e.g., 'jpg', 'txt').
        - `get_files_recursively(self, directory: str, recursive: bool = False) -> list:` Retrieves a list of files within a directory, searching recursively within subdirectories if specified.
        - `get_file_paths_with_dir(self, directory: str, include_dir: bool = False) -> list:` Retrieves a list of files within a directory, optionally including directory names in the paths.
        - `get_permission_string(self, permissions: int) -> str:` Converts numeric permissions to a human-readable string.

    By utilizing this class, you can manage file and directory operations within a designated root directory structure in a robust manner.

    **Usage Example:**

    ```python
    file_manager = FileManager("/path/to/your/root/directory")

    # Create a new folder
    file_manager.create_folder("/subdirectory")

    # Check permissions for a file
    file_manager.checkPathPermissions("/important_file.txt")

    # Create an empty file
    file_manager.create_file("/new_file.txt")

    # Retrieve a list of files
    all_files = file_manager.get_file_list("/documents")

    # Get only JPG files
    jpg_files = file_manager.get_files_by_extension("/images", extension=".jpg")

    # Get all files recursively (including subdirectories)
    all_files_recursive = file_manager.get_files_recursively("/documents", recursive=True)

    # Get file paths with directory names
    file_paths = file_manager.get_file_paths_with_dir("/documents", include_dir=True)
    """

    def __init__(self, root_path=None):
        """
        Initializes the FileManager object.

        Args:
            root_path (str, optional): The initial root path. Defaults to None.
        """

        self._root_path = None
        self.root_path = root_path

    @property
    def root_path(self):
        """
        Gets the current root path.

        Returns:
            str: The root path used for file operations.
        """
        return self._root_path

    @root_path.setter
    def root_path(self, root_path: str) -> None:
        """
        Sets the root path for file operations.

        Args:
            root_path (str): The new root path.

        Raises:
            ValueError: If the provided root path is invalid.

        Returns:
            None
        """

        if root_path is not None:
            self._root_path = self._normalize_path(root_path)

        else:
            raise ValueError("Invalid root path provided. Root path cannot be None")

    def _normalize_path(self, path: str) -> str:
        """
        Normalizes a given path by expanding tilde (~), handling leading slashes, and joining with home path if necessary.

        This function checks the given path for a leading tilde (~), a leading forward slash (/), or a missing leading slash for relative paths.
        If the path starts with a tilde, it expands the path using `os.path.expanduser`.
        If the path starts with a forward slash, it returns the path unchanged.
        If the path doesn't start with a tilde, a slash, or is a relative path without a leading slash, it joins the path with the home path using `os.path.join`.

        Args:
            path (str): The path to normalize.

        Returns:
            str: The normalized path.
        """

        if path.startswith("~"):
            # Expand tilde (~) using os.path.expanduser
            normalized_path = os.path.expanduser(path)

        elif path.startswith("/"):
            # Path starts with a forward slash, return unchanged
            normalized_path = path

        else:
            # Check for relative path without leading slash
            if not path.startswith("/") and not os.path.isabs(path):
                # Join path with home path using os.path.join
                normalized_path = os.path.join(os.path.expanduser("~"), path)

            else:
                # Path is already absolute or relative with leading slash
                normalized_path = path

        return normalized_path
    
    async def create_folder(self,
                                directory_name: str,
                                overwrite: bool = False,
                                permissions: int = 0o755,
                                subfolders: Optional[Union[Dict[str, Union[str, List[str]]], List[str]]] = None) -> None:
        """
        Creates a directory with optional overwriting and permission setting (asynchronous).

        This method creates a directory at the specified path, handling the creation
        of parent directories and optional overwriting of existing ones. It also sets
        the desired permissions for the created directory.

        Args:
            directory_name (str): The name of the directory to create, relative
                to the root path of the FileManager object.
            overwrite (bool, optional): If True, an existing directory with the
                same name will be removed before creating the new one. Defaults to False.
            permissions (int, optional): The numeric representation of the desired
                permissions for the directory (e.g., 0o755). If None, the default system
                permissions will be used. Defaults to 0o755.
            subfolders (Optional[Union[Dict[str, Union[str, List[str]]], List[str]]], optional): A string or list of subfolder names
                to create within the created directory. If None, no subfolders are created. Defaults to None.

        Raises:
            OSError: If an error occurs during directory creation, permission setting, or subfolder creation.
        """

        full_path = os.path.join(self.root_path, directory_name)

        try:
            # Handle overwriting of existing directory
            if overwrite:
                if os.path.exists(full_path):
                    if os.path.isdir(full_path):
                        shutil.rmtree(full_path, ignore_errors=True)
                        print(f"Removed existing directory '{directory_name}' and its contents.")
                    else:
                        raise OSError(f"Cannot overwrite '{full_path}'. '{directory_name}' is a file.")

            # Check and correct permissions of parent directories
            await self.checkPathPermissions(directory_path=full_path, request_permissions=permissions)

            # Create parent directories if necessary (using `makedirs` for efficiency)
            os.makedirs(name=full_path, mode=permissions, exist_ok=True)

            # Create nested subfolders recursively (if provided)
            if subfolders:
                if isinstance(subfolders, dict):
                    # Handle nested dictionary for subfolders
                    for subfolder_name, subfolder_structure in subfolders.items():
                        subfolder_path = os.path.join(full_path, subfolder_name

)
                        await self.create_folder(directory_name=subfolder_path, overwrite=overwrite, permissions=permissions, subfolders=subfolder_structure)
                elif isinstance(subfolders, str):
                    # Handle single subfolder as a string
                    subfolder_path = os.path.join(full_path, subfolders)
                    await self.create_folder(directory_name=subfolder_path, overwrite=overwrite, permissions=permissions, subfolders=None)
                elif isinstance(subfolders, list):
                    # Handle list of subfolders
                    for subfolder_name in subfolders:
                        subfolder_path = os.path.join(full_path, subfolder_name)
                        await self.create_folder(directory_name=subfolder_path, overwrite=overwrite, permissions=permissions, subfolders=None)

            # Print success message
            print(f"Created directory '{directory_name}' successfully.")

        except (FileNotFoundError, NotADirectoryError) as e:
            # More specific error handling
            print(f"Error: '{e}'.")

            if isinstance(e, FileNotFoundError):
                print(f"The specified path '{full_path}' does not exist.")
            elif isinstance(e, NotADirectoryError):
                print(f"A file with the same name '{directory_name}' already exists at the specified path.")

    async def create_file(self, file_path: Union[str, List[str]], sub_folder: Optional[str] = None) -> None:
        """
        Creates empty files at the specified paths, optionally within a subfolder relative to the root path.

        This method creates empty files at the specified paths relative to the root path of the FileManager object.
        It can accept a single file path as a string or a list of file paths. Additionally, it can specify a subfolder
        relative to the root path where the files will be created.

        Args:
            file_path (Union[str, List[str]]): The path or list of paths to the file(s) to create.
            sub_folder (Optional[str], optional): The subfolder within the root path where the files will be created.
                Defaults to None.

        Returns:
            None

        Raises:
            OSError: If an error occurs during file creation.
        """

        # Convert file_path to list if it's not already
        if not isinstance(file_path, list):
            file_path = [file_path]

        # Iterate over the list of file paths
        for path in file_path:
            # Combine with sub_folder if specified
            if sub_folder:
                full_path = os.path.join(self.root_path, sub_folder, path)
            else:
                full_path = os.path.join(self.root_path, path)

            try:
                # Create empty file
                with open(full_path, "w"):
                    pass
                print(f"Created file '{full_path}' successfully.")

            except OSError as e:
                print(f"Error creating file '{full_path}': {e}")

    async def checkPathPermissions(self, directory_path: str, request_permissions: int, resolve: bool = False) -> None:
            """
            Checks and corrects permissions of a directory path recursively, stopping at the root directory, using coroutines.

            This method checks the permissions of the given directory path and its parent directories recursively,
            stopping at the root directory. If the permissions don't match the requested permissions, it attempts
            to correct them using `os.chmod`. It utilizes coroutines and asyncio to improve performance.

            Args:
                directory_path (str): The path of the directory to check.
                request_permissions (int): The desired permissions for the directory (e.g., 0o755).
                resolve (bool, optional): If True, follows symbolic links to check the actual target.
                    Defaults to False.

            Raises:
                OSError: If an error occurs during permission checking or correction.
            """

            full_path = os.path.join(self.root_path, directory_path)
            if not os.path.exists(full_path):
                return
            
            current_path = full_path

            async def check_and_correct_permissions(path):
                try:
                    # Get current permissions using os.stat
                    current_stat = os.stat(path, follow_symlinks=resolve)
                    current_permissions = current_stat.st_mode & 0o777
                    #print(f"Path: {path} with permission: {current_permissions}")

                    # Check if permissions match
                    if current_permissions == request_permissions:
                        return  # All good, skip this directory

                    # Permissions don't match, attempt to correct
                    os.chmod(path, request_permissions)

                    #self.logger.info(f"Corrected permissions for '{path}': {current_permissions} -> {request_permissions}")
                    print(f"Corrected permissions for '{path}': {current_permissions} -> {request_permissions}")
                    

                except OSError as e:
                    raise OSError(f"Error checking permissions for '{path}': {e}")

            async def traverse_and_check(path):
                try:
                    # Check permissions of the current directory
                    await check_and_correct_permissions(path)

                    # Get list of child directories
                    child_dirs = [os.path.join(path, child) for child in os.listdir(path) if os.path.isdir(os.path.join(path, child))]

                    # Recursively check child directories
                    for child_dir in child_dirs:
                        await traverse_and_check(child_dir)

                except OSError as e:
                    raise OSError(f"Error traversing directory '{path}': {e}")

            # Start the asynchronous permission checking process
            await traverse_and_check(current_path)

    def get_file_list(self, directory: str, extension=None, recursive=False, include_dir=False) -> list:
        """
        Retrieves a list of files within a directory, optionally filtered by extension and searched recursively.

        This method searches for files in the specified directory, optionally applying
        filters based on extension and performing a recursive search within subdirectories.

        Args:
            directory (str): The path to the directory to search for files.
            extension (str, optional): The file extension to filter by (e.g., 'jpg', 'txt').
                If None, all files are included. Defaults to None.
            recursive (bool, optional): If True, searches for files recursively within
                subdirectories. Defaults to False.
            include_dir (bool, optional): If True, includes the directory name in the file paths.
                Defaults to False.

        Returns:
            list: A list of strings representing the full paths or file names of the found files.

        Raises:
            FileNotFoundError: If the specified directory does not exist.
            NotADirectoryError: If the specified path is not a directory.
        """

        full_path = os.path.join(self.root_path, directory)
        file_list = []

        try:
            # Validate directory existence and type
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Directory '{directory}' does not exist.")
            if not os.path.isdir(full_path):
                raise NotADirectoryError(f"Path '{directory}' is not a directory.")

            # Walk through directory tree
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    if extension is None or file.endswith(f".{extension}"):
                        if include_dir:
                            file_list.append(os.path.join(root, file))
                        else:
                            file_list.append(file)

                # If not recursive, break the loop after the first iteration
                if not recursive:
                    break

        except (FileNotFoundError, NotADirectoryError) as e:
            # Handle specific errors
            print(f"Error: '{e}'")
            raise e

        return file_list

    def get_files_by_extension(self, directory: str, extension: str = None) -> list:
        """
        Retrieves a list of files within a directory, optionally filtered by a specific extension.

        This method retrieves a list of files within the specified directory, optionally
        filtered by a specific file extension (e.g., 'jpg', 'txt').

        Args:
            directory (str): The path to the directory to search for files.
            extension (str, optional): The file extension to filter by (e.g., 'jpg', 'txt').
                If None, all files are included. Defaults to None.

        Returns:
            list: A list of strings representing the full paths or file names of the found files.
        """
        return self.get_file_list(directory=directory, extension=extension)

    def get_files_recursively(self, directory: str, recursive: bool = False) -> list:
        """
        Retrieves a list of files within a directory, optionally searching recursively within subdirectories.

        This method retrieves a list of files within the specified directory, optionally
        performing a recursive search within subdirectories.

        Args:
            directory (str): The path to the directory to search for files.
            recursive (bool, optional): If True, searches for files recursively within
                subdirectories. Defaults to False.

        Returns:
            list: A list of strings representing the full paths or file names of the found files.
        """
        return self.get_file_list(directory=directory, recursive=recursive)

    def get_file_paths_with_dir(self, directory: str, include_dir: bool = False) -> list:
        """
        Retrieves a list of files within a directory, optionally including directory names in the paths.

        This method retrieves a list of files within the specified directory, optionally
        including directory names in the file paths.

        Args:
            directory (str): The path to the directory to search for files.
            include_dir (bool, optional): If True, includes the directory name in the file paths.
                Defaults to False.

        Returns:
            list: A list of strings representing the full paths or file names of the found files.
        """
        return self.get_file_list(directory=directory, include_dir=include_dir)

    def get_permission_string(self, permissions: int) -> str:
        """
        Converts numeric permissions to a human-readable string.

        This method converts numeric permissions (e.g., 0o755) to a human-readable string
        format (e.g., 'rwxr-xr-x').

        Args:
            permissions (int): The numeric representation of permissions.

        Returns:
            str: A human-readable string representing the permissions.
        """

        permission_str = ''
        permission_str += 'r' if permissions & 0o400 else '-'
        permission_str += 'w' if permissions & 0o200 else '-'
        permission_str += 'x' if permissions & 0o100 else '-'
        permission_str += 'r' if permissions & 0o40 else '-'
        permission_str += 'w' if permissions & 0o20 else '-'
        permission_str += 'x' if permissions & 0o10 else '-'
        permission_str += 'r' if permissions & 0o4 else '-'
        permission_str += 'w' if permissions & 0o2 else '-'
        permission_str += 'x' if permissions & 0o1 else '-'

        return permission_str


# Example Usage:

if __name__ == '__main__':
    import os
    import asyncio

    async def main(root_path):
        # Initialize FileManager with a root directory
        
        fm = FileManager(root_path=root_path)

        # Create a folder with subfolders
        await fm.create_folder(
            directory_name="VPW_Test_Dir",
            overwrite=True,
            permissions=0o755,
            subfolders={
                "VPW_sub1": ["VPW_sub1.1", "VPW_sub1.2"],
                "VPW_sub1": ["VPW_sub2.1", "VPW_sub2.2"],
                "VPW_sub2": None,
                "VPW_sub3": None,  # No subfolders
                "VPW_sub4": {
                    "VPW_sub4.1":["VPW_sub4.1.1", "VPW_sub4.1.2"],
                }
                
                
            }
        )

        # Create an empty file
        await fm.create_file(file_path="VPW_Test_Dir/VPW_sub1/test.env")
        await fm.create_file(file_path="VPW_Test_Dir/VPW_sub1/test.toml")
        await fm.create_file(file_path="VPW_Test_Dir/VPW_sub1/test.json")
        await fm.create_file(sub_folder="VPW_Test_Dir/VPW_sub2", file_path=["test.doc", "test.xlsx","test.pdf"])

        # Get a list of files with specific extensions
        file_list = fm.get_files_by_extension(directory="VPW_Test_Dir/VPW_sub1", extension="txt")
        print("Files with extension 'txt':", file_list)

        # Get a list of all files recursively
        all_files = fm.get_files_recursively(directory="VPW_Test_Dir/VPW_sub1", recursive=True)
        print("All files recursively:", all_files)

        # Get a list of file paths with directory names included
        file_paths_with_dir = fm.get_file_paths_with_dir(directory="VPW_Test_Dir/VPW_sub1", include_dir=True)
        print("File paths with directory names:", file_paths_with_dir)

        # Check and correct permissions of directories
        await fm.checkPathPermissions(directory_path="new_folder", request_permissions=0o755, resolve=False)

    # Run the main coroutine
    root_path = os.path.join(os.getcwd(), "VisionPywods - TestFolder")
    asyncio.run(main(root_path))
