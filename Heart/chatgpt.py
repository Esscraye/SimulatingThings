import numpy as np
from moviepy.editor import VideoClip, ImageClip, CompositeVideoClip

# définition de la fonction qui dessine un coeur
def heart(x, y, size):
    xs = (x / size * 2 - 1) * 1.5
    ys = (y / size * 2 - 1) * 1.5
    return (xs ** 2 + ys ** 2 - 1) ** 3 - xs ** 2 * ys ** 3

# définition de la fonction qui convertit les coordonnées des points en image
def pts_to_img(pts, size, color):
    img = np.zeros((size, size, 3), dtype=np.uint8)
    x, y = np.meshgrid(np.arange(size), np.arange(size))
    for pt in pts:
        img[heart(x - pt[0], y - pt[1], size) < 0] = color
    return img

# définition des paramètres de la vidéo
duration = 5
fps = 25
size = 300
color = [255, 0, 0] # rouge

# définition des positions des coeurs à chaque frame
num_frames = duration * fps
pts_per_frame = 30
pts_step = 10
pts_max_offset = size // 3
pts_list = []
for i in range(num_frames):
    np.random.seed(i)
    pts = np.random.rand(pts_per_frame, 2) * size
    pts = pts[~np.any(np.abs(pts - np.mean(pts, axis=0)) > pts_max_offset, axis=1)]
    while len(pts) < pts_per_frame:
        np.random.seed(len(pts))
        new_pts = np.random.rand(pts_step, 2) * size
        new_pts = new_pts[~np.any(np.abs(new_pts - np.mean(new_pts, axis=0)) > pts_max_offset, axis=1)]
        pts = np.concatenate((pts, new_pts), axis=0)
    pts_list.append(pts)

# création de la vidéo
heart_clip = ImageClip(np.ones((1, 1)), duration=duration).fl(lambda gf, t: pts_to_img(pts_list[int(fps * t)], size, color))
video_clip = CompositeVideoClip([heart_clip.set_pos(("center", "center"))], size=(size, size)).set_fps(fps)
video_clip.write_videofile("heart.mp4", fps=fps, codec='libx264')
