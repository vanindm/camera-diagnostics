import argparse
from PIL import Image
from tqdm import tqdm

from rich.console import Console
from rich.table import Table

console = Console()

parser = argparse.ArgumentParser(
        prog="Bad Pixels Detector",
        description="Detect bad pixels on pitch black image")

parser.add_argument('filename')
parser.add_argument('-t', '--treshold', type=float, default=0.9)
parser.add_argument('-c', '--count', action="store_true")
parser.add_argument('-p', '--progress', action="store_true")
parser.add_argument('-v', '--verbose', type=int, choices=[0, 1, 2])

args = parser.parse_args()

def iter_wrap(x):
    global args
    if args.progress:
        return tqdm(x)
    return x

bad_pixels = []

max_value = 255

with Image.open(args.filename) as img:
    pixels = img.load()
    w, h = img.size

    for y in iter_wrap(range(h)):
        for x in range(w):
            r, g, b = pixels[x, y]
            if r > (args.treshold * max_value) or g > (args.treshold * max_value) or b > (args.treshold * max_value):
                bad_pixels.append((x, y, (r, g, b)))

if args.count:
    if args.verbose == 2:
        print(f"Found {len(bad_pixels)} bad pixels.")
    else:
        print(len(bad_pixels))

if args.verbose == 2:
    table = Table(title="Bad pixels")
    table.add_column("X", no_wrap=True)
    table.add_column("Y", no_wrap=True)
    table.add_column("R", no_wrap=True)
    table.add_column("G", no_wrap=True)
    table.add_column("B", no_wrap=True)
    for bad_pixel in bad_pixels:
        table.add_row(str(bad_pixel[0]), str(bad_pixel[1]), str(bad_pixel[2][0]), str(bad_pixel[2][1]), str(bad_pixel[2][2]))
    console.print(table)
elif args.verbose == 1:
    print(bad_pixels)
