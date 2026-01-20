import os
import sys

# Get the path where the script is running
current_dir = os.getcwd()
conflict_file = os.path.join(current_dir, "qdrant_client.py")
conflict_folder = os.path.join(current_dir, "qdrant_client")

print(f"Checking directory: {current_dir}")

if os.path.exists(conflict_file):
    print(f"\n[CRITICAL] Found conflicting file: {conflict_file}")
    print("ACTION: Delete this file immediately.")
elif os.path.exists(conflict_folder):
    print(f"\n[CRITICAL] Found conflicting folder: {conflict_folder}")
    print("ACTION: Rename or delete this folder immediately.")
else:
    print("\n[OK] No local 'qdrant_client' file or folder found in this directory.")
    print("If you still have issues, check your site-packages installation.")