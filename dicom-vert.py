import dicom_vert.application as app
import argparse

if __name__ == "__main__":

    try:
        # define parser for command line arguments
        parser = argparse.ArgumentParser(
            prog="DicomVert",
            description="Converts DICOM files to images in desired image format",
            epilog="""
            DICOM files can be converted to listed image formats.

            "--path" flag provides source path of dicom containing folder 
            "--format" flag decides images compression format.
            "--recursive" flag provides information of folders structure 
            """,
        )

        # define required arguments
        parser.add_argument("-p", "--path")
        parser.add_argument("-f", "--format", default="PNG")
        parser.add_argument("-r", "--recursive", action="store_true")
        parser.add_argument("-x", "--dicomext", default=".dcm")
        parser.add_argument("-s", "--resize", default=None)

        # parse arguments
        args = parser.parse_args()

        # call the application to start the process with given arguments
        converter = app.DConverter(
            args.path, args.format, args.recursive, args.dicomext, args.resize
        )

        converter.start_app()

    except TypeError as er:
        print(f"[ERROR] Unexpected or missing arguments were given: {er}")
