import time
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np
from PIL import Image
import sys
import os

from Snippets.snippet import Snippet


class Colorizing:
    def __init__(self, imagefolder, imagename="PythonClipVideo.mp4", videofolder=None):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

        self.image_name = imagename
        self.image_folder = imagefolder
        if videofolder is None:
            self.video_folder = self.image_folder
        else:
            self.video_folder = videofolder

        self.fps = 25
        self.pas = 1
        self.var_color = 1530 / (1530 / self.pas)

    def editnew(self, R, G, B, step):
        im = Image.open(self.image_name)
        im = im.rotate((720 / 1530) * step)
        imArray = np.asarray(im)
        arnull = np.array([0, 0, 0, 0])
        aradd = np.array([R, G, B, 0])

        if self.image_name == "IMG_0099.png":
            ar1 = np.array([1, 168, 244, 255])
            ar2 = np.array([26, 37, 111, 255])
            ar3 = np.array([23, 37, 114, 255])
            r1, v1, b1 = Snippet.couleur(True, step)
            r2, v2, b2 = Snippet.couleur(True, step + 612)
            r3, v3, b3 = Snippet.couleur(True, step + 700)
            na1 = np.array([r1, v1, b1, 255])
            na2 = np.array([r2, v2, b2, 255])
            na3 = np.array([r3, v3, b3, 255])

            """
            newImArray = np.where(imArray == arnull, imArray,
                                  np.where(imArray == ar1, (imArray + aradd) % 256,
                                           np.where(imArray == ar2, (imArray + aradd) % 256,
                                                    np.where(imArray == ar3, (imArray + aradd) % 256,
                                                             (imArray + aradd) % 256))))"""
            newImArray = np.where(imArray == arnull, imArray,
                                  np.where(imArray == ar1, na1,
                                           np.where(imArray == ar2, na2,
                                                    np.where(imArray == ar3, na3,
                                                             (imArray + aradd) % 256))))

        else:
            arblanc = np.array([250, 250, 250, 63])
            newImArray = np.where((imArray != arnull) & (imArray != arblanc),
                                  (imArray + aradd) % 256, imArray)

        print(f"création de l'image {step}")
        im = Image.fromarray(newImArray.astype(np.uint8))
        im.save(f"{self.image_folder}/{self.image_name}_"
                f"{self.alphabet[step // 26 // 26 % 26]}{self.alphabet[step // 26 % 26]}{self.alphabet[step % 26]}.png")

    def processing(self, step):
        max = 10
        depart = int(step * 1530 / max)
        arrive = int((step + 1) * 1530 / max)
        for i in range(depart, arrive):
            rouge, vert, bleu = Snippet.couleur(True, i)
            self.editnew(rouge, vert, bleu, i)

    def run(self):
        for i in range(1530):
            rouge, vert, bleu = Snippet.couleur(True, i)
            self.editnew(rouge, vert, bleu, i)

    def video(self):
        image_files = [
            f'{self.image_folder}/{img}'
            for img in os.listdir(self.image_folder)
            if img.endswith(".png")
        ]

        print("Analise des images pour la video en cours...")

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=self.fps)
        clip.write_videofile(f'{self.image_folder}/0Video.mp4')

    def concatenate(self):
        if clips := [
            f'{self.video_folder}/{clip}'
            for clip in os.listdir(self.video_folder)
            if clip.endswith(".mp4")
        ]:
            videofiles = [VideoFileClip(f'{self.video_folder}/{clip}') for clip in clips]
            final_clip = concatenate_videoclips(videofiles)
            final_clip.write_videofile(self.image_name)
            print("Clips concaténés !!")
        else:
            print("Aucun clip dans ce dossier !")

    # Calling the generate_video function

    def analyser(self):
        im = Image.open(self.image_name)
        imArray = np.asarray(im)
        for rows in imArray:
            for pixels in rows:
                if (pixels != np.array([0, 0, 0, 0])).all():
                    print(pixels)


def choix(nbr):
    """
    0 : IPNGris + marine
    1 : LEAP
    2 : BDA
    3 : LogoIPN + marine2
    """
    images = ["IPNGris.png", "IMG_0099.png", "LOGO_BDA.png", "logoIPNatransparent.png"]
    fichier = ["marine", "LEAP", "BDA", "marine2"]
    return images[nbr], fichier[nbr]


if __name__ == '__main__':
    starttime = time.time()

    nom_image, nom_dossier_images = choix(1)
    nom_dossier_videos = nom_dossier_images

    Logo = Colorizing(nom_dossier_images, nom_image, nom_dossier_videos)

    analyser = False
    runtotal = False
    processStep = False  # in range(10) (0 -> 9)
    video = True
    concat = False
    print(processStep)

    if runtotal:
        Logo.run()
    elif processStep:
        Logo.processing(processStep)

    if video:
        Logo.video()
    if concat:
        Logo.concatenate()

    print(f'Programme terminé en {float(time.time() - starttime)} secondes !')

    sys.exit()
