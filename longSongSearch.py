import os
import shutil
from tinytag import TinyTag
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import logging

# Configure log file
logging.basicConfig(filename='error.txt', level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def search_songs(directory, include_subdirs, duration_threshold):
    matching_songs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp3', '.ogg', '.m4a', '.opus', '.midi')):
                file_path = os.path.join(root, file)
                try:
                    tag = TinyTag.get(file_path)
                    if tag.duration and tag.duration > duration_threshold:
                        matching_songs.append(file_path)
                except Exception as e:
                    logging.error(f"Error processing the file {file_path}: {e}")
        if not include_subdirs:
            break
    return matching_songs

def move_songs(songs, target_directory, duration_label):
    target_folder = os.path.join(target_directory, f'more than {duration_label} minutes')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for song in songs:
        try:
            shutil.move(song, target_folder)
        except Exception as e:
            logging.error(f"Error moving the file {song}: {e}")

def ask_include_subdirs():
    return messagebox.askyesno("Search in Subdirectories", "Do you also want to search in subdirectories?")

def search_and_move_songs(duration_threshold, duration_label):
    directory = filedialog.askdirectory()
    if directory:
        include_subdirs = ask_include_subdirs()
        try:
            matching_songs = search_songs(directory, include_subdirs, duration_threshold)
            if matching_songs:
                move_songs(matching_songs, directory, duration_label)
                messagebox.showinfo("Completed", f"{len(matching_songs)} songs have been moved to the folder 'more than {duration_label} minutes'.")
            else:
                messagebox.showinfo("No Results", f"No songs found longer than {duration_label} minutes.")
        except Exception as e:
            logging.error(f"Error during song search and move: {e}")
            messagebox.showerror("Error", "An error occurred during the search and movement of songs. Check the error.txt file for more details.")

def main():
    root = tk.Tk()
    root.title("Search Songs by Duration")

    frame = ttk.Frame(root)
    frame.pack(pady=20)

    def open_search_window(duration_threshold, duration_label):
        search_and_move_songs(duration_threshold, duration_label)

    btn_search_5 = ttk.Button(root, text="Search for songs longer than 5 minutes", 
                              command=lambda: open_search_window(300, '5'))
    btn_search_5.pack(pady=10)

    btn_search_10 = ttk.Button(root, text="Search for songs longer than 10 minutes", 
                               command=lambda: open_search_window(600, '10'))
    btn_search_10.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
