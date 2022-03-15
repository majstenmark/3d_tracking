import numpy as np

from skspatial.objects import Points, Line
from skspatial.plotting import plot_3d
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import colors


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
    pos_cnt = Counter()
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
                pos_cnt[frameno] += 1
                corners = []
                for i in range(4):
                    px, py = float(data[2 + 2 * i]), float(data[2 + 2 * i + 1])
                    corners.append((px, py))
                positions.append((frameno, corners))
    return positions, cent_pos, frames, pos_cnt

def log2sides(intervals, cent_pos, pos_cnt):
    sides = [[] for _ in range(4)]
    sides2 = [[] for _ in range(4)]
    sides3 = [[] for _ in range(4)]
    inside = 0

    for frameno, rvec, tvec in cent_pos:
        inside = get_side(frameno, intervals, inside)
        if inside == -1:
            break
        no = pos_cnt[frameno]
        if no > 1:
            sides2[inside].append((rvec, tvec))
        if no > 2:
            sides3[inside].append((rvec, tvec))

        sides[inside].append((rvec, tvec))
    return sides, sides2, sides3


def side2XYZ(side):
    X, Y, Z = [], [], []
    #height = 720 
    for rvec, tvec in side:

        x, y, z = tvec[0], tvec[1], tvec[2]
        X.append(x)
        Y.append(y)
        Z.append(z)
    return X, Y, Z

def fitdata(points, pos_min2, pos_min3):
    # sort the data
 

    line_fit = Line.best_fit(points)
    
    
    errs = [[] for _ in range(3)]

    for pt in points:
        d = line_fit.distance_point(pt)
        errs[0].append(d)
    
    for pt in pos_min2:
        d = line_fit.distance_point(pt)
        errs[1].append(d)
    

    for pt in pos_min3:
        d = line_fit.distance_point(pt)
        errs[2].append(d)
    

    return errs

def printerrors(title, errs2d, errs3d):
    means2d = []
    means3d = []
    scale = 1.1 #the image is scaled 
    scalefactor = 1/scale


    mx2d = 0
    mx3d = 0
    mx2d = max(errs2d)
    mean2d = sum(errs2d)/len(errs2d)
        
    
    mx3d = max(errs3d)
    mean3d = sum(errs3d)/len(errs3d)
    
        # We can set the number of bins with the `bins` kwarg

    
    
    print('{}: Values 2D mean distance {:.4f} mm'.format(title, scalefactor * mean2d))
    print('Max 2D {}'.format(mx2d))
    
    print('{}: Values 3D mean distance {:.4f} mm'.format(title, scalefactor * mean3d))
    print('Max 3D {}'.format(mx3d))

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    n_bins = 20

    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(errs2d, bins=n_bins)
    axs[1].hist(errs3d, bins=n_bins)
    plt.show()

    
def to_points(pos):
    
    x, y, z = side2XYZ(pos)
         
    reorder = sorted(range(len(x)), key = lambda ii: x[ii])
    coords = [[x[ii], y[ii], z[ii]] for ii in reorder]
    coord2d = [[x[ii], y[ii]] for ii in reorder]
    return coords, coord2d

def get_errors(sides, sides2, sides3):
    INF = 10**12
    sidecoords = []
    for i, side in enumerate(sides):
        x, y, z = side2XYZ(side)
      
        reorder = sorted(range(len(x)), key = lambda ii: x[ii])
        coords = [[x[ii], y[ii], z[ii]] for ii in reorder]
        coord2d = [[x[ii], y[ii]] for ii in reorder]
        points = Points(coords)
        points2d = Points(coord2d)
        
        pt_min2_3d, pt_min2_2d = to_points(sides2[i])
        pt_min3_3d, pt_min3_2d = to_points(sides3[i])
        sidecoords.append((points, points2d, pt_min2_3d, pt_min2_2d, pt_min3_3d, pt_min3_2d))
        
    
        


    errors2d = [[] for _ in range(3)]
    errors3d = [[] for _ in range(3)]
    
    for i, (points, points2d, pt_min2_3d, pt_min2_2d, pt_min3_3d, pt_min3_2d) in enumerate(sidecoords):
    
        res = fitdata(points, pt_min2_3d, pt_min3_3d)
        
        res2d = fitdata(points2d, pt_min2_2d, pt_min3_2d)


        for i in range(3):
            errors3d[i].extend(res[i])
        
            errors2d[i].extend(res2d[i])
     
    return errors2d, errors3d
    
def calc_scale(sides):
    for side in sides:
        x, y, z = side2XYZ(side)
        dx = abs(max(x) - min(x))
        dy = abs(max(y) - min(y))
        dz = abs(max(z) - min(z))
        d = (dx **2 + dy **2 + dz ** 2) ** 0.5
        print(f'Side length {d}')

def sigma2(err):
    su2 = 0.0
    su = 0.0
    n = 0
    for e in err:
        su2 += e**2
        su += e
        n += 1
    mean = su/n
    return su2/n - mean **2, su/n, len(err) -1

def calc_F_stat(errors2d, errors3d):
    s1_2d, mean1_2d, dof1_2d = sigma2(errors2d[0])
    s2_2d, mean2_2d, dof2_2d = sigma2(errors2d[1])
    s1_3d, mean1_3d,dof1_3d = sigma2(errors3d[0])
    s2_3d, mean2_3d, dof2_3d = sigma2(errors3d[1])
    print(dof1_2d, dof2_2d)
    print(s1_2d, s2_2d)
    print(s1_3d, s2_3d)
    print(f'Deviation {s1_2d**0.5} and 3d {s1_3d**0.5}')
    F_stat_2d = s2_2d/s1_2d
    print(f'F stat 2d {F_stat_2d}')
    F_stat_3d = s2_3d/s1_3d
    print(f'F stat 3d {F_stat_3d}')
'''
Kvadrerat

s1_2d = 2.9036552222865066
s1_3d = 24.910342682029324
s2_2d = 0.11088325532156487
s2_3d = 2.3049050778460796
F_stat_2d = s1_2d/s2_2d
F_stat_3d = s1_3d/s2_3d
F_stat_2d
F_stat_3d

'''

def main():
    intervals = readcuts('cuts2_hres.txt')

    #logs = [('MAH00337_recalibrated.txt', 10), ('MAH00337min2_recalibrated.txt', 10), ('MAH00337_log_dodeca.txt', 12), ('MAH00337_log_dodeca_pnp.txt', 12)]
    #logs = [('log_may19_calc1_min1_fix.txt', 10), ('log_may19_calc1_min2_fix.txt', 10)]
    #logs = [('log_may19_calc2_min1_fix.txt', 10), ('log_may19_calc2_min2_fix.txt', 10)]
    #logs = [('log_conv_calc1_min1_hres.txt', 10), ('log_conv_calc1_min2_hres.txt', 10)]
    logs = [('log_conv_calc1_min1_scaled.txt', 10), ('log_conv_calc1_min2_scaled.txt', 10)]
    #
    #logs = [('log_conv_calc1_min1_fix.txt', 10), ('log_conv_calc1_min2_fix.txt', 10)]
    #logs = [('MAH00337_recalibrated.txt', 10), ('MAH00337min2_recalibrated.txt', 10), ('MAH00337_log_dodeca.txt', 12), ('MAH00337_log_dodeca_pnp.txt', 12)]
    #logs = [('./logs/MAH00337_old.txt', 10), ('./logs/MAH00337min2_old.txt', 10)]
    
    #logs = [('test_yumi_calib_min1.txt', 10), ('test_yumi_calib_min2.txt', 10), ('MAH00337_log_dodeca.txt', 12), ('MAH00337_log_dodeca_pnp.txt', 12)]
    
    titles = ['PNP min1', 'PNP min2']
    #intervals = readcuts('cuts.txt')
    for title, (logfile, centerid) in zip(titles, logs[1:2]):
        
        #_, cent_pos, _ = readlog('MAH00337_log_dodeca.txt', 12)
        #_, cent_pos, _ = readlog('MAH00337.txt', 10)
        
        _, cent_pos, _, pos_cnt = readlog(logfile, centerid)
        
        #_, cent_pos, _ = readlog('MAH00337.txt', 10)
        
        sides, sides2, sides3 = log2sides(intervals, cent_pos,pos_cnt)
        su = 0
        for side in sides:
            su += len(side)
        print('len', su)
        #calc_scale(sides)
        errors2d, errors3d = get_errors(sides2, sides2, sides3)
        calc_F_stat(errors2d, errors3d)
        printerrors(title, errors2d[0], errors3d[0])
        
#http://www.biokin.com/tools/f-critical.html
#https://en.wikipedia.org/wiki/Half-normal_distribution. larger value top.
if __name__ == '__main__':
    main()