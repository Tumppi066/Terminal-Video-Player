def rgbTo8bit(rgb):
    red = int((rgb[0] * 8) / 256)
    green = int((rgb[1] * 8) / 256)
    blue = int((rgb[2] * 4) / 256)

    return (red << 5) | (green << 2) | blue

print(rgbTo8bit((145, 23, 56)))