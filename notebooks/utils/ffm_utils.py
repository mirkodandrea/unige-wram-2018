import numpy as np
import matplotlib.pyplot as plt

from numpy.random import random
from matplotlib import animation
from matplotlib import colors

from IPython.core.display import display, HTML
from progressbar import ProgressBar as PB

EMPTY, TREE, FIRE = 0, 1, 2

def run_simulation(X, n_frames, func):
    '''
    initialize a simulation and returns an animatee object to 
    be used with run_and_display
    '''
    # Colours for visualization: brown for EMPTY, dark green for TREE and orange
    # for FIRE. Note that for the colormap to work, this list and the bounds list
    # must be one larger than the number of different values in the array.
    colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange']
    cmap = colors.ListedColormap(colors_list)
    bounds = [0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    
    fig = plt.figure(figsize=(15, 8))
    ax1 = fig.add_subplot(121)
    #ax.set_axis_off()
    im = ax1.imshow(X, cmap=cmap, norm=norm)#, interpolation='nearest')
    ax2 = fig.add_subplot(122)
    
    n_trees = np.nan * np.ones((n_frames,))
    n_trees[0] = np.sum(X == TREE)
    pl,  = ax2.plot(np.arange(n_frames), n_trees)#, interpolation='nearest')
    ax2.set_xlabel('iteration')
    ax2.set_ylabel('# of trees')    
    
    bar = PB(min_value=0, max_value=n_frames)
    # The animation function: called to produce a frame for each generation.
    def animate(i):
        bar.update(i)
        im.set_data(animate.X)
        animate.X = func(animate.X)

        animate.n_trees[i] = np.sum(animate.X == TREE)
        ax2.plot(np.arange(n_frames), animate.n_trees, 'r')
        ax2.set_xlim(0, n_frames)
        ax2.set_ylim(0, np.multiply(*animate.X.shape))

    # Bind our grid to the identifier X in the animate function's namespace.
    animate.X = X
    animate.n_trees = n_trees
    anim = animation.FuncAnimation(fig, animate, frames=n_frames)
    
    display(HTML(anim.to_jshtml(fps=10)))
