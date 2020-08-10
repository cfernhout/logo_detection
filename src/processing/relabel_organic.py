import os
import xml.etree.ElementTree as et

# Get a list of all files in the annotation folder
files = os.listdir("../data/")

for annotation_file in files:
    # Parse XML file
    tree = et.parse(annotation_file)
    root = tree.getroot()

    # Count all ebio occurrences and change XML text
    counter = 0
    for annot in root.iter("name"):
        keurmerk = annot.text
        if keurmerk == "ebio":
            annot.text = "organic"
            counter += 1
    print("Written {} annotations in file {}".format(counter, annotation_file))

    # Write results to files
    tree.write(annotation_file)
