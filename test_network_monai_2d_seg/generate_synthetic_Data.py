from monai.data import create_test_image_2d
from PIL import Image
import os


def gen_data(datadir):
    # create a temporary directory and 40 random image, mask pairs
    print(f"generating synthetic data to {datadir} (this may take a while)")
    for i in range(40):
        im, seg = create_test_image_2d(128, 128, num_seg_classes=1)
        Image.fromarray(im.astype("uint8")).save(os.path.join(datadir, f"img{i:d}.png"))
        Image.fromarray(seg.astype("uint8")).save(os.path.join(datadir, f"seg{i:d}.png"))


if __name__ == "__main__":
    datadir = 'data'
    gen_data(datadir)