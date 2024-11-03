import os
import json
import sys

def prompt_for_new_category_ids(categories):
    new_category_ids = {}
    for category in categories:
        current_id = category['id']
        name = category['name']
        print(f"Current category '{name}' has ID: {current_id}")
        new_id = input(f"Enter new ID for category '{name}': ")
        new_category_ids[current_id] = int(new_id)
    return new_category_ids

def rename_images_and_update_annotations(dataset_image_path, annotations_path):
    # Load annotations
    with open(annotations_path, 'r') as file:
        annotations = json.load(file)
    
    # Get new category IDs from user
    categories = annotations['categories']
    new_category_ids = prompt_for_new_category_ids(categories)

    # Update category IDs in annotations
    for category in categories:
        if category['id'] in new_category_ids:
            category['id'] = new_category_ids[category['id']]

    # Prompt for category prefix and starting sequence
    prefix = input("Enter category prefix (e.g., '05' for 050001): ")
    starting_sequence = int(input("Enter starting sequence number (e.g., '0001' for 050001): "))

    # Prepare key-value pairs for image renaming and ID updating
    file_mapping = {}
    new_image_id = starting_sequence  # Start from user-defined sequence
    
    for image_data in annotations['images']:
        old_filename = image_data['file_name']
        file_path = os.path.join(dataset_image_path, old_filename)

        if os.path.isfile(file_path):
            # Generate new filename and image ID
            new_filename = f"{int(prefix):02d}{new_image_id:04d}.jpg"
            new_image_path = os.path.join(dataset_image_path, new_filename)
            
            # Rename the actual file
            os.rename(file_path, new_image_path)
            
            # Update JSON fields
            new_id = int(f"{int(prefix):02d}{new_image_id:04d}")  # Numeric ID in the format 030001
            new_path = os.path.join("/datasets/anothertestdataset", new_filename)  # Adjust as needed

            # Map old filename and old image ID to the new filename and new ID
            file_mapping[image_data['id']] = {'new_filename': new_filename, 'new_id': new_id}
            image_data['id'] = new_id  # Update the id field to the new numeric format
            image_data['file_name'] = new_filename
            image_data['path'] = new_path  # Update the path field
            
            new_image_id += 1  # Increment sequence number
    
    # Update image IDs in annotations with the mappings
    update_annotations_with_mappings(annotations, file_mapping, new_category_ids)

    # Save updated annotations
    with open(annotations_path, 'w') as file:
        json.dump(annotations, file, indent=4)

def get_category_id_from_annotations(annotations, filename):
    for image in annotations['images']:
        if image['file_name'] == filename:
            for annotation in annotations['annotations']:
                if annotation['image_id'] == image['id']:
                    return annotation['category_id']
    return None

def update_annotations_with_mappings(annotations, file_mapping, new_category_ids):
    for annotation in annotations['annotations']:
        # Update image_id in annotations to match new image ids
        old_image_id = annotation['image_id']
        if old_image_id in file_mapping:
            new_id = file_mapping[old_image_id]['new_id']
            annotation['image_id'] = new_id  # Update image_id to new format in annotations
        
        # Update category_id in annotations
        old_category_id = annotation['category_id']
        if old_category_id in new_category_ids:
            annotation['category_id'] = new_category_ids[old_category_id]

def get_filename_by_image_id(images, image_id):
    for image in images:
        if image['id'] == image_id:
            return image['file_name']
    return None

def update_annotation_ids(annotations):
    print("Updating annotation IDs...")
    starting_id = int(input("Enter the starting ID for annotations: "))
    
    for annotation in annotations['annotations']:
        annotation['id'] = starting_id
        starting_id += 1  # Increment ID for each subsequent annotation


def main(dataset_image_path, annotations_path):
    rename_images_and_update_annotations(dataset_image_path, annotations_path)
    
    # Load annotations again after renaming and updating image IDs
    with open(annotations_path, 'r') as file:
        annotations = json.load(file)
    
    # Call the function to update annotation IDs
    update_annotation_ids(annotations)
    
    # Save updated annotations with new annotation IDs
    with open(annotations_path, 'w') as file:
        json.dump(annotations, file, indent=4)
    print("Annotation IDs have been updated.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py dataset_image_path annotations_path")
    else:
        dataset_image_path = sys.argv[1]
        annotations_path = sys.argv[2]
        main(dataset_image_path, annotations_path)
