import moviepy.video.io.ImageSequenceClip
import numpy as np
from PIL import Image
from math import sin, cos
import os
import math
import random
from Snippets.snippet import Snippet

R = 250
r = 100

hauteur = 1000
largeur = 1000

alphabet = 'abcdefghijklmnopqrstuvwxyz'

rouge = 0
bleu = 0
vert = 0

Lx, Ly, Lz = -1, 0, 0


step = 0

matrice_image = np.empty((hauteur, largeur, 3), dtype=np.uint8)
matrice_image_bis = np.empty((hauteur, largeur), dtype=float)
rotation_en_y = 0
Z_R_center = 0
for rotation_en_x in np.arange(0, math.pi * 3, math.pi / 100):
    rotation_en_z = rotation_en_x

    matrice_image[:] = 0
    matrice_image_bis[:] = -np.inf
    for theta in np.arange(0, 2 * math.pi, math.pi / 1500):
        for alpha in np.arange(0, 2 * math.pi, math.pi / 800):
            Y_R_center = R * sin(theta)
            X_R_center = R * cos(theta)
            Z = r * sin(alpha)
            Y = (R + r * cos(alpha)) * cos(theta)
            X = (R + r * cos(alpha)) * sin(theta)
            ZZ = Y * sin(rotation_en_x % math.pi) + Z * cos(rotation_en_x % math.pi)
            YY = Y * cos(rotation_en_x % math.pi) - Z * sin(rotation_en_x % math.pi)
            XX = X
            ZZZ = ZZ * cos(rotation_en_y % math.pi) - XX * sin(rotation_en_y % math.pi)
            YYY = YY
            XXX = ZZ * sin(rotation_en_y % math.pi) + XX * cos(rotation_en_y % math.pi)
            z = ZZZ
            y = XXX * sin(rotation_en_z) + YYY * cos(rotation_en_z)
            x = XXX * cos(rotation_en_z) - YYY * sin(rotation_en_z)

            ZZ_R_center = Y_R_center * sin(rotation_en_x % math.pi) + Z_R_center * cos(rotation_en_x % math.pi)
            YY_R_center = Y_R_center * cos(rotation_en_x % math.pi) - Z_R_center * sin(rotation_en_x % math.pi)
            XX_R_center = X_R_center
            ZZZ_R_center = ZZ_R_center * cos(rotation_en_y % math.pi) - XX_R_center * sin(rotation_en_y % math.pi)
            YYY_R_center = YY_R_center
            XXX_R_center = ZZ_R_center * sin(rotation_en_y % math.pi) + XX_R_center * cos(rotation_en_y % math.pi)
            z_R_center = ZZZ_R_center
            y_R_center = XXX_R_center * sin(rotation_en_z) + YYY_R_center * cos(rotation_en_z)
            x_R_center = XXX_R_center * cos(rotation_en_z) - YYY_R_center * sin(rotation_en_z)

            z_norm = z - z_R_center
            y_norm = y - y_R_center
            x_norm = x - x_R_center

            # print(math.sqrt(x_norm**2 + y_norm**2 + z_norm**2))
            #produit_scalaire = abs(-z_norm)
            # print(z_norm,y_norm,x_norm)
            p_s = ((Lx * x_norm + Ly * y_norm + Lz * z_norm) / (
                np.sqrt((z_norm ** 2 + y_norm ** 2 + x_norm ** 2) * (
                        Lx ** 2 + Ly ** 2 + Lz ** 2))))

            rouge, vert, bleu = Snippet.couleur(True, 2*int(z))
            if matrice_image_bis[hauteur // 2 - int(y), largeur // 2 + int(x)] <= z:
                matrice_image[hauteur // 2 - int(y), largeur // 2 + int(x), 0] = rouge * np.abs(p_s)  # rouge
                matrice_image[hauteur // 2 - int(y), largeur // 2 + int(x), 1] = vert * np.abs(p_s)  # vert
                matrice_image[hauteur // 2 - int(y), largeur // 2 + int(x), 2] = bleu * np.abs(p_s)  # bleu
                matrice_image_bis[hauteur // 2 - int(y), largeur // 2 + int(x)] = z

    step = step + 1
    print(step)
    im = Image.fromarray(matrice_image, 'RGB')
    im = im.convert('RGB')
    im.save("C:/Leo/Informatique/Projets/Donut/image/donut" + alphabet[(step // 26) // 26] + alphabet[step // 26] +
            alphabet[step % 26] + ".png")

image_folder = 'C:/Leo/Informatique/Projets/Donut/image'
fps = 30

image_files = [
    f'{image_folder}/{img}'
    for img in os.listdir(image_folder)
    if img.endswith(".png")
]

print(image_files)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('C:/Leo/Informatique/Projets/Donut/image/my_video.mp4')
