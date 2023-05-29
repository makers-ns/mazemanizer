import numpy as np
import cv2 as cv

class Mapa:
    BALL_RANGE_1 = [(169, 0, 255), (179, 0, 255)]
    BALL_RANGE_2 = [(0, 0, 255), (10, 0, 255)]
    START_RANGE = [(70, 92, 55), (90, 255, 255)]
    GOAL_RANGE = [(0, 0, 68), (179, 78, 146)]
    
    def __init__(self, m):
        self.m = m
    
    # WIP: Not for use
    @staticmethod
    def from_image(image, cell_size, matrix_size):
        COLOR_CLASSES = [
            (255, 0, 0), # field
            (0, 255, 0), # wall
            (0, 255, 255), # ball
            (0, 0, 0), # start
            [(70, 92, 55), (90, 255, 255)], # goal
        ]

        image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        image_hsv = cv.cvtColor(image, cv.COLOR_RGB2HSV)

        m = np.zeros(matrix_size, dtype=int)
        w, h = cell_size
        for y in range(matrix_size[1]):
            for x in range(matrix_size[0]):
                thresh_mask_counts = np.array([0, 0])
                ball_mask_count = 0
                start_end_mask_counts = np.array([0, 0])
                # extract cell to analyze
                y_begin = h*y
                y_end = h*(y+1)-1
                x_begin = w*x
                x_end = w*(x+1)-1
                cell = image[y_begin:y_end, x_begin:x_end]
                cell_gray = image_gray[y_begin:y_end, x_begin:x_end]
                cell_hsv = image_hsv[y_begin:y_end, x_begin:x_end]
                # field and wall treshold
                kernel_3x3 = np.ones((3, 3), np.float32) / 9
                cell_gray_blured = cv.filter2D(cell_gray, -1, kernel_3x3)
                _, field_wall_tresh = cv.threshold(cell_gray_blured, 60, 255, cv.THRESH_BINARY)
                thresh_mask_counts[0] = np.where(field_wall_tresh.flatten())[0].size
                thresh_mask_counts[1] = h * w - thresh_mask_counts[0] # komplement klasifikaciji zida je klasifikacija puta
                # mask for start field
                start_mask = cv.inRange(cell_hsv, Mapa.START_RANGE[0], Mapa.START_RANGE[1])
                start_end_mask_counts[0] = np.where(start_mask.flatten())[0].size
                # end field
                end_mask = cv.inRange(cell_hsv, Mapa.GOAL_RANGE[0], Mapa.GOAL_RANGE[1])
                start_end_mask_counts[1] = np.where(end_mask.flatten())[0].size
                # ball cells
                #print(np.where(cell_hsv[:,:,0].flatten() > 160)[0].size)
                ball_mask_count = np.where(cell_hsv[:,:,0].flatten() > 178)[0].size
                #ball_mask_1 = cv.inRange(cell_hsv, Mapa.BALL_RANGE_1[0], Mapa.BALL_RANGE_1[1])
                #ball_mask_2 = cv.inRange(cell_hsv, Mapa.BALL_RANGE_2[0], Mapa.BALL_RANGE_2[1])
                #ball_mask = ball_mask_1 + ball_mask_2
                #ball_mask_count = np.where(ball_mask.flatten())[0].size
                klass = -1
                if ball_mask_count > 0:
                    klass = 2
                elif np.max(start_end_mask_counts) > 55:
                    klass = 3 + np.argmax(start_end_mask_counts)
                else:
                    klass = np.argmax(thresh_mask_counts)
                m[y, x] = klass
                if y in range(16, 17+1) and x in range(7, 8+1):
                    print(thresh_mask_counts, ball_mask_count, start_end_mask_counts)
                #m[y, x] = np.argmax(mask_counts)
        m[0:2, 0:2] = 1
        m[0:2, 22:24] = 1
        m[22:24, 0:2] = 1
        m[22:24, 22:24] = 1
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
                
                
                
