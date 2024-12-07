import cv2
import numpy as np
import pytesseract
import os

# Function to extract number plate from image
def extract_number_plate(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply edge detection using Canny
    edges = cv2.Canny(blurred, 100, 200)
    
    # Find contours in the edged image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get the contour with maximum area
    max_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box coordinates of the contour
    x, y, w, h = cv2.boundingRect(max_contour)
    
    # Crop the number plate using the bounding box coordinates
    number_plate = image[y:y+h, x:x+w]
    
    return number_plate

# Function to recognize text from image
def recognize_text(image):
    # Use Tesseract to recognize text
    text = pytesseract.image_to_string(image, config='--psm 6')
    return text.strip()

# Function to process video feed
def process_video():
    # Open video capture device
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Extract number plate from frame
        number_plate = extract_number_plate(frame)
        
        # Recognize text from number plate
        plate_text = recognize_text(number_plate)
        
        # Display frame with number plate
        cv2.imshow('Number Plate Recognition', frame)
        
        # If number plate text is not empty, save it to file
        if plate_text:
            filename = os.path.join(r'E:\-SINGH PRODUCTION_\sidhhi chemicals\project1_camera based\numberplate', 'number_plate.txt')
            with open(filename, 'w') as f:
                f.write(plate_text)
            print("Number plate text:", plate_text)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release video capture device and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()
