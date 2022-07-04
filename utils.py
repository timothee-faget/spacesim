import json
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import datetime
import csv

from objects import Planet, System

def import_system(name="solar_system"):
    syst_data = json.load(open(f'data/{name}.json'))
    syst = System("Solar System")

    for planet_data in syst_data["planets"]:
        pos = (planet_data["x"], planet_data["y"], planet_data["z"])
        vel = (planet_data["vx"], planet_data["vy"], planet_data["vz"])
        planet = Planet(planet_data["name"], planet_data["mass"], pos, vel, planet_data["isSun"])
        syst.add_planet(planet)
    
    return syst

def my_plot_2d(x, y, tit="Plot", lims=[0,1,-1,1], labels=['x','y']):
    plt.plot(x, y)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.axis(lims)
    plt.title(tit)
    plt.grid()
    plt.show()

class SysLogger:
    def __init__(self, system, T, h) -> None:
        self.system = system
        self.T = T
        self.h = h
        self.start_date = datetime.datetime.now()
        self.start_time = time.time()
        self.file_name = f"{system.name.replace(' ', '_')}_{self.start_date.year}{self.start_date.month}{self.start_date.day}{self.start_date.hour}.csv"
        self.file = open(self.file_name, 'w')
        self.writer = csv.writer(self.file, delimiter =';',escapechar=' ', quoting=csv.QUOTE_NONE)
        self.write_system_info()

    def write_system_info(self):
        self.writer.writerow(["START_SYS_INFO"])
        self.writer.writerow([self.start_date])
        self.writer.writerow([f"System Name: {self.system.name}"])
        self.writer.writerow([f"Duration: {self.T}"])
        self.writer.writerow([f"Step: {self.h}"])
        for line in self.system.get_info_value():
            self.writer.writerow([line])
        self.writer.writerow(["END_SYS_INFO"])
        self.writer.writerow(["START_SYS_STATE"])
        row = ["system time", "time"]
        for planet in self.system.planets:
            row.append(f"{planet.name}_x")
            row.append(f"{planet.name}_y")
            row.append(f"{planet.name}_z")
            row.append(f"{planet.name}_u")
            row.append(f"{planet.name}_v")
            row.append(f"{planet.name}_w")
            row.append(f"{planet.name}_fx")
            row.append(f"{planet.name}_fy")
            row.append(f"{planet.name}_fz")
        self.writer.writerow(row)

    def write_system_state(self, t, args):
        # print([datetime.datetime.now(), t, *args])
        self.writer.writerow([datetime.datetime.now(), t, *args])

    def close_logger(self):
        self.writer.writerow(["END_SYS_STATE"])
        self.file.close()


class SysLogReader():
    def __init__(self, file) -> None:
        self.file_name = file
        self.file = open(self.file_name, 'r')
        self.reader = csv.reader(self.file, delimiter = ';', quotechar="'")
        self.read_log_data()
        self.dict_log = {'x':0,
                        'y':1,
                        'z':2,
                        'u':3,
                        'v':4,
                        'w':5,
                        'fx':6,
                        'fy':7,
                        'fz':8}

    def detect_file_data(self):
        i, i_start, i_end = 0, 0, 0
        for row in self.reader:
            if row[0] == 'START_SYS_STATE':
                i_start = i
            elif row[0] == 'END_SYS_STATE':
                i_end = i
            i += 1
        self.file.seek(0)
        return i_start, i_end

    def read_log_data(self):
        i_start, i_end = self.detect_file_data()
        data = []
        i=0
        for row in self.reader:
            if (i>i_start) and (i<i_end):
                data.append(row)
            i+=1
        data = np.array(data)
        data = data[1:, 1:]
        data = data.astype(float)
        self.data = data

    def plot_log(self, i_planets, mode):
        if type(mode) == list:
            for m in mode:
                i_mode = self.dict_log[m]
                plt.subplot(len(mode), 1, mode.index(m)+1)
                for i in i_planets:
                    i_col = i * 9 + i_mode + 1
                    plt.plot(self.data[1:, 0], self.data[1:, i_col], label=m)
                plt.grid()
                plt.legend()
            plt.show()
        else:
            i_mode = self.dict_log[mode]
            plt.figure('plot_log')
            for i in i_planets:
                i_col = i * 9 + i_mode + 1
                plt.plot(self.data[1:, 0], self.data[1:, i_col], label=mode)
            plt.grid()
            plt.legend()
            plt.show()
        
    def plot_system(self):
        plt.figure('plot_system')
        for i in range(int((len(self.data[0])-1)/9)):
            i_x = i * 9 + 1
            i_y = i * 9 + 2
            plt.plot(self.data[1:, i_x], self.data[1:, i_y]) #, marker='.')
        plt.axis('square')
        plt.show()

    def plot_system_3d(self):
        plt.figure('plot 3d system')
        plt.axes(projection='3d')
        for i in range(int((len(self.data[0])-1)/9)):
            i_x = i * 9 + 1
            i_y = i * 9 + 2
            i_z = i * 9 + 3
            plt.plot(self.data[1:, i_x], self.data[1:, i_y], self.data[1:, i_z]) #, marker='.')
        # plt.axis('square')
        plt.show()
        pass

        


    