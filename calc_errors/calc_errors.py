import numpy as np

from skspatial.objects import Points, Line
from skspatial.plotting import plot_3d


def readcuts(cut_filename):
    ints = [[] for _ in range(4)]
    with open(cut_filename, 'r') as cutfile:
        curr_start = 0
        curr_side = 0
        for line in cutfile.readlines():
            if len(line) > 2:
                data = line.split()
                if len(data) > 2:
                    frameno = int(data[2])
                elif len(data) == 2:
                    frameno = int(data[1])

                if frameno - curr_start > 5:
                
                    ints[curr_side].append([curr_start, frameno])

                    curr_start = frameno
                    curr_side += 1
                    curr_side %= 4
            
    return ints
    
def check_side(frameno, side_intervals):
    for lo, hi in side_intervals:
        if lo <= frameno <= hi:
            return True
    return False

def get_side(frameno, intervals, lastside):
    for i in range(4):
        side = (lastside + i) % 4
        if check_side(frameno, intervals[side]):
            return side
    return -1


def readlog(log, CENTID):
    positions = []
    cent_pos = []
    frames = []
    # Define the codec and create VideoWriter object
    with open(log, 'r+') as logfile: 
        
        for line in logfile.readlines():
            line = line.replace('[', '')
            line = line.replace(']', '')
            
            data = line.split()
            frameno = int(float(data[0]))
            frames.append(frameno)
            id = int(data[1])
            if id == CENTID:
                rvec = np.array(list(map(float, data[2:5])))
                tvec = np.array(list(map(float, data[5:8])))
                cent_pos.append((frameno, rvec, tvec))
            elif id < 10:
                corners = []
                for i in range(4):
                    px, py = float(data[2 + 2 * i]), float(data[2 + 2 * i + 1])
                    corners.append((px, py))
                positions.append((frameno, corners))
    return positions, cent_pos, frames

def log2sides(intervals, cent_pos):
    sides = [[] for _ in range(4)]
    inside = 0

    for frameno, rvec, tvec in cent_pos:
        inside = get_side(frameno, intervals, inside)
        if inside == -1:
            break
        sides[inside].append((rvec, tvec))
    return sides


def side2XYZ(side):
    X, Y, Z = [], [], []
    height = 720 
    for rvec, tvec in side:

        x, y, z = tvec[0], height -tvec[1], tvec[2]
        X.append(x)
        Y.append(y)
        Z.append(z)
    return X, Y, Z

def fitdata(points):
    # sort the data
 

    line_fit = Line.best_fit(points)
    
    
    errs = []
    for pt in points:
        d = line_fit.distance_point(pt)
        errs.append(d)
    return errs

def printerrors(title, errs2d, errs3d):
    means2d = []
    means3d = []
    scale = 1.1 #the image is scaled 
    scalefactor = 1/scale


    mx2d = 0
    mx3d = 0

    for i, side_err in enumerate(errs2d):
        mean = sum(side_err)/len(side_err)
        means2d.append(mean)
        mx2d = max(max(side_err), mx2d)
    
    for i, side_err in enumerate(errs3d):
        mean = sum(side_err)/len(side_err)
    
        # We can set the number of bins with the `bins` kwarg
        means3d.append(mean)

        mx3d = max(max(side_err), mx3d)
    
    
    print('{}: Values 2D average distance {:.4f} mm'.format(title, scalefactor * sum(means2d)/len(means2d)))
    print('Max 2D {}'.format(mx2d))
    
    print('{}: Values 3D average distance {:.4f} mm'.format(title, scalefactor * sum(means3d)/len(means3d)))
    print('Max 3D {}'.format(mx3d))
    
    

def get_errors(sides):
    INF = 10**12
    sidecoords = []
    for i, side in enumerate(sides):
        x, y, z = side2XYZ(side)
      
        reorder = sorted(range(len(x)), key = lambda ii: x[ii])
        coords = [[x[ii], y[ii], z[ii]] for ii in reorder]
        coord2d = [[x[ii], y[ii]] for ii in reorder]
        points = Points(coords)
        points2d = Points(coord2d)
        sidecoords.append((points, points2d))
    errors2d = []
    errors3d = []
    
    for i, (points, points2d) in enumerate(sidecoords):

        res = fitdata(points)
        errors3d.append(res)
        
        res2d = fitdata(points2d)
        errors2d.append(res2d)
     
    return errors2d, errors3d
    

def main():
    intervals = readcuts('cuts.txt')
    logs = [('log_min1.txt', 10), ('log_min2.txt', 10)]
    titles = ['PNP min1', 'PNP min2'] 
    for title, (logfile, centerid) in zip(titles, logs):
        _, cent_pos, _ = readlog(logfile, centerid)
        sides = log2sides(intervals, cent_pos)
        errors2d, errors3d = get_errors(sides)
        printerrors(title, errors2d, errors3d)
    

if __name__ == '__main__':
    main()