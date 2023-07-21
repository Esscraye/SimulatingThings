import sys
import time
import moviepy.video.io.ImageSequenceClip
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
from multiprocessing import Pool

class Snippet:
    @staticmethod
    def couleur(degrade, coefficient=0):
        if not degrade:
            return 14, 248, 244
        coefficient = coefficient % 1530

        if coefficient < 255:
            rouge, vert, bleu = 255, 127.5 + coefficient / 2, 0
        elif coefficient < 510:
            rouge, vert, bleu = 510 - coefficient, 255, 0
        elif coefficient < 765:
            rouge, vert, bleu = 0, 255, coefficient - 510
        elif coefficient < 1020:
            rouge, vert, bleu = 0, 1020 - coefficient + (coefficient % 765) / 2, 255
        elif coefficient <= 1275:
            rouge, vert, bleu = coefficient - 1020, 127.5, 255
        else:
            rouge, vert, bleu = 255, 127.5, 1530 - coefficient
        return rouge, vert, bleu

class Donut:
    def __init__(self, film):
        self.pixel = 740
        self.ratio = 16/9

        self.hauteur = self.pixel
        self.largeur = int(self.pixel * self.ratio)
        self.Rayon = self.pixel / 5
        self.rayon = self.Rayon / 2.5
        self.pas_theta = np.arctan(np.sqrt(2) / (2 * (self.Rayon + self.rayon)))
        self.pas_alpha = 1.5 * np.arctan(1 / (2 * self.rayon))

        self.Lx, self.Ly, self.Lz = -1, 0, -6  # vecteur lumière
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.image_folder = 'D:/Leo/Informatique/Python/SimulatingThings/Donut/image'
        self.video_folder = "D:/Leo/Informatique/Python/SimulatingThings/Donut/video/"
        self.fps = 30
        self.frame = 'donut'  # nom racine des images
        self.film = film  # nom de la video
        self.pas = np.pi / 200
        self.var_color = 1530 / (2 * np.pi / self.pas)  # coef de variation de couleur

    def donut(self, start, stop, coef, name='donut'):
        rotation_en_x = np.arange(start, stop, self.pas)
        rotation_en_y = np.zeros(rotation_en_x.shape)
        rotation_en_z = np.arange(start, stop, self.pas)

        c_xs, s_xs = np.cos(rotation_en_x), np.sin(rotation_en_x)
        c_ys, s_ys = np.cos(rotation_en_y), np.sin(rotation_en_y)
        c_zs, s_zs = np.cos(rotation_en_z), np.sin(rotation_en_z)

        theta = np.arange(0, 2 * np.pi, self.pas_theta)
        c_xt, s_xt = np.cos(theta), np.sin(theta)

        alpha = np.arange(0, 2 * np.pi, self.pas_alpha)
        c_xa, s_xa = np.cos(alpha), np.sin(alpha)

        matrice_image = np.empty((self.hauteur, self.largeur, 3), dtype=np.uint8)
        matrice_image_bis = np.empty((self.hauteur, self.largeur), dtype=float)

        bar = tqdm(total=int(((2 * np.pi) / self.pas) / 9), desc='Progress')

        Z_R_center, Y_R_center, X_R_center = 0, self.Rayon * s_xt, self.Rayon/2 * c_xt
        Zs = self.rayon * s_xa
        Ys = (self.Rayon + self.rayon * c_xa[None, :]) * s_xt[:, None]
        Xs = (self.Rayon + self.rayon * c_xa[None, :]) * c_xt[:, None]

        for step, (c_x, s_x, c_y, s_y, c_z, s_z) in enumerate(zip(c_xs, s_xs, c_ys, s_ys, c_zs, s_zs)):
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
    with Pool(processes=5) as pool:
        pool.starmap(donut.processing, [(1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)])
    donut.video()
    # donut.deletion()
    print(f'ended in {str(time.time() - debut)} secondes')
    sys.exit()
