from PIL import Image
import numpy as np


def get_bit_stream(message, index):
    return format(ord(message[index]), '08b')


def get_bits(bit_stream, ind):
    # print bit_stream
    if ind == 6:
        last = 0
    else:
        last = int(bit_stream[ind + 2])

    return int(bit_stream[ind]), int(bit_stream[ind + 1]), last


def change_bits(r, g, b, bits, flag=False):
    """

    :type bits: Integer array
    """
    if bits[0]:
        r = r | bits[0]
    else:
        # print "R before", r
        r &= 0b11111110
        # print "R after", r
    if bits[1]:
        g = g | bits[1]
    else:
        g &= 0b11111110

    if not flag:
        if bits[2]:
            b |= bits[2]
        else:
            b &= 0b11111110
    return r, g, b


def append_to_message(pic, img_index):
    r1, g1, b1 = pic[img_index], pic[img_index + 1], pic[img_index + 2]
    r2, g2, b2 = pic[img_index + 3], pic[img_index + 4], pic[img_index + 5]
    r3, g3, b3 = pic[img_index + 6], pic[img_index + 7], pic[img_index + 8]
    char = ""
    char += str(r1 & 0x00000001)
    char += str(g1 & 0x00000001)
    char += str(b1 & 0x00000001)
    char += str(r2 & 0x00000001)
    char += str(g2 & 0x00000001)
    char += str(b2 & 0x00000001)
    char += str(r3 & 0x00000001)
    char += str(g3 & 0x00000001)
    return char


def reshape(pic, w, h):
    pic = np.resize(pic, (pic.size / 3, 3))
    pic = pic.reshape((h, w, 3))
    img_copy = Image.fromarray(pic)
    return img_copy


def encrypt(image, message):
    img = Image.open(image)
    width, height = img.size
    msg_index = 0
    pic = (np.array(img))
    pic = pic.flatten()

    l = len(message)
    bits_l = format(l, '024b')
    pic[-1] = int(bits_l[16:24], 2)
    pic[-2] = int(bits_l[8:16], 2)
    pic[-3] = int(bits_l[0:8], 2)

    for img_index in range(0, pic.size, 9):
        if msg_index == len(message):
            img_copy = reshape(pic, width, height)
            return img_copy

        r1, g1, b1 = pic[img_index], pic[img_index + 1], pic[img_index + 2]
        r2, g2, b2 = pic[img_index + 3], pic[img_index + 4], pic[img_index + 5]
        r3, g3, b3 = pic[img_index + 6], pic[img_index + 7], pic[img_index + 8]
        bit_stream = get_bit_stream(message, msg_index)
        counter = 0
        for ind in range(0, 8, 3):
            bits = get_bits(bit_stream, ind)
            if counter == 0:
                # print "R1 before", r1
                r1, g1, b1 = change_bits(r1, g1, b1, bits)
                # print "R1 after", r1

                pic[img_index], pic[img_index + 1], pic[img_index + 2] = r1, g1, b1

            elif counter == 1:
                r2, g2, b2 = change_bits(r2, g2, b2, bits)
                pic[img_index + 3], pic[img_index + 4], pic[img_index + 5] = r2, g2, b2

            elif counter == 2:
                r3, g3, b3 = change_bits(r3, g3, b3, bits, True)
                pic[img_index + 6], pic[img_index + 7], pic[img_index + 8] = r3, g3, b3

            else:
                print "Dude WTF!"
            counter += 1
        msg_index += 1

    return None


def decode(image):
    img = Image.open(image)
    msg_index = 0
    msg = ""
    pic = (np.array(img))
    # print pic
    pic = pic.flatten()
    length = get_msg_len(pic[-3:])
    print length
    for img_index in range(0, pic.size, 9):
        if msg_index == length:
            return msg
        char = append_to_message(pic, img_index)
        msg += str(chr(int(char, 2)))
        msg_index += 1


def get_msg_len(pix):
    s = ""
    for i in xrange(0, 3):
        s += format(pix[i], '08b')
    return int(s, 2)
