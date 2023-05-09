import os
from lxml import etree

# Set the path to your XML annotations and your output folder for YOLOv5 annotations
xml_dir = r'C:\Users\Public\Documents\file chia label\xml_convert\labels'
if not os.path.exists("labeltxt"):
    os.makedirs("labeltxt")
out_dir = 'labeltxt'

# Define the class labels (optional)
class_labels = ['xop','mayin','rong']

# Loop over each XML annotation file
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith('.xml'):
        # Open the XML file and get the root
        xml_path = os.path.join(xml_dir, xml_file)
        tree = etree.parse(xml_path)
        root = tree.getroot()

        # Get the image dimensions
        width = int(root.find('size/width').text)
        height = int(root.find('size/height').text)

        # Open the output file
        out_file_path = os.path.join(out_dir, xml_file.replace('.xml', '.txt'))
        out_file = open(out_file_path, 'w')

        # Loop over each object in the XML file
        for obj in root.findall('object'):
            # Get the class label
            class_label = obj.find('name').text
            if class_labels is not None and class_label not in class_labels:
                continue
            class_index = class_labels.index(class_label) if class_labels is not None else 0

            # Get the bounding box coordinates and convert them to YOLOv5 format
            bbox = obj.find('bndbox')
            x_min = float(bbox.find('xmin').text)
            y_min = float(bbox.find('ymin').text)
            x_max = float(bbox.find('xmax').text)
            y_max = float(bbox.find('ymax').text)

            x_center = (x_min + x_max) / 2 / width
            y_center = (y_min + y_max) / 2 / height
            bbox_width = (x_max - x_min) / width
            bbox_height = (y_max - y_min) / height

            # Write the YOLOv5 annotation to the output file
            out_file.write(f'{class_index} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n')

        # Close the output file
        out_file.close()
