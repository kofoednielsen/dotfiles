from PIL import Image, ImageDraw, ImageFont


fontsize = 10
image = Image.new("RGBA", (1000, 1000), (255, 255, 255))
draw = ImageDraw.Draw(image)
txt = "😞"
font = ImageFont.truetype("/usr/share/fonts/twemoji/twemoji.ttf", 50)
draw.text((10, 0), txt, (0, 0, 0), font=font)
image.save('emoji.png')
