import shutil
import logging
from pathlib import Path
from threading import Thread

logging.basicConfig(level=logging.INFO)


class FileSorter:
    def __init__(self, source_folder_path: str, target_folder_path: str) -> None:
        """
        Initialize FileSorter object with source and target folder paths.
        """
        self.source_folder_path = source_folder_path
        self.target_folder_path = target_folder_path

    def sort_files(self) -> None:
        """
        Sort files from source folder into target folder based on their extensions.
        """
        file_mapping: dict = {}
        source_folder = Path(self.source_folder_path)
        target_folder = Path(self.target_folder_path)

        # Check if source folder exists and is a directory
        if not source_folder.exists() or not source_folder.is_dir():
            logging.error("Source folder does not exist or is not a directory.")
            return

        # Check if target folder exists and is a directory
        if not target_folder.exists() or not target_folder.is_dir():
            logging.error("Target folder does not exist or is not a directory.")
            return

        # Iterate over files in source folder and organize them by extension
        for file_path in source_folder.rglob("*"):
            if file_path.is_file():
                extension = file_path.suffix
                file_mapping.setdefault(extension, []).append(file_path)

        # Move files into folders based on their extension
        for extension, files in file_mapping.items():
            extension_folder = target_folder / extension[1:]
            extension_folder.mkdir(parents=True, exist_ok=True)
            for file_path in files:
                file_path_new = extension_folder / file_path.name
                shutil.copy(file_path, file_path_new)

        logging.info("File copying completed successfully.")


if __name__ == "__main__":
    source_folder_path = input("Please enter a path to the source folder: ").strip()
    target_folder_path = input("Please the path to the destination folder: ").strip()

    file_sorter = FileSorter(source_folder_path, target_folder_path)
    thread = Thread(target=file_sorter.sort_files)
    thread.start()
    thread.join()
