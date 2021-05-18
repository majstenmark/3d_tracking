import numpy as np

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
