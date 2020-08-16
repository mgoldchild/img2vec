import os
import sys

from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append("../img2vec_pytorch")  # Adds higher directory to python modules path.


input_path = './patch_images2'

img2vec = None


def load_img2vec():
    from img_to_vec import Img2Vec
    global img2vec
    img2vec = Img2Vec(model='alexnet')


load_img2vec()

# For each test image, we store the image in a list
list_pics = []
filenames = []
for file in os.listdir(input_path):
    filename = os.fsdecode(file)
    img = Image.open(os.path.join(input_path, filename)).convert('RGB')
    list_pics.append(img)
    filenames.append(filename)

vectors = img2vec.get_vec(list_pics)

pics = {}
for i, vec in enumerate(vectors):
    pics[filenames[i]] = vec


pic_name = ""
while pic_name != "exit":
    pic_name = str(input("Which filename would you like similarities for?\n"))

    try:
        sims = {}
        for key in list(pics.keys()):
            if key == pic_name:
                continue

            sims[key] = cosine_similarity(pics[pic_name].reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]

        d_view = [(v, k) for k, v in sims.items()]
        d_view.sort(reverse=True)
        for v, k in d_view:
            print(v, k)

    except KeyError as e:
        print('Could not find filename %s' % e)

    except Exception as e:
        print(e)
