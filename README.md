# Dicom-vert DICOM to image converter

Dicom-vert converts dicom datasets to image datasets with given image compression format. The tool creates a directory in the same file path and locates converted images in this directory.  


    ├── my_DICOM_dataset
        ├── file1.dcm
        ├── file2.dcm
        ├── ...
    ├── images_my_DICOM_dataset (created by dicom-vert)
        ├── file1.png
        ├── file2.png
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
```bash
python dicom-vert.py --path ./dataset/DICOM_files --format PNG
```