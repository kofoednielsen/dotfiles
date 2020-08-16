from PIL import Image, ImageDraw, ImageFont


fontsize = 200
image = Image.new("RGBA", (1000, 1000), (255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("/usr/share/fonts/ubuntu/UbuntuMono-R.ttf", 50)
txt = "😞"
draw.text((10, 0), txt, (0, 0, 0), font=font)
image.save('emoji.png')
