import sys
import time
import moviepy.video.io.ImageSequenceClip
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
from Snippets.snippet import Snippet

class Donut:
    def __init__(self, film):
        self.hauteur = 2160
        self.largeur = 3440
        self.Rayon = 500
        self.rayon = 200
        self.Lx, self.Ly, self.Lz = -1, 0, -3  # vecteur lumière
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.image_folder = 'D:/Leo/Informatique/Python/SimulatingThings/Donut/image'
        self.video_folder = "D:/Leo/Informatique/Python/SimulatingThings/Donut/video/"
        self.fps = 60
        self.frame = 'donut'  # nom racine des images
        self.film = film  # nom de la video
        self.pas = np.pi / 400
        self.pas_theta = np.pi / 2500
        self.pas_alpha = np.pi / 1000
        self.var_color = 1530 / (2 * np.pi / self.pas)  # coef de variation de couleur

    def donut(self, start, stop, coef, name='donut'):
        rotation_en_x = np.arange(start, stop, self.pas)
        rotation_en_y = np.zeros(rotation_en_x.shape)

        c_xs, s_xs = np.cos(rotation_en_x), np.sin(rotation_en_x)
        c_ys, s_ys = np.cos(rotation_en_y), np.sin(rotation_en_y)
        c_zs, s_zs = np.cos(rotation_en_x), np.sin(rotation_en_x)

        theta = np.arange(0, 2 * np.pi, self.pas_theta)
        c_xt, s_xt = np.cos(theta), np.sin(theta)

        alpha = np.arange(0, 2 * np.pi, self.pas_alpha)
        c_xa, s_xa = np.cos(alpha), np.sin(alpha)

        matrice_image = np.empty((self.hauteur, self.largeur, 3), dtype=np.uint8)
        matrice_image_bis = np.empty((self.hauteur, self.largeur), dtype=float)

        bar = tqdm(total=int(((2 * np.pi) / self.pas) / 9), desc='Progress')

        Z_R_center, Y_R_center, X_R_center = 0, self.Rayon * s_xt, self.Rayon * c_xt
        Zs = self.rayon * s_xa
        Ys = (self.Rayon + self.rayon * c_xa[None, :]) * s_xt[:, None]
        Xs = (self.Rayon + self.rayon * c_xa[None, :]) * c_xt[:, None]

        for step, (c_x, s_x, c_y, s_y, c_z, s_z) in enumerate(zip(c_xs, s_xs, c_ys, s_ys, c_zs, s_zs)):
            # start = time.time()
            matrice_image[:] = 0
            matrice_image_bis[:] = -np.inf

            # grand cercle
            ZZ_R_center = Y_R_center * s_x + Z_R_center * c_x
            YY_R_center = Y_R_center * c_x - Z_R_center * s_x
            ZZZ_R_center = ZZ_R_center * c_y - X_R_center * s_y
            XXX_R_center = ZZ_R_center * s_y + X_R_center * c_y
            y_R_center = XXX_R_center * s_z + YY_R_center * c_z
            x_R_center = XXX_R_center * c_z - YY_R_center * s_z

            # petit cercle
            ZZs, YYs = Ys * s_x + Zs * c_x, Ys * c_x - Zs * s_x
            ZZZs, YYYs, XXXs = ZZs * c_y - Xs * s_y, YYs, ZZs * s_y + Xs * c_y
            zs, ys, xs = ZZZs, XXXs * s_z + YYYs * c_z, XXXs * c_z - YYYs * s_z
            zs_norm, ys_norm, xs_norm = zs - ZZZ_R_center[:, None], ys - y_R_center[:, None], xs - x_R_center[:, None]

            produit_scalaire = ((self.Lx * xs_norm + self.Ly * ys_norm + self.Lz * zs_norm) / (
                np.sqrt((zs_norm ** 2 + ys_norm ** 2 + xs_norm ** 2) * (
                        self.Lx ** 2 + self.Ly ** 2 + self.Lz ** 2)))).flatten()

            coord_y = (self.hauteur // 2 - ys.astype(int)).flatten()
            coord_x = (self.largeur // 2 + xs.astype(int)).flatten()

            zs = zs.flatten()
            try:
                mask, = np.where(matrice_image_bis[coord_y, coord_x] < zs)
            except Exception:
                return Exception

            coef += self.var_color
            rouge, vert, bleu = Snippet.couleur(True, coef)
            while len(mask):
                p_s = produit_scalaire[mask]
                coo_y, coo_x = coord_y[mask], coord_x[mask]
                matrice_image[coo_y, coo_x, 0] = np.where(p_s < 0, rouge * np.abs(p_s), 0)
                matrice_image[coo_y, coo_x, 1] = np.where(p_s < 0, vert * np.abs(p_s), 0)
                matrice_image[coo_y, coo_x, 2] = np.where(p_s < 0, bleu * np.abs(p_s), 0)
                matrice_image_bis[coo_y, coo_x] = zs[mask]
                mask, = np.where(matrice_image_bis[coord_y, coord_x] < zs)


            im = Image.fromarray(matrice_image, 'RGB')
            im = im.convert('RGB')
            im.save(
                f'{self.image_folder}/{name}{self.alphabet[step // 26 // 26 // 26 // 26]}{self.alphabet[step // 26 // 26 // 26 // 26]}{self.alphabet[step // 26 // 26 // 26]}{self.alphabet[step // 26 // 26]}{self.alphabet[step // 26]}{self.alphabet[step % 26]}.png'
            )

            # print(f"{str(time.time() - start)} secondes pour la création de l'image.")
            bar.update(1)

    def video(self):
        image_files = [f'{self.image_folder}/{img}' for img in os.listdir(self.image_folder) if img.endswith(".png")]

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=self.fps)
        clip.write_videofile(self.video_folder + self.film + '.mp4')

    def deletion(self):
        image_files = [f'{self.image_folder}/{img}' for img in os.listdir(self.image_folder) if img.endswith(".png")]

        for image in image_files:
            os.remove(image)

    def processing(self, step, etapes):
        nombre = (2 * np.pi) / self.pas
        depart = step * (2 * np.pi) / etapes
        arrive = (step + 1) * (2 * np.pi) / etapes
        coef = (nombre / etapes) * step * self.var_color
        name = f"donut_step{str(step + 1)}_"
        self.donut(depart, arrive, coef, name)


if __name__ == '__main__':
    donut = Donut('Video_donut_4k')
    debut = time.time()
    console = 1  # 1 à 3 pour les images, autre chose pour la vidéo
    if console == 1:
        donut.processing(9, 9)
        donut.processing(1, 9)
        donut.processing(3, 9)
    elif console == 2:
        donut.processing(2, 9)
        donut.processing(4, 9)
        donut.processing(6, 9)
    elif console == 3:
        donut.processing(5, 9)
        donut.processing(7, 9)
        donut.processing(8, 9)
    else:
        donut.video()
        donut.deletion()
    print(f'{str(time.time() - debut)}secondes')
    print("finit")
    sys.exit()
