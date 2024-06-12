#Place your image in the folder with the image-hodler folder, then run the script.

from progress.spinner import MoonSpinner
from PIL import Image
import numpy as np
import os

def closest(color):
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    return np.where(distances == np.amin(distances))[0][0]

done = False
spinner = MoonSpinner('Processing… ')

img_folder = 'image-holder'
img_file = os.listdir(img_folder)[0]
img_path = os.path.join(os.path.basename(img_folder), os.path.basename(img_file))

img = Image.open(img_path, 'r')
img.putalpha(255)
img_val = list(img.getdata())

ref = Image.open('ref.png', 'r')
ref_val = list(ref.getdata())
colors = np.array(ref_val)

final_val = []

w, h = img.size
img_out = Image.new(mode='RGB', size=(w, h))

inc = 0
for i in img_val:
    ndx = closest(i)
    final_val.append(ndx)
    xpos = inc % w
    ypos = inc // w
    img_out.putpixel((xpos, ypos), ref_val[ndx])
    if inc % 5000 == 0:
        spinner.next()
    inc += 1
    
done = True
final = ', '.join(str(x) for x in final_val)
with open("outfile.txt", "w") as outfile:
    outfile.write(final)
img_out.save('output-' + os.path.basename(img_file))
print("\rProcess Completed!")

