# -*- coding: utf-8 -*-
"""
donut arc-enciel :
"""

import moviepy.video.io.ImageSequenceClip
import numpy as np
from PIL import Image
import os

k = int(input("coefficient de variation de couleur >>> "))
etape = int(input("étape 1, 2, 3 ou 4 ?? >>> "))

R = 50
r = 20

hauteur = 300
largeur = 300

Lx = 0
Ly = 0
Lz = -1

alphabet = 'abcdefghijklmnopqrstuvwxyz'

rouge = 14
vert = 248
bleu = 244


def rouge(x):
    x = x % 1530
    if x < 255 or x >= 510 and x >= 1020 and x > 1275:
        return 255
    elif x < 510:
        return 510 - x
    elif x < 1020:
        return 0
    else:
        return x - 1020


def vert(x):
    x = x % 1530
    if x < 255:
        return 127.5 + x / 2
    elif x < 765:
        return 255
    elif x < 1020:
        return 1020 - x + (x % 765) / 2
    else:
        return 127.5


def bleu(x):
    x = x % 1530
    if x < 510:
        return 0
    elif x < 765:
        return x - 510
    elif x <= 1275:
        return 255
    else:
        return 1530 - x


if etape == 1:
    depart = 0
    arrive = np.pi / 2
    x = 0
    name = "A_"
elif etape == 2:
    depart = np.pi / 2
    arrive = np.pi
    x = 382.5 * k / 4
    name = "B_"
elif etape == 3:
    depart = np.pi
    arrive = 3 * np.pi / 2
    x = 765 * k / 4
    name = "C_"
else:
    depart = 3 * np.pi / 2
    arrive = 2 * np.pi
    x = 1147.5 * k / 4
    name = "D_"

rotation_en_x = np.arange(depart, arrive, np.pi / 190)
rotation_en_y = np.zeros(rotation_en_x.shape)
rotation_en_z = rotation_en_x

c_xs, s_xs = np.cos(rotation_en_x), np.sin(rotation_en_x)
c_ys, s_ys = np.cos(rotation_en_y), np.sin(rotation_en_y)
c_zs, s_zs = np.cos(rotation_en_z), np.sin(rotation_en_z)

theta = np.arange(0, 2 * np.pi, np.pi / 500)
c_xt, s_xt = np.cos(theta), np.sin(theta)

alpha = np.arange(0, 2 * np.pi, np.pi / 300)
c_xa, s_xa = np.cos(alpha), np.sin(alpha)

matrice_image = np.empty((hauteur, largeur, 3), dtype=np.uint8)
matrice_image_bis = np.empty((hauteur, largeur), dtype=float)

Z_R_center = 0
step = 0
for i, (c_x, s_x, c_y, s_y, c_z, s_z) in enumerate(zip(c_xs, s_xs, c_ys, s_ys, c_zs, s_zs)):
    matrice_image[:] = 0
    matrice_image_bis[:] = -np.inf

    print(i)
    Y_R_center = R * s_xt
    X_R_center = R * c_xt
    ZZ_R_center = Y_R_center * s_x + Z_R_center * c_x
    YY_R_center = Y_R_center * c_x - Z_R_center * s_x
    XX_R_center = X_R_center
    ZZZ_R_center = ZZ_R_center * c_y - XX_R_center * s_y
    YYY_R_center = YY_R_center
    XXX_R_center = ZZ_R_center * s_y + XX_R_center * c_y
    z_R_center = ZZZ_R_center
    y_R_center = XXX_R_center * s_z + YYY_R_center * c_z
    x_R_center = XXX_R_center * c_z - YYY_R_center * s_z

    Zs = r * s_xa
    Ys = (R + r * c_xa[None, :]) * s_xt[:, None]
    Xs = (R + r * c_xa[None, :]) * c_xt[:, None]
    ZZs = Ys * s_x + Zs * c_x
    YYs = Ys * c_x - Zs * s_x
    XXs = Xs
    ZZZs = ZZs * c_y - XXs * s_y
    YYYs = YYs
    XXXs = ZZs * s_y + XXs * c_y
    zs = ZZZs
    ys = XXXs * s_z + YYYs * c_z
    xs = XXXs * c_z - YYYs * s_z
    zs_norm = zs - z_R_center[:, None]
    ys_norm = ys - y_R_center[:, None]
    xs_norm = xs - x_R_center[:, None]

    produit_scalaire = ((Lx * xs_norm + Ly * ys_norm + Lz * zs_norm) / (
                np.sqrt(zs_norm ** 2 + ys_norm ** 2 + xs_norm ** 2) * np.sqrt(Lx ** 2 + Ly ** 2 + Lz ** 2))).flatten()

    coord_y = (hauteur // 2 - ys.astype(int)).flatten()
    coord_x = (largeur // 2 + xs.astype(int)).flatten()
    zs = zs.flatten()

    mask, = np.where(matrice_image_bis[coord_y, coord_x] < zs)

    print(len(mask))
    x += int(k)
    while len(mask):
        matrice_image[coord_y[mask], coord_x[mask], 0] = np.where(produit_scalaire[mask] < 0,
                                                                  rouge(x) * np.abs(produit_scalaire[mask]), 0)
        matrice_image[coord_y[mask], coord_x[mask], 1] = np.where(produit_scalaire[mask] < 0,
                                                                  vert(x) * np.abs(produit_scalaire[mask]), 0)
        matrice_image[coord_y[mask], coord_x[mask], 2] = np.where(produit_scalaire[mask] < 0,
                                                                  bleu(x) * np.abs(produit_scalaire[mask]), 0)
        matrice_image_bis[coord_y[mask], coord_x[mask]] = zs[mask]
        mask, = np.where(matrice_image_bis[coord_y, coord_x] < zs)
        # print(len(mask))

    step = step + 1
    im = Image.fromarray(matrice_image, 'RGB')
    im = im.convert('RGB')
    im.save(
        (
            (
                (
                    (
                        (
                            (
                                f"D:/Léo/Informatique/simulation/image/donut{name}"
                                + alphabet[
                                    ((((step // 26) // 26) // 26) // 26)
                                ]
                                + alphabet[(((step // 26) // 26) // 26) // 26]
                            )
                            + alphabet[((step // 26) // 26) // 26]
                        )
                        + alphabet[(step // 26) // 26]
                    )
                    + alphabet[step // 26]
                )
                + alphabet[step % 26]
            )
            + ".png"
        )
    )


image_folder = 'D:/Léo/Informatique/simulation/image'
fps = 30

image_files = [
    f'{image_folder}/{img}'
    for img in os.listdir(image_folder)
    if img.endswith(".png")
]

print(image_files)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('D:/Léo/Informatique/simulation/video/my_couleur.mp4')

"""for image in image_files:
    os.remove(image)"""
