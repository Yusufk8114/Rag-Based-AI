# Converts the videos to mp3
import os
import re
import subprocess

files = os.listdir("videos")
for file in files:
    match = re.search(r'Part_(\d+)\.mp4', file)
    if match:
        part_number = match.group(1)
        print(f"Processing Part {part_number}...")
        
        # Move this inside the 'if' block so it only runs when a match is found
        subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/Part_{part_number}.mp3"])
    else:
        print(f"Skipping or alternative format: {file}")