import pathlib
import sys

import pillow_heif
from PIL import Image

file_path = pathlib.Path(sys.argv[1])


PATH = pathlib.Path(file_path)

if ".heic" not in file_path.name:
    print("Arquivo não é um HEIC")
    exit()

heif_file = pillow_heif.read_heif(file_path)


image = Image.frombytes(
    heif_file.mode,
    heif_file.size,
    heif_file.data,
    "raw",
)
image.save(PATH.with_suffix(".jpg"), format="JPEG")
