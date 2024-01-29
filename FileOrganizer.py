from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tkinter import Tk, filedialog

source_dir = "C:/Users/Orion/Downloads"
dest_dir_sfx = ""
dest_dir_music = "C:/Users/Orion/Downloads/Music"
dest_dir_video = "C:/Users/Orion/Downloads/Video"
dest_dir_image = "C:/Users/Orion/Downloads/Image"
dest_dir_documents = "C:/Users/Orion/Downloads/Documents"
dest_dir_software = "C:/Users/Orion/Downloads/Software"

# supported image types
image_extensions = [
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jif",
    ".jfif",
    ".jfi",
    ".png",
    ".gif",
    ".webp",
    ".tiff",
    ".tif",
    ".psd",
    ".raw",
    ".arw",
    ".cr2",
    ".nrw",
    ".k25",
    ".bmp",
    ".dib",
    ".heif",
    ".heic",
    ".ind",
    ".indd",
    ".indt",
    ".jp2",
    ".j2k",
    ".jpf",
    ".jpf",
    ".jpx",
    ".jpm",
    ".mj2",
    ".svg",
    ".svgz",
    ".ai",
    ".eps",
    ".ico",
]
# supported Video types
video_extensions = [
    ".webm",
    ".mpg",
    ".mp2",
    ".mpeg",
    ".mpe",
    ".mpv",
    ".ogg",
    ".mp4",
    ".mp4v",
    ".m4v",
    ".avi",
    ".wmv",
    ".mov",
    ".qt",
    ".flv",
    ".swf",
    ".avchd",
]
# supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# supported Document types
document_extensions = [
    ".doc",
    ".docx",
    ".odt",
    ".pdf",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
]

software_extensions = [".exe", ".msi"]

archive_extensions = [".zip", ".rar", ".7z", ".tar"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_software_files(entry, name)
                self.check_archieves_files(entry, name)

    # * Checks all Audio Files
    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    # * Checks all Video Files
    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    # * Checks all Image Files
    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    # * Checks all Document Files
    def check_document_files(self, entry, name):
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(
                documents_extension.upper()
            ):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    # * Checks all Software Files
    def check_software_files(self, entry, name):
        for software_extension in software_extensions:
            if name.endswith(software_extension) or name.endswith(
                software_extension.upper()
            ):
                move_file(dest_dir_software, entry, name)
                logging.info(f"Moved document file: {name}")

    # * Checks all Archieve Files
    def check_archieves_files(self, entry, name):
        for archive_extension in archive_extensions:
            if name.endswith(archive_extension) or name.endswith(
                archive_extension.upper()
            ):
                move_file(dest_dir_archieve, entry, name)
                logging.info(f"Moved document file: {name}")


def select_destination(title):
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory(title=f"Select for {title} directory")


if __name__ == "__main__":
    print("Program is running....")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Ask the user to select the source directory
    root = Tk()
    root.withdraw()
    source_dir = filedialog.askdirectory(title="Select Source Directory")

    # Set the destination directories based on the selected source directory
    dest_dir_sfx = select_destination("SFX")
    dest_dir_music = select_destination("Music")
    dest_dir_video = select_destination("Video")
    dest_dir_image = select_destination("Image")
    dest_dir_documents = select_destination("Documents")
    dest_dir_software = select_destination("Software")
    dest_dir_archieve = select_destination("Archives")

    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
