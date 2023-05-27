import numpy as np
import cv2 as cv

class Mapa:
    m = None
    
    def __init__(self, m):
        self.m = m
    
    # WIP: Not for use
    @staticmethod
    def from_image(image, cell_size, matrix_size):
        COLOR_CLASSES = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (0, 0, 0),
            (255, 255, 255),
        ]
        m = np.zeros(matrix_size, dtype=int)
        w, h = cell_size
        for y in range(matrix_size[1]):
            for x in range(matrix_size[0]):
                # extract cell to analyze
                y_begin = h*y
                y_end = h*(y+1)-1
                x_begin = w*x
                x_end = w*(x+1)-1
                cell = image[y_begin:y_end, x_begin:x_end]
                # use kmeans to find one mean color
                kmeans_img = np.float32(cell.reshape((-1, 3)))
                criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                n_clusters = 1
                ret, label, center = cv.kmeans(kmeans_img,n_clusters,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
                center = np.uint8(center)
                res = center[label.flatten()]
                res2 = res.reshape((cell.shape))
                mean_color = res2[0, 0]
                # find distance between color classes
                distances = [Mapa._color_distance(klass, mean_color) for klass in COLOR_CLASSES]
                m[y, x] = np.argmin(distances)
        return Mapa(m)
    
    @staticmethod
    def _color_distance(color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        rmean = np.uint64((r1 + r2) / 2)
        r = r1 - r2
        g = g1 - g2
        b = b1 - b2
        distance = np.sqrt([(np.uint64((512 + rmean) * r**2) >> np.uint64(8)) + 4 * g**2 + (np.uint64((767 - rmean) * b**2) >> np.uint64(8))])
        return distance[0]
                
                
                
