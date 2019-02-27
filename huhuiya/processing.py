import os
import argparse
import glob
import PIL
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", help="path to folder containing images")
parser.add_argument("--target_dir", help="path to folder containing images")
parser.add_argument("--output_dir", help="path to folder containing images")
a = parser.parse_args()
input_paths = glob.glob(os.path.join(a.input_dir, "*.jpg"))
target_paths = glob.glob(os.path.join(a.target_dir, "*.jpg"))
output_dir = a.output_dir
#
#def save_images(fetches, step=None):
#    image_dir = os.path.join(a.output_dir, "images")
#    if not os.path.exists(image_dir):
#        os.makedirs(image_dir)
#
#    filesets = []
#    for i, in_path in enumerate(fetches["paths"]):
#        name, _ = os.path.splitext(os.path.basename(in_path.decode("utf8")))
#        fileset = {"name": name, "step": step}
#        for kind in ["inputs", "outputs", "targets"]:
#            filename = name + "-" + kind + ".png"
#            if step is not None:
#                filename = "%08d-%s" % (step, filename)
#            fileset[kind] = filename
#            out_path = os.path.join(image_dir, filename)
#            contents = fetches[kind][i]
#            with open(out_path, "wb") as f:
#                f.write(contents)
#        filesets.append(fileset)
#    return filesets


def get_name(path):
    name, _ = os.path.splitext(os.path.basename(path))
    return name

    # if the image names are numbers, sort by the value rather than asciibetically
    # having sorted inputs means that the outputs are sorted in test mode


if all(get_name(path).isdigit() for path in input_paths):
    input_paths = sorted(input_paths, key=lambda path: int(get_name(path)))
else:
    input_paths = sorted(input_paths)

if all(get_name(path).isdigit() for path in target_paths):
    target_paths = sorted(target_paths, key=lambda path: int(get_name(path)))
else:
    target_paths = sorted(target_paths)

#target=Image.new('RGB',2*image_input.size[0],image_input.size[1])
for i in range(len(input_paths)):
    image_input= Image.open(input_paths[i])
    image_target = Image.open(target_paths[i])
    #[w1,h1] = image_input.size()
    #[w2,h2] = image_target.size()
    target=Image.new('RGB',(2*image_input.size[0],image_input.size[1]))
    w=image_input.size[0]
    h=image_input.size[1]
    image_input = image_input.resize((w,h),PIL.Image.ANTIALIAS)
    image_target = image_target.resize((w,h),PIL.Image.ANTIALIAS)
    target.paste(image_input,(0,0,w,image_target.size[1]))
    target.paste(image_target,(w,0,w+image_target.size[0],image_target.size[1]))
    target.show()
    target.save(output_dir+'/'+str(i)+'.jpg', quality = 80)
