from PIL import Image, ImageDraw, ImageFont
import os;
import glob;
import tkinter;
from tkinter import filedialog;
import piexif;


OUTPUT_PATH = "watermark";

def writeOnImage(text, image):
    width, height = image.size;
    #open the image context for drawing
    context = ImageDraw.Draw(image);
    #hard-code the font
    font = ImageFont.truetype('C:/Windows/Fonts/Verdana.ttf', 45);
    textWidth,textHeight = context.textsize(text, font=font);
    textHeight = textHeight + 5; #give some buffer at the bottom
    #draw gray text for drop shadow with small offset
    context.text((width-(textWidth+3),height-textHeight), text, fill=(128,128,128), font=font);
    #draw black text for text
    context.text((width-(textWidth+5),height-(textHeight+3)), text, fill=(0,0,0), font=font);
    return;
#end writeOnImage

root = tkinter.Tk();
folder_selected = filedialog.askdirectory();

os.chdir(folder_selected);
root.destroy();

if(not os.path.isdir(OUTPUT_PATH)):
    os.mkdir(OUTPUT_PATH);


for file in glob.glob("*.jpg"):
    image = Image.open(file);
    
    exif_dict = piexif.load(image.info['exif'])
    
    exif_dict["0th"][piexif.ImageIFD.Copyright] = "Joseph Wilson {http://wilsonadventurephotography.com}";
    
    
    exif_bytes = piexif.dump(exif_dict)
    
    writeOnImage("@jojo", image);
    image.save(OUTPUT_PATH + "\\" + file, quality=100, subsampling=0, exif=exif_bytes);
    size = 1024,1024
    image.thumbnail(size)
    image.save(OUTPUT_PATH + "\\" + file + ".thumb.jpg", quality=100, subsampling=0, exif=exif_bytes);
