#!/bin/bash

# Step 1: Delete all content from the folder cylinder-6
CYLINDER_FOLDER="cylinders-6"
if [ -d "$CYLINDER_FOLDER" ]; then
  echo "Deleting all content from folder: $CYLINDER_FOLDER"
  rm -rf "$CYLINDER_FOLDER"/*
else
  echo "Folder $CYLINDER_FOLDER does not exist. Creating it."
  mkdir -p "$CYLINDER_FOLDER"
fi

# Step 1.5: Delete visualization file
HTML_FILE_RM="visualization/output/visualize_scene_graph_output.html" # Replace with the actual path to the generated HTML file
if [ -f "$HTML_FILE_RM" ]; then
  echo "Deleting viz file: $HTML_FILE_RM"
  rm "$HTML_FILE_RM"
else
  echo "File $HTML_FILE_RM does not exist."
fi

# Step 2: Call the script ./generate-dataset.sh with the required parameters
echo "Executing ./generate-dataset.sh 6 1 1 1 true"
./generate-dataset.sh 6 1 1 1 true

# Step 3: Execute the Python file with the parameter filenamepath.json imagepath.png
cd visualization
PYTHON_SCRIPT="visualize_scene_graph.py" # Replace this with the name of your Python script
PARAMETER="../cylinders-6/scene_tr/CLEVR_000000_pre_000.json"
PARAMETER1="../cylinders-6/image_tr/CLEVR_000000_pre_000.png"
if [ -f "$PYTHON_SCRIPT" ]; then
  echo "Executing Python script: $PYTHON_SCRIPT with parameter: $PARAMETER and $PARAMETER1"
  python3 "$PYTHON_SCRIPT" "$PARAMETER" "$PARAMETER1"
else
  echo "Python script $PYTHON_SCRIPT not found. Please ensure it exists."
fi
cd ..


# Step 4: Open the generated HTML file in the default web browser
HTML_FILE="visualization/output/visualize_scene_graph_output.html" # Replace with the actual path to the generated HTML file
if [ -f "$HTML_FILE" ]; then
  echo "Opening generated HTML file in the browser: $HTML_FILE"
  xdg-open "$HTML_FILE" # Works on Linux
else
  echo "Generated HTML file $HTML_FILE not found. Please ensure it exists."
  exit 1
fi

# Step 5: Open the PNG file in the default web browser
PNG_FILE="cylinders-6/image_tr/CLEVR_000000_pre_000.png" # Replace with the actual path to the generated HTML file
if [ -f "$PNG_FILE" ]; then
  echo "Opening PNG file: $PNG_FILE"
  xdg-open "$PNG_FILE" # Works on Linux
else
  echo "PNG file $PNG_FILE not found. Please ensure it exists."
  exit 1
fi