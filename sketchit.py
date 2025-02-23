import cv2
import turtle
import numpy as np
import time
import argparse
import cv2

# Parser untuk command --gambar
parser = argparse.ArgumentParser(description='Menggambar sketsa gambar menggunakan turtle.')
parser.add_argument('--gambar', type=str, required=True, help='Path ke file gambar.')
args = parser.parse_args()

# Fungsi untuk menemukan jarak terdekat dari titik yang sudah digambar
def jarakDekat(p):
    if len(posisi) > 0:
        nodes = np.array(posisi)
        jarak = np.sum((nodes - p) ** 2, axis=1)
        i_min = np.argmin(jarak)
        return posisi[i_min]
    else:
        return None

def outline(gambar): #  Mencari tepi gambar / outline gambar
    srcGambar = cv2.imread(gambar, 0)
    ubahGambar = cv2.GaussianBlur(srcGambar, (7, 7), 0)
    th3 = cv2.adaptiveThreshold(
        ubahGambar, maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY, blockSize=9, C=2
    )
    return th3

gambar = args.gambar
im = cv2.imread(gambar, 0)
th3 = outline(gambar)

lebarGambar = im.shape[1]
tinggiGambar = im.shape[0]

CUTOFF_LEN = ((lebarGambar + tinggiGambar) / 2) / 60
iH, iW = np.where(th3 == [0])
iW = iW - lebarGambar / 2
iH = -1 * (iH - tinggiGambar / 2)
posisi = [list(iwh) for iwh in zip(iW, iH)]

t = turtle.Turtle()
t.color("black")
t.shapesize(1)
t.pencolor("black")

t.speed(1000)
turtle.tracer(0, 0)
t.penup()
t.goto(posisi[0])
t.pendown()

time.sleep(3)

p = posisi[0]
while p:
    p = jarakDekat(p)
    if p:
        current_pos = np.asarray(t.pos())
        new_pos = np.asarray(p)
        length = np.linalg.norm(new_pos - current_pos)
        if length < CUTOFF_LEN:
            t.goto(p)
            turtle.update()
        else:
            t.penup()
            t.goto(p)
            t.pendown()
        posisi.remove(p)
    else:
        p = None

time.sleep(3)
turtle.penup()
turtle.done()
