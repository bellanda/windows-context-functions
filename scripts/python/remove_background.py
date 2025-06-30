import pathlib
import sys

from PIL import Image
from rembg import remove

image_path = pathlib.Path(sys.argv[1])


input = Image.open(image_path)
output = remove(input)
output.save(image_path.with_stem(image_path.stem + "-NO_BACKGROUND").with_suffix(".png"))
