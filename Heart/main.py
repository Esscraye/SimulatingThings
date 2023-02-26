import sys
import time
import moviepy.video.io.ImageSequenceClip
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
from Snippets.snippet import Snippet


class Heart:
    def __init__(self, film):
        self.hauteur = 500
        self.largeur = 500
        self.Rayon = 50
        self.rayon = 20
        self.Lx, self.Ly, self.Lz = 0, 0, -1  # vecteur lumière
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.image_folder = 'Images'
        self.video_folder = "Video"
        self.fps = 30
        self.frame = 'heart'  # nom racine des images
        self.film = film  # nom de la video
        self.pas = np.pi / 400
        self.pas_theta = np.pi / 250
        self.pas_alpha = np.pi / 100
        self.var_color = 1530 / (2 * np.pi / self.pas)  # coef de variation de couleur

    def make_sym(self, a):
        w, h, c = a.shape
        a[w - w // 2 :, :] = np.flipud(a[:w // 2, :])
        a[:, h - h // 2:] = np.fliplr(a[:, :h // 2])

    def heart(self, start, stop, coef, name='heart'):
        rotation_en_x = np.arange(start, stop, self.pas)
        rotation_en_y = np.zeros(rotation_en_x.shape)

        c_xs, s_xs = np.cos(rotation_en_x), np.sin(rotation_en_x)
        c_ys, s_ys = np.cos(rotation_en_y), np.sin(rotation_en_y)
        c_zs, s_zs = np.cos(rotation_en_x), np.sin(rotation_en_x)

        theta = np.arange(0, np.pi, self.pas_theta)
        c_xt, s_xt = np.cos(theta), np.sin(theta)

        alpha = np.arange(0, np.pi, self.pas_alpha)
        c_xa, s_xa = np.cos(alpha), np.sin(alpha)

        matrice_image = np.empty((self.hauteur, self.largeur, 3), dtype=np.uint8)
        matrice_image_bis = np.empty((self.hauteur, self.largeur), dtype=float)

        bar = tqdm(total=int(((2 * np.pi) / self.pas) / 9), desc='Progress')
        for step, (c_x, s_x, c_y, s_y, c_z, s_z) in enumerate(zip(c_xs, s_xs, c_ys, s_ys, c_zs, s_zs), start=1):
            # start = time.time()
            matrice_image[:] = 0
            matrice_image_bis[:] = -np.inf

            # grand cercle
            Z_R_center, Y_R_center, X_R_center = 0, self.Rayon * s_xt, self.Rayon * c_xt
            ZZ_R_center = Y_R_center * s_x + Z_R_center * c_x
            YY_R_center = Y_R_center * c_x - Z_R_center * s_x
            ZZZ_R_center = ZZ_R_center * c_y - X_R_center * s_y
            XXX_R_center = ZZ_R_center * s_y + X_R_center * c_y
            y_R_center = XXX_R_center * s_z + YY_R_center * c_z
            x_R_center = XXX_R_center * c_z - YY_R_center * s_z

            # petit cercle
            Zs = self.rayon * s_xa
            Ys = (self.Rayon + self.rayon * c_xa[None, :]) * s_xt[:, None]
            Xs = (self.Rayon + self.rayon * c_xa[None, :]) * c_xt[:, None]
            ZZs, YYs = Ys * s_x + Zs * c_x, Ys * c_x - Zs * s_x
            ZZZs, YYYs, XXXs = ZZs * c_y - Xs * s_y, YYs, ZZs * s_y + Xs * c_y
            zs, ys, xs = ZZZs, XXXs * s_z + YYYs * c_z, XXXs * c_z - YYYs * s_z

            matrice_image = self.make_sym(matrice_image)

            zs_norm, ys_norm, xs_norm = zs - ZZZ_R_center[:, None], ys - y_R_center[:, None], xs - x_R_center[:, None]

            produit_scalaire = ((self.Lx * xs_norm + self.Ly * ys_norm + self.Lz * zs_norm) / (
                np.sqrt((zs_norm ** 2 + ys_norm ** 2 + xs_norm ** 2) * (
                        self.Lx ** 2 + self.Ly ** 2 + self.Lz ** 2)))).flatten()

            coord_y = (self.hauteur // 2 - ys.astype(int)).flatten()
            coord_x = (self.largeur // 2 + xs.astype(int)).flatten()

            zs = zs.flatten()
            try:
                mask, = np.where(matrice_image_bis[coord_y, coord_x] < zs)
            except:
                mask, = np.where(matrice_image_bis[coord_y, coord_x] < zs)

            # print(len(mask))
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
                # print(len(mask))

            im = Image.fromarray(matrice_image, 'RGB')
            im = im.convert('RGB')
            im.save(
                ((((((f'{self.image_folder}/{name}' + self.alphabet[((((step // 26) // 26) // 26) // 26)]
                      + self.alphabet[(((step // 26) // 26) // 26) // 26])
                     + self.alphabet[((step // 26) // 26) // 26])
                    + self.alphabet[(step // 26) // 26])
                   + self.alphabet[step // 26])
                  + self.alphabet[step % 26]) + ".png"))

            #print(str(time.time() - debut) + "secondes pour la création de l'image.")
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
        name = f"heart_step{str(step + 1)}_"
        self.heart(depart, arrive, coef, name)


if __name__ == '__main__':
    heart = Heart('Video_heart_4k')
    debut = time.time()
    heart.processing(9, 9)
    heart.processing(1, 9)
    heart.processing(3, 9)
    print(f'{str(time.time() - debut)}secondes')
    """
    heart.processing(1, 9)
    heart.processing(4, 9)
    heart.processing(3, 9)
    print(str(time.time() - debut) + "secondes")
    """
    """
    heart.processing(1, 9)
    heart.processing(4, 9)
    heart.processing(3, 9)
    print(str(time.time() - debut) + "secondes")
    """
    # heart.video()
    # heart.deletion()
    print("finit")
    sys.exit()
