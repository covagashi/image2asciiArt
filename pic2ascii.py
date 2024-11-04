import sys
import numpy as np
from PIL import Image

# Contrast on a scale -10 -> 10
contrast = 10
density = ('$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|'
           '()1{}[]?-_+~i!lI;:,"^`\'.            ')
density = density[:-11+contrast]
n = len(density)

img_name = sys.argv[1]
try:
    width = int(sys.argv[2])
except IndexError:
    # Default ASCII image width.
    width = 100

# Read in the image, keeping the alpha channel if it exists
img = Image.open(img_name)


if img.mode == 'RGBA':
    _, _, _, alpha = img.split()
    img_gray = img.convert('L')
else:
    img_gray = img.convert('L')
    alpha = None

# Resize the image as required.
orig_width, orig_height = img_gray.size
r = orig_height / orig_width
height = int(width * r * 0.5)
img_gray = img_gray.resize((width, height), Image.Resampling.LANCZOS)
if alpha:
    alpha = alpha.resize((width, height), Image.Resampling.LANCZOS)

# Now map the pixel brightness to the ASCII density glyphs.
arr = np.array(img_gray)
if alpha:
    alpha_arr = np.array(alpha)

for i in range(height):
    for j in range(width):
        
        if alpha is not None and alpha_arr[i,j] == 0:
            print(' ', end='')
        else:
            p = arr[i,j]
            k = int(np.floor(p/256 * n))
            print(density[n-1-k], end='')
    print()