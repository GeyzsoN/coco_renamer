# This will rename the filenames of your images and will do it to the annotations too.
# IMPORTANT!
This will replace the original image names and the annotations.json so you need to actually duplicate the dataset. That is the most important part.

# The purpose of this repo is for the filenames to not be in conflict with one another

<hr>

## The renamer.py will do the following:
* change the file names in the images into a sequential format.
* once the file names are renamed, the corresponding path and filenames in the annotations are also renamed accordingly.
* each of the caretory id will be replaced with your desired string. so for example you are assigned Kitkat with category_id = 3, you can replace it with 3
* rename the image filenames with your desired category id and sequence combination, for example in my case when prompted, i type 03, and for the sequence i type 0001
* then the annotation ids will be renamed in sequence accordingly. so in cases where each image has multiple instances of the same category, it will sequentially rename those.

## system prompts you should answer:
* Current category 'Kitkat' has ID: 5
* Enter new ID for category 'Kitkat': 3
* Enter category prefix (e.g., '05' for 050001): 03
* Enter starting sequence number (e.g., '0001' for 050001): 0001
* Updating annotation IDs...
* Enter the starting ID for annotations: 030001
Then it will say: Annotation IDs have been updated.


To use this go to your terminal and type:
```python
python3 renamer.py [draganddropyourimagepath/images/] [draganddropyourannotationfile/annotations.json]
```

Credits: GK and ChatGPT4o
