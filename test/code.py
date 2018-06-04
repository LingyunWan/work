from PIL import Image, ImageFont, ImageDraw
from PIL import Image
# import ImageFilter,ImageDraw,ImageFont
import random

width = 1000
height = 40
# ImageFont.truetype()是选择字体(用于打印验证码的字体)
font = ImageFont.truetype('arial.ttf', 28)
image = Image.new("RGB", (width,height),(0,0,0))
draw = ImageDraw.Draw(image)
for i in range(9):
    # print(i)'random.randint(0,9)',
    # 第一个参数代表位置，带二个代表内容，第三个代表字体，第四个代表字体颜色
    # 打印的字体的宽,字体间隔;字体打印的范围;验证码所使用的字体;字体颜色
    # draw.text((20*i, 10), str(random.randint(0, 9)), font=font, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw.text((20*i, 10), str(random.randint(0, 9)), font=font, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    # print(i)
image.show()
