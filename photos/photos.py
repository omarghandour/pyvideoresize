import os
import cv2
import tkinter as tk
from tkinter import filedialog

def compress_and_convert_to_webp(input_folder, output_folder, quality=70, max_size=(1280, 1280)):
    os.makedirs(output_folder, exist_ok=True)
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".png")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".webp"
            output_path = os.path.join(output_folder, output_filename)

            try:
                img = cv2.imread(input_path)
                if img is None:
                    print(f"❌ Could not read {filename}")
                    continue

                # Resize if needed
                height, width = img.shape[:2]
                max_w, max_h = max_size
                scale = min(max_w / width, max_h / height, 1.0)
                if scale < 1.0:
                    img = cv2.resize(img, (int(width * scale), int(height * scale)))

                # Save as WebP
                cv2.imwrite(output_path, img, [cv2.IMWRITE_WEBP_QUALITY, quality])
                print(f"✔ Converted: {filename} → {output_filename}")
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    # Hide tkinter root window
    root = tk.Tk()
    root.withdraw()

    print("📂 Select the input folder with photos:")
    input_folder = filedialog.askdirectory(title="Select Input Folder")

    if not input_folder:
        print("❌ No input folder selected. Exiting.")
        exit()

    print("💾 Select the output folder to save WebP images:")
    output_folder = filedialog.askdirectory(title="Select Output Folder")

    if not output_folder:
        print("❌ No output folder selected. Exiting.")
        exit()

    compress_and_convert_to_webp(input_folder, output_folder)
