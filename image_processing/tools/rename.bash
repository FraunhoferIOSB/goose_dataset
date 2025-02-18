#!/bin/bash

# Source and destination directories
SOURCE_DIR="PATH_TO_LABELS"
DEST_DIR="PATH_TO_SAVE_RENAMED_LABELS"

EXTENSIONS=('_windshield_vis.png' '_camera_left.png' '_front.png' '_realsense.png')

for ext in "${EXTENSIONS[@]}"; do
	echo "Finding labels: ${ext}"
	# Find files, create directories, and copy with the new name
	find "$SOURCE_DIR" -type f -name "*$ext" | while read -r file; do
	    # Get the relative path and create new filename
	    relative_path="${file#$SOURCE_DIR/}"
	    new_filename="${relative_path/${ext}/_labelids.png}"
	    
	    # Create the destination directory if it doesn't exist
	    mkdir -p "$DEST_DIR/$(dirname "$new_filename")"
	    
	    # Copy the file to the new location with the new name
	    cp "$file" "$DEST_DIR/$new_filename"
	done
done
