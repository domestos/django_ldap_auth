import os
import pyqrcode

from config.settings import STATICFILES_DIRS
from PIL import Image, ImageDraw, ImageFont

def run_qr_gen(item):
    s_number = item.inventory_number
    qp = pyqrcode.create(str(s_number))
    path  =  os.path.join(STATICFILES_DIRS[0]+"/equipment/qr_code/temp/", str(s_number).replace("/", "-").replace(" ", "-")+".png")
    qp.png(path, scale=8)



def run_generate_qr_code(items):
    print('QR-code Generate ')
    for item in items:
        s_number  = item.inventory_number
        qp=pyqrcode.create(s_number)
        print (s_number)
        path = os.path.join(STATICFILES_DIRS[0]+"/equipment/qr_code/temp/",str(item.id)+'.png')
        print('path2 '+path )
        # txt = qp.terminal()
        # print(txt)
       # qp.svg(path, scale=8)
        qp.png(path, scale=8)


        #Adds caption
        # img=Image.open(path)
        # width,height = img.size
        #
        # print("width = "+ str(width))
        # print("height = "+ str(round(height+(height/2)+20)))
        # bi=Image.new("RGBA", (width+25, round(height+(height/2)+20)),"white")
        # bi.paste(img,(5,0,(width+5),(height+0)))
        #
        #
        # draw=ImageDraw.Draw(bi)
        # font_number = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",20)
        # w,h= font_number.getsize(s_number)
        # draw.text((50 ,100 ),  s_number, font=font_number, fill="black")
        #
        # img.save(os.path.join(STATICFILES_DIRS, s_number.replace("/", "-")+'_.png'))


        # img = Image.open(path)
        # width,height = img.size

        # bi=Image.new("RGBA", (width+15, round(height+(height/4))),"white")
        # bi.paste(img,(5,0,(width+5),(height+0)))

        # font_number = ImageFont.truetype("arial.ttf",20)
        # #/usr/share/fonts/truetype/freefont/FreeMono.ttf
        # font = ImageFont.truetype("arial.ttf",18)
        # #font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",17)
        # w,h= font.getsize(s_number)

        # draw = ImageDraw.Draw(bi)
        # # draw.text(((width-w)/4,(height+((height/50)-h)/5)),  s_number, font=font_number, fill="black")
        # draw.text(((width-w)/4, height-h+3),  s_number, font=font_number, fill="black")

        # bi.save(os.path.join(STATICFILES_DIRS[0]+"/equipment/qr_code/", s_number.replace("/", "-").replace(" ", "-")+'.png'))
