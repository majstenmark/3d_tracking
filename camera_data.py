import yaml
import numpy as np
YAML_FILE = "data_sony.yaml"
def sony_data():
    with open(YAML_FILE, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        camera_matrix = np.array(data_loaded['camera_matrix'])
        dist_coeffs = np.array(data_loaded['dist_coeff'])
    return camera_matrix, dist_coeffs

def get_data(YAML_FILE):
    with open(YAML_FILE, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        camera_matrix = np.array(data_loaded['camera_matrix'])
        dist_coeffs = np.array(data_loaded['dist_coeff'])
    return camera_matrix, dist_coeffs