# Dicom-vert DICOM to image converter

Dicom-vert converts DICOM formatted datasets to image datasets with given image compression format. The tool creates a directory in the same file path and locates converted images in this directory. Dicom-verts supports conversion in two different directory (folder) structure type as follows: 

Folder Structure Type A:

    ├── my_DICOM_dataset
        ├── file1.dcm
        ├── file2.dcm
        ├── ...
    ├── images_my_DICOM_dataset (created by dicom-vert)
        ├── file1.png
        ├── file2.png
        ├── ...

Folder Structure Type B:

    ├── my_DICOM_dataset
        ├── directory1
            ├── file1.dcm
            ├── file1.dcm
        ├── directory2
            ├── file1.dcm
            ├── file1.dcm
        ├── ...
    ├── images_my_DICOM_dataset (created by dicom-vert)
        ├── directory1
            ├── file1.png
            ├── file1.png
        ├── directory2
            ├── file1.png
            ├── file1.png
        ├── ...


# How to use
1- Clone the repository to your local environment
```bash
git clone https://github.com/denizcelik/dicom-to-image-converter.git
```
2- Install required python packages by using requirement.txt file
```bash
pip install -r requirements.txt
```
3- Run the application with specified arguments to convert your dataset  
For folder structure type A:
```bash
python dicom-vert.py --path ./dataset/DICOM_files --format PNG
```
For folder structure type B:
```bash
python dicom-vert.py --recursive --path ./dataset/DICOM_files --format PNG 
```