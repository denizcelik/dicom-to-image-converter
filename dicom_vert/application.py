import numpy as np
from pydicom import dcmread
from PIL import Image
from pathlib import Path, PurePath
from os import sep
from matplotlib import pyplot as plt
from copy import deepcopy


class DConverter:
    def __init__(
        self,
        path_dataset,
        format_img="PNG",
        recursive=False,
        ext_dicom=".dcm",
        resize_dim=None,
    ) -> None:

        if not Path(path_dataset).is_dir():
            raise NotADirectoryError("Given path is not a directory")

        self.path_dicom_dataset = path_dataset
        self.format_img = format_img
        self.ext_dicom = ext_dicom
        self.recursive = recursive
        self.resize_dim = int(resize_dim)
        self.list_dicom_paths, self.num_dicom_paths = self.extract_dicom_paths()

    def extract_dicom_paths(self):

        # read paths
        path_dicom_files = Path(self.path_dicom_dataset)
        # get a list of paths
        glob_str = f"*{self.ext_dicom}"
        if self.recursive:
            glob_str = "**/" + glob_str
        print("Glob String:", glob_str)
        list_dicom_paths = list(path_dicom_files.glob(glob_str))
        # extract number info.
        num_dicom_paths = len(list_dicom_paths)
        print("[INFO] Number of DICOM paths:", num_dicom_paths)
        # return list of paths
        return list_dicom_paths, num_dicom_paths

    def create_images_dir(self):

        # get path of parent directory
        path_parent = PurePath(self.path_dicom_dataset).parent
        # get name of dataset directory
        name_root_dir = PurePath(self.path_dicom_dataset).name
        # define path of converted images file
        self.path_images = path_parent / f"images_{name_root_dir}"
        print("[INFO] Images directory created at: " + str(self.path_images))
        # create a directory for converted images
        Path(self.path_images).mkdir(parents=False, exist_ok=True)

    def scale_pixels(self, data_dicom, scaler=np.uint8):

        # get image data as numpy array
        dicom_image = data_dicom.pixel_array
        # cast image array to float16
        dicom_image_f16 = dicom_image.astype(np.float16)
        # rescale image and cast it to scaler type
        dicom_image_rescaled = np.uint8(
            (np.maximum(dicom_image_f16, 0) / dicom_image_f16.max())
            * np.iinfo(scaler).max
        )
        # return scaled image
        return dicom_image_rescaled

    def resize_image(self, image, resize_dim=None):

        if resize_dim:
            image = np.array(
                Image.fromarray(image).resize((resize_dim, resize_dim))
            ).astype(np.uint8)
        return image

    def show_dicom_samples(self, list_dicom_paths, num_samples=3):

        # create subplot object
        fig, ax = plt.subplots(1, num_samples, figsize=((5 * num_samples, 15)))
        # copy list of dicom paths in order to prevent modification
        list_copy_paths = deepcopy(list_dicom_paths)

        for i in range(num_samples):

            # get a random index
            ind_random = np.random.randint(len(list_copy_paths))
            # get image path with random index
            path_random = list_copy_paths[ind_random]
            # read dicom file with random image path
            data_dicom = dcmread(path_random)
            # scale and cast the image file
            image_uint8 = self.scale_pixels(data_dicom)
            # write random obtained sample image
            ax[i].imshow(image_uint8, cmap=plt.cm.bone)
            ax[i].set_title("index:" + str(ind_random))

    def convert_dicoms_to_images(self):

        # iterate over dicom file paths
        for ind, path_dicom_current in enumerate(self.list_dicom_paths):

            # print information log
            print("[INFO] Image index:", ind)
            if self.recursive:
                print(
                    f"[INFO] Image dir.: {path_dicom_current.parent.parts[-1]} - Image name: {path_dicom_current.name.replace('.dcm', '')}"
                )

            # read dicom file
            dicom_current = dcmread(path_dicom_current)
            # convert, scale and cast the image
            img_final = self.scale_pixels(dicom_current)
            # resize image if specified
            img_final_resized = self.resize_image(img_final, self.resize_dim)
            # save converted image to defined path
            self.save_converted_image(img_final_resized, path_dicom_current)
            print("")

    def save_converted_image(self, img, path_dicom):

        # configure extension and conf. for converted images
        if self.format_img == "PNG":
            extension_img = ".png"
            configurations = None
        else:
            raise ValueError(f"Invalid image compression extention: {self.format_img}")

        # get name of current dicom file
        name_img_current = path_dicom.name[:-4]
        # define saving path for converted image
        dir_name_add = ""
        if self.recursive:
            dir_name_add = Path(path_dicom.parent.parts[-1])
            path_current_dir = Path(self.path_images) / dir_name_add
            path_current_dir.mkdir(parents=False, exist_ok=True)
        path_img_saving = (
            self.path_images / dir_name_add / Path(name_img_current + extension_img)
        )
        # print defined image path & its directory if exist
        print("[INFO] Saved to:", path_img_saving)
        # save the image to defined path
        Image.fromarray(img).save(str(path_img_saving), format=self.format_img)

    def start_app(self):

        # create a directory for images
        self.create_images_dir()
        # convert dicom files to images
        self.convert_dicoms_to_images()
