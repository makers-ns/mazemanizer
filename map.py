import numpy as np

class Map:
    def __init__(self):
        pass
    
    # WIP: Not for use
    @staticmethod
    def from_image(image, cell_size):
        m = np.zeros((26, 28))
        h, w = image.shape[:2]
        for y in range(int(h / cell_size[1])):
            for x in range(int(w / cell_size[0])):
                # extract cell to analyze
                y_begin = y*h
                y_end = y*(h+1)-1
                x_begin = x*w
                x_end = x*(w+1)-1
                cell = image[y_begin:y_end, x_begin:x_end]
                # find dominant color
                cell2d = cell.reshape(-1, cell.shape[-1])
                cell1d = np.ravel_multi_index(cell2d.T, (256, 256, 256))
                np.unravel_index(np.bincount(cell1d).argmax(), (256, 256, 256))
