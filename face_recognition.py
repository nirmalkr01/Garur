import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import os
import cv2
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.video_file = None
        self.directory = None
        self.canvas = None
        self.cap = None
        self.current_index = None
        self.video_files = []
        self.original_fps = 30  # Default original FPS
        self.delay = 0  # Delay between frames
        self.start_time = 0  # Start time for managing speed

        # Fixed size for video display
        self.video_width = 640
        self.video_height = 480

        # Zoom parameters
        self.zoom_factor = 1.0  # Initial zoom factor (100%)
        self.zoom_scale_visible = False  # Flag to track if zoom scale is visible

        # Playback speed options
        self.speed_options = [0.25, 0.5, 1.0, 1.5, 2.0]  # Playback speeds
        self.current_speed_index = 2  # Default speed index (1x)

        # Flag for video playing state
        self.playing = False  # Start with video paused
        self.video_ended = False

        # Initialize the UI components
        self.setup_ui()

    def setup_ui(self):
        # Create the top level window for video player
        self.top = tk.Toplevel(self.root)
        self.top.title("Video Player")
        self.top.geometry(f"{self.video_width + 20}x{self.video_height + 100}")  # Adjusted size for scrollbars and zoom scale
        self.top.resizable(False, False)  # Disable resizing

        # Create canvas for video display
        self.canvas = tk.Canvas(self.top, width=self.video_width, height=self.video_height)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Scrollbars for canvas
        self.scroll_x = tk.Scrollbar(self.top, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Buttons for navigation and pause
        self.btn_prev = ttk.Button(self.top, text="<", width=5, command=self.play_previous_video)
        self.btn_prev.place(x=self.video_width // 2 - 100, y=self.video_height + 10)

        self.btn_pause = ttk.Button(self.top, text="❚❚", width=5, command=self.toggle_pause)
        self.btn_pause.place(x=self.video_width // 2 - 20, y=self.video_height + 10)

        self.btn_next = ttk.Button(self.top, text=">", width=5, command=self.play_next_video)
        self.btn_next.place(x=self.video_width // 2 + 60, y=self.video_height + 10)

        # Replay and Zoom Buttons
        self.btn_replay = ttk.Button(self.top, text="⏮", width=5, command=self.replay_video)
        self.btn_replay.place(relx=1.0, x=-80, y=10, anchor=tk.NE)  # Adjusted position

        # Search Button
        self.btn_search = ttk.Button(self.top, text="🔍", width=5, command=self.perform_search)
        self.btn_search.place(x=self.video_width // 2 - 300, y=self.video_height + 10)

        self.btn_zoom = ttk.Button(self.top, text="➕", width=5, command=self.toggle_zoom)
        self.btn_zoom.place(relx=1.0, x=-120, y=10, anchor=tk.NE)  # Adjusted position

        # Scale for zoom control
        self.zoom_scale = ttk.Scale(self.top, from_=0, to=100, orient=tk.HORIZONTAL, command=self.zoom_scale_changed)
        self.zoom_scale.set(0)  # Start with 0% zoom (original size)
        self.zoom_scale.pack_forget()  # Initially hide the zoom scale

        # Playback speed button
        self.speed_var = tk.StringVar(self.top)
        self.speed_var.set(f"{self.speed_options[self.current_speed_index]}x")
        self.speed_menu = ttk.Combobox(self.top, textvariable=self.speed_var, values=[f"{speed}x" for speed in self.speed_options], state="readonly", width=5)
        self.speed_menu.place(x=self.video_width // 2 + 245, y=self.video_height + 10)
        self.speed_menu.bind("<<ComboboxSelected>>", self.change_speed)  # Bind selection event to change_speed method

        # Bind double-click events for seeking
        self.canvas.bind("<Double-Button-1>", self.seek_backward_forward)  # Double-click on left or right side of video frame

    def play_video(self, video_path):
        self.video_file = video_path
        self.directory = os.path.dirname(video_path)
        self.video_files = [f for f in os.listdir(self.directory) if f.endswith(('.mp4', '.avi'))]
        self.current_index = self.video_files.index(os.path.basename(video_path))

        if self.cap:
            self.cap.release()

        self.cap = cv2.VideoCapture(self.video_file)

        if not self.cap.isOpened():
            messagebox.showerror("Error", f"Could not open video file {self.video_file}")
            self.close_player()
            return

        # Get original FPS of the video
        self.original_fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.playing = True
        self.video_ended = False
        self.update_frame()

    def update_frame(self):
        if not self.playing:
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Apply zoom factor to frame size
            if self.zoom_factor != 1.0:
                scaled_width = int(self.video_width * self.zoom_factor)
                scaled_height = int(self.video_height * self.zoom_factor)
                frame = cv2.resize(frame, (scaled_width, scaled_height))
            
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(image=frame)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
            self.canvas.image = frame  # Keep a reference to avoid garbage collection

            # Update the scroll region to accommodate the zoomed frame size
            if self.zoom_factor != 1.0:
                self.canvas.config(scrollregion=(0, 0, scaled_width, scaled_height))
            else:
                self.canvas.config(scrollregion=(0, 0, self.video_width, self.video_height))

            # Calculate delay based on current speed factor
            speed_factor = self.speed_options[self.current_speed_index]
            self.delay = int(1000 / (self.original_fps * speed_factor))

            if self.start_time == 0:
                self.start_time = self.root.after(0, self.update_frame)
            else:
                self.start_time = self.root.after(self.delay, self.update_frame)
        else:
            self.video_ended = True
            self.playing = False
            self.cap.release()

    def toggle_pause(self):
        if not self.cap or not self.cap.isOpened():
            return

        if self.playing:
            self.playing = False
            self.btn_pause.configure(text="▶")
        else:
            self.playing = True
            self.video_ended = False
            self.btn_pause.configure(text="❚❚")
            self.update_frame()

    def replay_video(self):
        if not self.cap or not self.cap.isOpened():
            self.play_video(self.video_file)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the beginning of the video
            self.playing = True
            self.video_ended = False
            self.btn_pause.configure(text="❚❚")
            self.start_time = 0
            self.update_frame()

    def toggle_zoom(self):
        if self.zoom_scale_visible:
            self.zoom_scale_visible = False
            self.zoom_scale.place_forget()
        else:
            self.zoom_scale_visible = True
            self.zoom_scale.place(x=self.video_width // 2 - 50, y=self.video_height - 30)  # Position above the pause button
            self.zoom_scale.tkraise()  # Bring to the front

    def zoom_scale_changed(self, value):
        self.zoom_factor = 1.0 + float(value) / 100  # Convert 0-100 scale to 1.0-2.0 zoom factor
        if self.playing:
            self.update_frame()  # Refresh the frame to apply zoom

    def change_speed(self, event=None):
        selected_speed = self.speed_menu.get()
        speed_index = self.speed_options.index(float(selected_speed[:-1]))  # Extract the speed factor from "1.0x" format
        self.current_speed_index = speed_index
        self.update_frame()  # Restart video with the selected speed

    def seek_backward_forward(self, event):
        if not self.cap or not self.cap.isOpened():
            return

        total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)

        # Determine click position relative to the canvas
        canvas_width = self.canvas.winfo_width()
        click_x = event.x

        if click_x < canvas_width / 2:
            # Clicked on the left side of the canvas
            new_frame = current_frame - self.original_fps * 10
            if new_frame < 0:
                new_frame = 0  # Ensure not to go below 0
        else:
            # Clicked on the right side of the canvas
            new_frame = current_frame + self.original_fps * 10
            if new_frame >= total_frames:
                new_frame = total_frames - 1  # Ensure not to exceed total frames

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        self.update_frame()

    def play_next_video(self):
        self.stop_video()
        self.current_index = (self.current_index + 1) % len(self.video_files)
        next_video = self.video_files[self.current_index]
        next_video_path = os.path.join(self.directory, next_video)
        self.play_video(next_video_path)

    def play_previous_video(self):
        self.stop_video()
        self.current_index = (self.current_index - 1) % len(self.video_files)
        prev_video = self.video_files[self.current_index]
        prev_video_path = os.path.join(self.directory, prev_video)
        self.play_video(prev_video_path)

    def stop_video(self):
        if self.cap:
            self.cap.release()
        self.playing = False
        self.video_ended = False

    def close_player(self):
        if self.cap:
            self.cap.release()
        if self.top:
            self.top.destroy()

    def perform_search(self):
        email = simpledialog.askstring("Input", "Please fill the email by which you login", parent=self.top)
        if not email:
            return  # If no email is provided, do nothing

        base_path = "E:\\-SINGH PRODUCTION_\\sidhhi chemicals\\project1_camera based\\images"
        email_folder_path = os.path.join(base_path, email)

        # Check if the email-named folder exists
        if not os.path.exists(email_folder_path):
            messagebox.showinfo("Search Result", "Data not found. Email folder does not exist.", parent=self.top)
            return

        search_query = simpledialog.askstring("Input", "Enter your search query", parent=self.top)
        if not search_query:
            return  # If no search query is provided, do nothing

        search_file_path = os.path.join(email_folder_path, search_query)
        if os.path.exists(search_file_path):
            messagebox.showinfo("Search Result", "Data is found.", parent=self.top)  # Show message with parent=self.top
        else:
            messagebox.showinfo("Search Result", "Data not found.", parent=self.top)  # Show message with parent=self.top

def open_video_file(root):
    video_file = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=(("Video Files", "*.mp4 *.avi"), ("All Files", "*.*"))
    )

    if video_file:
        player = VideoPlayer(root)
        player.play_video(video_file)

if __name__ == "__main__":
    root = tk.Tk()
    open_video_file(root)  # Open the video player
    root.mainloop()  # Ensure the Tkinter mainloop keeps running
