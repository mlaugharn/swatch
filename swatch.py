import mahotas
import argparse


def trunctriple(triple, resolution):
    return [(singleton // resolution) * resolution for singleton in triple]


def tally_colors(image, resolution):
    output = {}
    height = len(image)
    width = len(image[0])
    for y in range(height):
        for x in range(width):
            # no alpha values please
            pixel = tuple(trunctriple(image[y][x][:3], resolution))
            if pixel in output:
                output[pixel] += 1
            else:
                output[pixel] = 1
    return output


def max_key(unsortedDictionary):
    values = list(unsortedDictionary.values())
    keys = list(unsortedDictionary.keys())
    return keys[values.index(max(values))]


def max_n_times(dictionary, n):
    output = []
    tempdict = dictionary.copy()
    for _ in range(n):
        if len(tempdict) == 0:
            raise IndexError("There aren't " + str(numColors) + " reduced colors in the specified image. Reduce -n and/or -r.")
        key = max_key(tempdict)
        output.append(key)
        tempdict.pop(key)
    return output


def saturation(triple):
    return color_distance(triple, [avg(triple)] * 3)


def color_distance(triple1, triple2):
    dr, dg, db = [triple2[val] - triple1[val] for val in range(3)]
    return (dr ** 2 + dg ** 2 + db ** 2) ** (1 / 2)


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def avg(iterable):
    return sum(iterable) / len(iterable)


def theme_cycle_colors():
    index = 0
    themecopy = open(template).read()
    print("Populating theme with colors...")
    if not args.unique:
        while "<colorful>" in themecopy:
            themecopy = themecopy.replace("<colorful>", rgb_to_hex(highlights[index]), 1)
            index = (index + 1) % len(highlights)
    else:
        while "<colorful>" in themecopy and index < len(highlights):
            themecopy = themecopy.replace("<colorful>", rgb_to_hex(highlights[index]), 1)
            index += 1
    outname = args.image + '.tmTheme'
    open(outname, 'w').write(themecopy)
    print("Theme written to " + outname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A tool to generate Textmate/Sublime Text themes from images.")
    parser.add_argument("image", action="store", type=str, help="The image to extract colors from.")
    parser.add_argument("--light", action="store_true", default=False, help="Switch to light-background color scheme.")
    parser.add_argument("-r", action="store", type=int, default=64, help="Reduction of RGB colors. A reduction of 64 rounds RGB values to the nearest multiple of 64.")
    parser.add_argument("-n", action="store", type=int, default=10, help="Number of reduced colors to choose from.")
    parser.add_argument("-c", action="store", type=int, default=128, help="Minimum contrast between background and colors. 255 is the contrast between black and white.")
    parser.add_argument("--unique", action="store_true", default=False, help="Use each color only once.")
    args = parser.parse_args()
    template = 'tomorrow-dark-base'
    background = (29, 31, 33)
    if args.light:
        template = 'tomorrow-light-base'
        background = (255, 255, 255)
    print("Attempting to read image...")
    imageArray = mahotas.imread(args.image).astype('uint8').tolist()
    # imageArray = mahotas.imread(args.image).astype('uint8').tolist()
    print("Image read. Attempting to reduce and tally colors...")
    # imageArray = mahotas.imresize(image, 1).tolist()
    talliedColors = tally_colors(imageArray, int(args.r))
    print("Colors reduced and tallied. Finding the " + str(args.n) + " most prevalent colors...")
    numColors = int(args.n)
    maxes = max_n_times(talliedColors, numColors)
    saturations = dict(zip(maxes, [saturation(color) for color in maxes]))
    highlights = list(filter(lambda color: color_distance(color, background) > int(args.c), max_n_times(saturations, int(numColors / 2))))
    lowlights = [color for color in saturations if color not in highlights]
    theme_cycle_colors()
