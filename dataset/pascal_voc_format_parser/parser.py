import os
import json
import shutil
import xml.etree.ElementTree as ET
import xml.dom.minidom

'''
# STRUCTURE OF PASCAL VOC DATASET

Dataset/
│── Annotations/        # XML annotation files (Pascal VOC format)
│── JPEGImages/         # Image files (.jpg, .png, etc.)
│── ImageSets/
│   ├── Main/
│   │   ├── train.txt   # List of training image filenames (without extensions)
│   │   ├── val.txt     # List of validation image filenames
│   │   ├── trainval.txt # Combined train + val
│   │   ├── test.txt    # List of test images (if applicable)
'''


def create_pascal_voc_structure(base_path):
    base_path = os.path.join(base_path, "Dataset")
    directories = [
        "Annotations",
        "JPEGImages",
        "ImageSets/Main"
    ]
    
    for directory in directories:
        path = os.path.join(base_path, directory)
        os.makedirs(path, exist_ok=True)
    
    # Create empty text files
    file_names = ["train.txt", "val.txt", "trainval.txt", "test.txt"]
    for file_name in file_names:
        open(os.path.join(base_path, "ImageSets/Main", file_name), 'a').close()

def delete_pascal_voc_structure(base_path):
    dataset_path = os.path.join(base_path, "Dataset")
    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)

def process_json(json_data, file_name,output_path):
    """Process JSON data (modify this function as needed)."""
    #print(f"Processing: {json_data}")  # Replace with actual processing logic
    json_data["image_filename"] = file_name  # Add image filename
    if create_pascal_voc_annotation(output_path, json_data) == -1: # Create Pascal VOC annotation
        return
    
    # process and copy image
    #TODO: copy image to JPEGImages folder as well with regard to the same filename as for the annotation

def process_json_files(base_path,output_path):
    """
    Recursively processes all .json files in each numbered folder inside scene_tr.
    
    Args:
        base_path (str): Path to the 'scene_tr' directory.
    """
    cnt = 0
    for folder_name in sorted(os.listdir(base_path)):  # Iterate over numbered folders
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):  # Ensure it's a directory
            for file_name in sorted(os.listdir(folder_path)):  # Iterate over files
                if file_name.endswith('.json'):  # Process only JSON files
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as json_file:
                        json_data = json.load(json_file)
                        #process_json(json_data, file_name, output_path)  # Apply function to JSON data
                        process_json(json_data, f"{cnt:06d}.xml".format(), output_path)
                        cnt+=1


def create_pascal_voc_annotation(output_path, json_data):
    """
    Converts the provided JSON data into a Pascal VOC XML annotation file.
    
    Args:
        output_path (str): Directory to save the XML file.
        json_data (dict): Data containing image details and objects.
    
    Returns:
        None (Creates an XML file in the output_path).
    """
    filename = json_data["image_filename"]  # Extract filename
    width, height, depth = 320, 240, 3  # Default values, modify if needed

    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "JPEGImages"
    ET.SubElement(annotation, "filename").text = filename
    ET.SubElement(annotation, "path").text = os.path.join(output_path, filename)

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)


    for obj in json_data["objects"]:
        try:
            obj_element = ET.SubElement(annotation, "object")
            ET.SubElement(obj_element, "name").text = obj["shape"]  # Using shape as class name
            ET.SubElement(obj_element, "pose").text = "Unspecified"
            ET.SubElement(obj_element, "truncated").text = "0"
            ET.SubElement(obj_element, "difficult").text = "0"

            bndbox = ET.SubElement(obj_element, "bndbox")
            xmin, ymin, xmax, ymax = obj["bbox"]  # Extract bounding box
            ET.SubElement(bndbox, "xmin").text = str(int(xmin))
            ET.SubElement(bndbox, "ymin").text = str(int(ymin))
            ET.SubElement(bndbox, "xmax").text = str(int(xmax))
            ET.SubElement(bndbox, "ymax").text = str(int(ymax))
        except:
            print("Error with file: ", filename)
            return -1

    # Convert ElementTree to string
    xml_str = ET.tostring(annotation, encoding="utf-8")

    # Pretty-print the XML
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="  ")  # Add indentation

    # Save XML file with proper formatting
    xml_filename = os.path.join(output_path, filename.replace(".png", ".xml"))
    with open(xml_filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)

    print(f"Saved formatted XML: {xml_filename}")
    return 0


# Example usage
if __name__== "__main__":
    # Current directory
    base_path = "." 
    delete_pascal_voc_structure(base_path)
    create_pascal_voc_structure(base_path)

    # Path to the 'scene_tr' directory
    scene_tr_path = "cylinders-6/scene_tr"
    process_json_files(scene_tr_path, output_path="Dataset/Annotations")