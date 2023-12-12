import subprocess
import os
import customtkinter
from googleapiclient.discovery import build
from pytube import YouTube
from tkinter import *
import urllib
from CTkListbox import *
from PIL import Image
from config import API_KEY

customtkinter.set_appearance_mode("dark")

class MainApp(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.master.geometry("500x350")
        self.master.title("Vai - Downloader and Converter")
        self.current_frame = None
        self.create_main_frame()
        
    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def create_main_frame(self):
        self.clear_current_frame()
        self.current_frame = customtkinter.CTkScrollableFrame(master=self.master, width=450, height=300)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # Download video from URL pop-up
        def button_click_event():
            search_entry = customtkinter.CTkInputDialog(text="Paste the video URL", title="Download")
            self.search_video(search_entry.get_input())
            self.create_search_frame()

        # App logo
        my_logo = customtkinter.CTkImage(light_image=Image.open("/Users/alifoo/Desktop/projects/Vai/logo.png"),
                                  dark_image=Image.open("/Users/alifoo/Desktop/projects/Vai/logo.png"),
                                  size=(180, 180))
        image_label = customtkinter.CTkLabel(master=self.current_frame, image=my_logo, text="")  # display image with a CTkLabel
        image_label.pack(pady=1)

        label = customtkinter.CTkLabel(master=self.current_frame, text="Welcome to Vai.", font=customtkinter.CTkFont(family="Roboto", size=24, weight='bold'))
        label.pack(padx=10)
        label = customtkinter.CTkLabel(master=self.current_frame, text="Your 1-click video downloader and converter.", font=customtkinter.CTkFont(family="Roboto", size=12))
        label.pack(pady=5,padx=10)

        search_button = customtkinter.CTkButton(master=self.current_frame, text="Download new video", font=customtkinter.CTkFont(family="Roboto", size=12),
                                                command=lambda: button_click_event())
        search_button.pack(pady=5,padx=10)
        convert_button = customtkinter.CTkButton(master=self.current_frame, text="Convert", font=customtkinter.CTkFont(family="Roboto", size=12),
                                                 command=self.create_convert_frame)
        convert_button.pack(pady=5,padx=10)

        exit_button = customtkinter.CTkButton(master=self.current_frame, text="Exit", font=customtkinter.CTkFont(family="Roboto", size=12),
                                                 command=lambda: exit())
        exit_button.pack(pady=5,padx=10)

    # Base function for back buttons
    def go_back_to_main_frame(self):
        self.create_main_frame()

    def create_search_frame(self):
        self.clear_current_frame()
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.current_frame = customtkinter.CTkScrollableFrame(master=self.master, width=450, height=300)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        label = customtkinter.CTkLabel(master=self.current_frame, text="Video downloaded successfully. Want to download more?")
        label.pack(pady=5,padx=10)

        def button_click_event():
            search_entry = customtkinter.CTkInputDialog(text="Paste the video URL", title="Download")
            self.search_video(search_entry.get_input())
            self.create_search_frame()

        search_button = customtkinter.CTkButton(master=self.current_frame, text="Download new video",
                                                command=lambda: button_click_event())
        search_button.pack(pady=5,padx=10)

        back_button = customtkinter.CTkButton(master=self.current_frame, text="Back",
                                               command=self.go_back_to_main_frame)
        back_button.pack(pady=5,padx=10)


    def create_convert_frame(self):
        self.clear_current_frame()

        self.current_frame = customtkinter.CTkScrollableFrame(master=self.master, width=450, height=300)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        def convert_click_event():
            if convert_click() is True:
                self.create_convert_frame_success_screen()
            else:
                self.create_convert_frame_failure_screen()
        
        convert_button = customtkinter.CTkButton(master=self.current_frame, text="Convert to MP3", font=customtkinter.CTkFont(family="Roboto", size=12),
                                                command=lambda: convert_click_event())
        convert_button.pack(pady=5,padx=10)

        back_button = customtkinter.CTkButton(master=self.current_frame, text="Back",
                                               command=self.go_back_to_main_frame)
        back_button.pack(pady=5, padx=10)

    # Convert page after successfully converting. Gotta find a way to do this without creating a whole new frame.
    def create_convert_frame_success_screen(self):
        self.clear_current_frame()

        self.current_frame = customtkinter.CTkScrollableFrame(master=self.master, width=450, height=300)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        success_label = customtkinter.CTkLabel(master=self.current_frame, text=f"Your video was successfully converted to mp3.")
        success_label.pack(pady=5, padx=10)

        def convert_click_event():
            if convert_click() is True:
                self.create_convert_frame_success_screen()
        
        convert_button = customtkinter.CTkButton(master=self.current_frame, text="Convert to MP3", font=customtkinter.CTkFont(family="Roboto", size=12),
                                                command=lambda: convert_click_event())
        convert_button.pack(pady=5,padx=10)

        back_button = customtkinter.CTkButton(master=self.current_frame, text="Back",
                                               command=self.go_back_to_main_frame)
        back_button.pack(pady=5, padx=10)

    def create_convert_frame_failure_screen(self):
        self.clear_current_frame()

        self.current_frame = customtkinter.CTkScrollableFrame(master=self.master, width=450, height=300)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        success_label = customtkinter.CTkLabel(master=self.current_frame, text=f"An error ocurred when trying to convert your files. Check if they are already converted.")
        success_label.pack(pady=5, padx=10)

        def convert_click_event():
            if convert_click() is True:
                self.create_convert_frame_success_screen()
        
        convert_button = customtkinter.CTkButton(master=self.current_frame, text="Convert to MP3", font=customtkinter.CTkFont(family="Roboto", size=12),
                                                command=lambda: convert_click_event())
        convert_button.pack(pady=5,padx=10)

        back_button = customtkinter.CTkButton(master=self.current_frame, text="Back",
                                               command=self.go_back_to_main_frame)
        back_button.pack(pady=5, padx=10)



    def search_video(self, query):
        # Check if the input is a valid YouTube URL
        if is_youtube_url(query):
            video_id = extract_video_id_from_url(query)
            download_video(video_id)
        else:
            print("Invalid YouTube URL.")

        self.create_main_frame()

# Youtube URL handling
def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url

# Need video id to make search
def extract_video_id_from_url(url):
    video_id = None
    if "youtube.com" in url:
        # Splitting URL in params
        query_params = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        video_id = query_params.get("v", [None])[0]
    elif "youtu.be" in url:
        video_id = url.rsplit("/", 1)[-1]
    return video_id

def download_video(video_id):
    try:
        youtube_url = f'https://www.youtube.com/watch?v={video_id}' # using the id extracted
        yt = YouTube(youtube_url)

        video_stream = yt.streams.get_highest_resolution()

        video_stream.download()
        print(f"Video '{yt.title}' downloaded successfully.")

    except Exception as e:
        print(f"Error downloading video: {str(e)}")

def video_download_button():
    search_query = input("Enter the YouTube video URL: ")
    
    if is_youtube_url(search_query):
        video_id_to_download = extract_video_id_from_url(search_query)
        download_video(video_id_to_download)
    else:
        print("Invalid YouTube URL.")

def is_file_in_directory(file_path, directory_path):
    abs_file_path = os.path.abspath(file_path)
    abs_directory_path = os.path.abspath(directory_path)
    return os.path.commonpath([abs_file_path, abs_directory_path]) == abs_directory_path

# Event function for the convert button. Convert all files at once.
def convert_click():
    input_directory = '/Users/alifoo/Desktop/projects/Vai/'
    output_directory = '/Users/alifoo/Desktop/projects/Vai/Converted_videos/'

    files = os.listdir(input_directory)

    mp4_files = [file for file in files if file.lower().endswith(".mp4")]

    try:
        for mp4_file in mp4_files:
            input_video = os.path.join(input_directory, mp4_file)
            output_mp3 = os.path.join(output_directory, os.path.splitext(mp4_file)[0] + ".mp3")

            if os.path.exists(os.path.abspath(output_mp3)):
                print(f"{input_video} is already converted to mp3.")
            else:
                convert_video_to_mp3(input_video, output_mp3)
                print(f"Conversion of {input_video} was successful!")

        return True
    # Code a better error handling in the future
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def convert_video_to_mp3(input_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        output_file
    ]
    try:
        if os.path.exists(os.path.abspath(output_file)):
            print(f"{input_file} is already converted to mp3.")
        else:
            subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Conversion of {input_file} failed!")

def main():
    root = customtkinter.CTk()
    app = MainApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()