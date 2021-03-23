import pandas as pd
import numpy as np
import os
import datetime

disk_path = "/media/aes/"
disk = ['ADATA UFD']


def save_data(data_t, data1, data2, test_name='data', data2_label=''):
    disk_driver = find_USB()
    if disk_driver != '0':
        dim = 2
        if data2 is not None:
            dim = 3
        n = len(data_t)
        data_array = np.zeros((dim, n))
        for i in range(0, n):
            data_array[0, i] = data_t[i]
        for i in range(0, n):
            data_array[1, i] = data1[i]
        if data2 is not None:
            for i in range(0, len(data2)):
                data_array[2, i] = data2[i]
        np_data = data_array.T
        nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        labels = ['Time (s)', 'Voltage (V)']
        if data2 is not None:
            labels.append(data2_label)
        save = pd.DataFrame(np_data, columns=labels)
        save_path = disk_path + disk_driver + "/" + test_name + "." + nowTime
        save_path.replace(" ", "_")
        save.to_csv(save_path)
        print("Saving success to " + save_path)
        return save_path
    print("Saving failed!")
    return '0'


def find_USB():
    for driver_name in os.listdir(disk_path):
        if driver_name not in disk:
            print("USB driver found!")
            return driver_name
    print("USB driver not found!")
    return '0'


if __name__ == '__main__':
    '''
    t = range(0, 7)
    v = [10, 5, 23, 34, 33, 76, 23]
    i = [9, 4, 4, 23, 235, 5, 43]
    save_data(t, v)
    '''
    d = find_USB()
    print(d)

