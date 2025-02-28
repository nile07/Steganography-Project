import cv2
import os
import string

# try:

#     img = cv2.imread("D:\Downloads\Aicte Intership\Stenography-main\Stenography-main\messi.jpg") # Replace with the correct image path#image
# else:

try:
    # Replace with your image path
    image_path = "D:\Downloads\Aicte Intership\Stenography-main\Stenography-main\messi.jpg"
    
    # Check if image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: Image file not found at '{image_path}'")
    
    # Try to read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Error: Failed to read image - file may be corrupted or invalid format")

except Exception as e:
    print(e)
    exit()


msg = input("Enter secret message:")
password = input("Enter a passcode:")

d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

m = 0
n = 0
z = 0

for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3

cv2.imwrite("encryptedImage.jpg", img)
os.system("start encryptedImage.jpg")  # Use 'start' to open the image on Windows

message = ""
n = 0
m = 0
z = 0

pas = input("Enter passcode for Decryption: ")
if password == pas:
    for i in range(len(msg)):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    print("Decryption message:", message)
else:
    print("YOU ARE NOT auth")
# Keep the terminal open until user presses Enter
input("\nPress Enter to exit...")  # <-- Added this line