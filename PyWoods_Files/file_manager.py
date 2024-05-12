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
    * **File Information Retrieval:**
        - `get_file_list(directory: str, extension=None, recursive=False, include_dir=False) -> list:`
            Retrieves a list of files within a directory (relative to the root path), optionally filtered by extension, searched recursively within subdirectories, or including directory names in the results.
        - `get_files_by_extension(self, directory: str, extension: str = None) -> list:`
            Retrieves a list of files within a directory, optionally filtered by a specific extension (e.g., 'jpg', 'txt').
        - `get_files_recursively(self, directory: str, recursive: bool = False) -> list:`
            Retrieves a list of files within a directory, searching recursively within subdirectories if specified.
        - `get_file_paths_with_dir(self, directory: str, include_dir: bool = False) -> list:`
            Retrieves a list of files within a directory, optionally including directory names in the paths.

    By utilizing this class, you can manage file and directory operations within a designated root directory structure in a robust manner.

    **Usage Example:**

    ```python
    file_manager = FileManager("/path/to/your/root/directory")

    # Create a new folder
    file_manager.create_folder("/subdirectory")

    # Check permissions for a file
    file_manager.checkPathPermissions("/important_file.txt")

    # Retrieve a list of files
    all_files = file_manager.get_file_list("/documents")

    # Get only JPG files
    jpg_files = file_manager.get_files_by_extension("/images", extension=".jpg")

    # Get all files recursively (including subdirectories)
    all_files_recursive = file_manager.get_files_recursively("/documents", recursive=True)

    # Get file paths with directory names
    file_paths = file_manager.get_file_paths_with_dir("/documents", include_dir=True)
    ```
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
    
    @staticmethod
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
                        subfolder_path = os.path.join(full_path, subfolder_name)
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

            # Iterate through directory entries using os.scandir
            for entry in os.scandir(full_path):
                # Skip hidden files/directories (optional)
                # if entry.is_hidden():
                #     continue

                full_entry_path = os.path.join(full_path, entry.name)

                if entry.is_file():
                    if extension is None or full_entry_path.endswith("." + extension):
                        if include_dir:
                            file_list.append(os.path.relpath(full_entry_path, directory))
                        else:
                            file_list.append(entry.name)

                elif recursive and entry.is_dir():
                    sub_file_list = self.get_file_list(full_entry_path, extension, recursive, include_dir)
                    if include_dir:
                        for sub_file in sub_file_list:
                            file_list.append(os.path.join(entry.name, sub_file))
                    else:
                        file_list.extend(sub_file_list)

        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"Error accessing directory '{directory}': {e}")

        return file_list
    
    def get_files_by_extension(self, directory: str, extension: str = None) -> list:
        """
        Retrieves a list of files within a directory, optionally filtered by extension.

        This method searches for files in the specified directory, optionally applying
        a filter based on the provided extension (e.g., 'jpg', 'txt').

        Args:
            directory (str): The path to the directory to search for files.
            extension (str, optional): The file extension to filter by.
                Defaults to None (all files included).

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

            # Iterate through directory entries using os.scandir
            for entry in os.scandir(full_path):
                # Skip hidden files/directories (optional)
                # if entry.is_hidden():
                #     continue

                full_entry_path = os.path.join(full_path, entry.name)

                if entry.is_file():
                    if extension is None or full_entry_path.endswith("." + extension):
                        file_list.append(full_entry_path)  # Append full path

        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"Error accessing directory '{directory}': {e}")

        return file_list
    
    def get_files_recursively(self, directory: str, recursive: bool = False) -> list:
        """
        Retrieves a list of files within a directory, searching recursively if specified.

        This method searches for files in the specified directory and, if the
        `recursive` parameter is True, also searches within subdirectories.

        Args:
            directory (str): The path to the directory to search for files.
            recursive (bool, optional): If True, searches for files recursively
                within subdirectories. Defaults to False.

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

            # Iterate through directory entries using os.scandir
            for entry in os.scandir(full_path):
                # Skip hidden files/directories (optional)
                # if entry.is_hidden():
                #     continue

                full_entry_path = os.path.join(full_path, entry.name)

                if entry.is_file():
                    file_list.append(full_entry_path)  # Append full path

                elif recursive and entry.is_dir():
                    # Recursive call for subdirectories
                    sub_files = self.get_files_recursively(full_entry_path, recursive)
                    file_list.extend(sub_files)

        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"Error accessing directory '{directory}': {e}")

        return file_list

    def get_file_paths_with_dir(self, directory: str, include_dir: bool = False) -> list:
        """
        Retrieves a list of files within a directory, optionally including directory names.

        This method searches for files in the specified directory and, if the
        `include_dir` parameter is True, prepends the directory name to the file names
        in the returned list.

        Args:
            directory (str): The path to the directory to search for files.
            include_dir (bool, optional): If True, includes the directory name in the
                file paths. Defaults to False.

        Returns:
            list: A list of strings representing the file paths or file names of the found files.

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

            # Iterate through directory entries using os.scandir
            for entry in os.scandir(full_path):
                # Skip hidden files/directories (optional)
                # if entry.is_hidden():
                #     continue

                full_entry_path = os.path.join(full_path, entry.name)

                if entry.is_file():
                    if include_dir:
                        # Prepend directory name if requested
                        file_list.append(os.path.relpath(full_entry_path, directory))
                    else:
                        file_list.append(entry.name)  # Append filename only

        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"Error accessing directory '{directory}': {e}")

        return file_list



    def get_permission_string(self, permissions: int) -> str:
        """
        Converts numeric permissions to a human-readable string.

        This method takes numeric permissions (e.g., 0o755) and converts them
        into a string representation like "rwxr-xr-x" for user, group, and others.

        Args:
            permissions (int): The numeric permissions to convert.

        Returns:
            str: The human-readable string representation of the permissions.
        """

        permission_string = ""

        # Extract permission bits for user, group, and others
        user_perms = (permissions & 0o700) >> 6
        group_perms = (permissions & 0o070) >> 3
        other_perms = permissions & 0o007

        # Convert permission bits to characters (rwx-)
        permission_chars = {
            0: "-",
            1: "--x",
            2: "-w-",
            3: "-wx",
            4: "r-",
            5: "r-x",
            6: "rw-",
            7: "rwx"
        }

        permission_string += permission_chars[user_perms]
        permission_string += permission_chars[group_perms]
        permission_string += permission_chars[other_perms]

        return permission_string
