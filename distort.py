import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
import random

def randdistort(img):
    image= np.array(plt.imread(img))
    rows, cols = image.shape[0], image.shape[1]

    src_cols = np.linspace(0, cols, 20)
    src_rows = np.linspace(0, rows, 10)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    funclist=[lambda x: np.sin(x),lambda x: np.cos(x),lambda x: np.arctan(x)]
    numberOfFunctions=random.randint(2,5)
    # add sinusoidal oscillation to row coordinates
    def func(x):
        newfuncs=[]
        for i in range(numberOfFunctions):
            rand1=random.randint(1,5)
            rand2=random.randint(0,30)
            rand3=random.randint(0,10)
            newfuncs.append(lambda x: rand3*random.choice(funclist)(1/rand1*x+rand2))
        for function in newfuncs:
            x+=function(x)
        return x

            
    def func2(x):
        newfuncs=[]
        for i in range(numberOfFunctions):
            rand1=random.randint(1,5)
            rand2=random.randint(0,30)
            rand3=random.randint(0,15)
            newfuncs.append(lambda x: rand3*random.choice(funclist)(1/rand1*x+rand2))
        for function in newfuncs:
            x+=function(x)
        return x
    dst_rows = src[:, 1] + func(np.linspace(0, 10 * np.pi, src.shape[0]))
    dst_cols =src[:, 0] + func2(np.linspace(0, 3 * np.pi, src.shape[0]))
    dst_rows *= 1.5
    dst_rows -= 1.5 * 50
    dst = np.vstack([dst_cols, dst_rows]).T


    tform = PiecewiseAffineTransform()
    tform.estimate(src, dst)

    out_rows = image.shape[0] - 1.5 * 50
    out_cols = cols
    out = warp(image, tform, output_shape=(out_rows, out_cols))

    fig, ax = plt.subplots()
    ax.imshow(out)
    ax.plot(tform.inverse(src)[:, 0], tform.inverse(src)[:, 1], '.b')
    plt.imsave('name.png', out)
    ax.axis((0, out_cols, out_rows, 0))
    return 'name.png'
