import cv2
import os
import time
import threading
import json
from tkinter import messagebox, filedialog

# Global variables
camera_threads = []
camera_windows = []

class CameraThread(threading.Thread):
    def __init__(self, camera_index, output_folder):
        threading.Thread.__init__(self)
        self.camera_index = camera_index - 1
        self.output_folder = output_folder
        self.stop_event = threading.Event()
        self.cap = None
        self.out = None

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"Warning: Camera {self.camera_index + 1} is not available. Skipping...")
            return
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI

        output_folder = os.path.join(self.output_folder, time.strftime("%d_%m_%Y"))
        try:
            os.makedirs(output_folder, exist_ok=True)
            if not os.access(output_folder, os.W_OK):
                raise PermissionError(f"No write permission for directory: {output_folder}")
        except (OSError, PermissionError) as e:
            print(f"Error creating directory: {output_folder}")
            print(e)
            self.stop_event.set()  # Stop thread on error
            return
        
        camera_folder = os.path.join(output_folder, f"Camera_{self.camera_index + 1}")
        try:
            os.makedirs(camera_folder, exist_ok=True)
            if not os.access(camera_folder, os.W_OK):
                raise PermissionError(f"No write permission for directory: {camera_folder}")
        except (OSError, PermissionError) as e:
            print(f"Error creating directory: {camera_folder}")
            print(e)
            self.stop_event.set()  # Stop thread on error
            return

        output_filename = f"camera{self.camera_index + 1}_{time.strftime('%Y%m%d_%H%M%S')}.avi"
        output_video_path = os.path.join(camera_folder, output_filename)
        
        try:
            self.out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (640, 480))
        except cv2.error as e:
            print(f"Error initializing VideoWriter: {output_video_path}")
            print(e)
            self.stop_event.set()  # Stop thread on error
            return

        start_time = time.time()
        while not self.stop_event.is_set():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (640, 480))
                
                current_time = time.localtime()
                formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                cv2.putText(frame, formatted_time, (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                
                elapsed_time = int(time.time() - start_time)
                cv2.putText(frame, f"Recording Time: {elapsed_time}s", (20, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                
                try:
                    self.out.write(frame)
                    window_name = f'Camera {self.camera_index + 1}'
                    if window_name not in camera_windows:
                        camera_windows.append(window_name)
                    cv2.imshow(window_name, frame)
                except cv2.error as e:
                    print(f"OpenCV error while writing frame: {e}")
                    self.stop_event.set()  # Stop thread on error
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop_event.set()
                    break
            else:
                print(f"Error: Failed to capture frame from camera {self.camera_index}.")
                break

        self.release_resources()

    def stop(self):
        self.stop_event.set()

    def release_resources(self):
        if self.cap is not None:
            self.cap.release()
        if self.out is not None:
            self.out.release()
        window_name = f'Camera {self.camera_index + 1}'
        if window_name in camera_windows:
            cv2.destroyWindow(window_name)
            camera_windows.remove(window_name)

def start_surveillance(root, user_data_file_path, user_email, num_cameras):
    global camera_threads

    # Stop any existing surveillance before starting new one
    stop_surveillance()

    # Load user data
    try:
        with open(user_data_file_path, 'r') as file:
            user_data = json.load(file)
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Error decoding JSON: {str(e)}")
        return
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {user_data_file_path} not found.")
        return
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    # Check if save_path exists in user_data
    if 'save_path' not in user_data:
        messagebox.showerror("Error", "save_path is missing in user data.")
        return

    output_folder = user_data['save_path']
    
    # Check if output folder exists and is writable
    if not os.access(output_folder, os.W_OK):
        messagebox.showerror("Error", f"Permission denied: Check folder permissions for {output_folder}")
        return
    
    camera_threads = []
    connected_cameras = 0
    for camera_index in range(1, num_cameras + 1):
        cap = cv2.VideoCapture(camera_index - 1)
        if cap.isOpened():
            cap.release()
            connected_cameras += 1
            thread = CameraThread(camera_index, output_folder)
            thread.start()
            camera_threads.append(thread)
    if connected_cameras == 0:
        print("Error: No cameras available.")

    root.resizable(False, True)

def stop_surveillance():
    global camera_threads
    for thread in camera_threads:
        thread.stop()
        thread.join()
        thread.release_resources()
    camera_threads = []
    cv2.destroyAllWindows()  # Ensure all OpenCV windows are closed

def save_output_folder(user_data_file_path, output_folder, user_email):
    try:
        with open(user_data_file_path, 'r+') as file:
            user_data = json.load(file)
            user_data['save_path'] = output_folder
            file.seek(0)
            json.dump(user_data, file, indent=4)
            file.truncate()
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    import tkinter as tk
    from login import LoginPage

    root = tk.Tk()
    root.title("Surveillance System")

    def start_surveillance_handler():
        # Display the login page
        login_page = LoginPage(root)
        root.wait_window(login_page.root)  # Wait for the login page to be closed
        
        if hasattr(root, 'current_user_email') and hasattr(root, 'current_user_file_path'):
            start_surveillance(root, root.current_user_file_path, root.current_user_email, 4)
        else:
            messagebox.showerror("Error", "User is not logged in or file path is missing.")

    surveillance_button = tk.Button(root, text="Start Surveillance", command=start_surveillance_handler)
    surveillance_button.pack(pady=20)

    root.mainloop()
 