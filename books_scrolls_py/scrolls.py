import math
from PIL import Image

def read_tha_books():
    """
    Analyse books from daScrolls.csv file. Count each of the type.
    :return: List of tuples in format [(type_of_book1, count1), (type_of_book2, count2)..]
    """
    #  Works properly, dictionary part is similar to next function.
    #  Analyse the book types and their count
    books = []
    with open("daScrolls.csv", "r") as book_file:
        lines = book_file.readlines()
        for line in lines:
            row = line.split(";")
            books.append(row[1])

    #  Dictionary with book types, counts how many books have the type.
    dic = {}
    for i in range(len(books)):
        if books[i] in dic:
            dic[books[i]] += 1
        else:
            dic[books[i]] = 1
    dic["Other"] = dic.pop("")
    return list(dic.items())


def analyze_sum_skillz():
    """
    Analyse 'Skill Book' type and 'Spell Tome' type books. Prints graph which visualize count of the books.
    Example of the graph:
    skill tree  count
    conjuration ########################################################
    destruction ###########################################
    speech      ####################
    sneak       ###

    :return: dictionary, where key is the name of the skill tree which is upgraded by the book, value is its count.
    """
    #  Analyse the scrolls and choose the right types of them.
    #  Add the skillz to the list.
    skillz = []
    with open("daScrolls.csv", "r") as book_file:
        lines = book_file.readlines()
        for line in lines:
            row = line.split(";")
            if row[1] == "Skill Book" or row[1] == "Spell Tome":
                if row[2] != "":
                    skillz.append(row[2])

    wanna_cry = {}
    for i in range(len(skillz)):
        skillz[i] = skillz[i].replace("\n", "")
        if skillz[i] in wanna_cry:
            wanna_cry[skillz[i]] += 1
        else:
            wanna_cry[skillz[i]] = 1

    #  Sorts it to make it looks noice.
    sorted_crying = sorted(wanna_cry, key=lambda x: wanna_cry[x], reverse=True)
    for k in sorted_crying:
        print(k.ljust(12, " "), "#" * wanna_cry[k])

    return wanna_cry


def inscribe_dha_scroll(background, text):
    """
    Insert the text into background. Both images have the same size.
    :param background: image of the background
    :param text: image of the text
    :return: merged image
    """
    scroll = Image.open(background).convert("RGBA")
    text = Image.open(text).convert("RGBA")

    data = text.getdata()
    new_data = []
    for pixels in data:
        if pixels[0] == 255 and pixels[1] == 255 and pixels[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(pixels)
    text.putdata(new_data)
    scroll.paste(text, text)
    scroll.save("complete_scroll.png")
    return scroll


def cover_trackz(mightyFrekINGSrulz):
    """
    Blurs the input image
    :param mightyFrekINGSrulz: image
    :return: blurred image
    """
    # I use the new image complete_scroll.png
    image = Image.open(mightyFrekINGSrulz).convert("RGB")
    width, height = image.size
    for h in range(height):
        for w in range(width):
            image.putpixel((w, h), get_average_value(w, h, image))
    image.show()


# Makes the magic called blur happen by using average values of pixels thanks to matrices.
def get_average_value(width, height, image):
    width_total, height_total = image.size
    r_sum, g_sum, b_sum = 0, 0, 0
    for i in range(4):
        for j in range(4):
            w = min(max(width - j, 0), width)
            h = min(max(height - i, 0), height)
            r, g, b = image.getpixel((w, h))
            r_sum += r
            g_sum += g
            b_sum += b
    return (r_sum // 16, g_sum // 16, b_sum // 16)

# Interface of the turtle implementation is up to you
#UNDONE

WIDTH, HEIGHT = 1000, 1000

def svg_made(lines, color="black", width=1):
    #  Returns lines.

    svg_lines = ""
    s = '<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:{}; stroke-width:{}" />'
    for x1, y1, x2, y2 in lines:
        svg_lines += s.format(x1, y1, x2, y2,
                              color, width)
    return svg_lines

class Turtle:
    def __init__(self, color="black", width=1):
        self.x = 0
        self.y = 0
        self.heading = 0
        self.lines = []
        self.color = color
        self.width = width

    def right(self, angle):
        self.heading = (self.heading + angle) % 360

    def left(self, angle):
        self.heading = (self.heading - angle) % 360

    def forward(self, d, cry=False):
        #  move forward by distance d
        #  if cry is True don't display the line

        nx = round(self.x + d * math.cos(self.heading * math.pi / 180), 2)
        ny = round(self.y + d * math.sin(self.heading * math.pi / 180), 2)

        if not cry:
            self.lines.append((WIDTH / 2 + self.x, HEIGHT / 2 + self.y,
                               WIDTH / 2 + nx, HEIGHT / 2 + ny))

        self.x, self.y = nx, ny

    def move(self, x, y):
        self.x, self.y = x, y

    def svg_made(self):
        #  return  lines

        return getsvg(self.lines, self.color, self.width)



#testing
# inscribe_dha_scroll("scroll.png", "text.png")
# cover_trackz("complete_scroll.png")
# print(read_tha_books())
# print(analyze_sum_skillz())
