from PIL import Image, ImageChops
import numpy as np
import os
import math
import sys


def is_row_background(img, size, y, bg_color=(255, 255, 255), tolerance=230):
    for x in range(0, size[0]):
        px_color = img.getpixel((x, y))
        diff = max([abs(px_color[0] - bg_color[0]), abs(px_color[1] - bg_color[1]), abs(px_color[2] - bg_color[2])])
        if diff > tolerance:
            return False
    return True


def first_nonwhitespace_row(img, size, startrow=0, bg_color=(255,255,255)):
    for y in range(startrow, size[1]):
        if not is_row_background(img, size, y, bg_color):
            return y
    return -1


def first_whitespace_row(img, size, startrow=0, bg_color=(255,255,255)):
    for y in range(startrow, size[1]):
        if is_row_background(img, size, y, bg_color):
            return y
    return -1


def extract(img):
    segments = []
    row = 0
    #arr = np.array(img)
    size = img.size
    while row < img.size[1]:
        start = first_nonwhitespace_row(img, size, row)
        if start == -1:
            break
        end = first_whitespace_row(img, size, start)
        if end == -1:
            end = img.size[1]
        segments.append(img.crop((0, start, img.size[0], end)))
        row = end
    return segments


def sort_key(fname: str) -> int:
    return int(fname.split('-')[1].split('.')[0])

def sort_key_comment(fname: str) -> int:
    return int(fname[1:].split('.')[0])

def extract_all():
    files = sorted(os.listdir('./imgs'), key=sort_key)
    comments = []
    for f in files:
        print('Extracting from ' + f + ': ', end="")
        sys.stdout.flush()
        img = Image.open('imgs/' + f)
        extracted = extract(img)
        comments.extend(extracted)
        img.close()
        print('[Found ' + str(len(extracted)) + ']   So far: ' + str(len(comments)))
    return comments


def save_all(comments):
    for (i, comment) in enumerate(comments):
        print('Saving comment A' + str(i + 1))
        comment.save('comments/A' + str(i + 1) + '.jpg', 'JPEG')


def rename_from(num: int):
    files = sorted(os.listdir('./comments'), key=sort_key_comment)
    highest = sort_key_comment(files[-1])
    for i in range(highest, num - 1, -1):
        print(f'Renaming comments/A{i}.jpg to comments/A{i+1}.jpg')
        os.rename(f'comments/A{i}.jpg', f'comments/A{i+1}.jpg')

def rename_from_down(num: int):
    files = sorted(os.listdir('./comments'), key=sort_key_comment)
    highest = sort_key_comment(files[-1])
    for i in range(num, highest + 1, 1):
        print(f'Renaming comments/A{i}.jpg to comments/A{i-1}.jpg')
        os.rename(f'comments/A{i}.jpg', f'comments/A{i-1}.jpg')

if __name__ == '__main__':
    save_all(extract_all())
