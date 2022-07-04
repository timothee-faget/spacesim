import sys
from syslog import syslog
import numpy as np

from objects import Planet, System
from utils import SysLogger, SysLogReader, import_system, my_plot_2d
from solver.solver import bulirsch

def main():
    solarSystem = import_system('1_sun_2_planet')
    T = 370
    t = 0
    h = 0.1
    j_max = 10
    sysLogger = SysLogger(solarSystem, T, h)
    sysLogger.write_system_state(t, solarSystem.get_state())
    Y = solarSystem.get_y_matrix()

    while t < T: # y'a surement moyen de faire beaucoup mieux ici assez facilement
        Y = bulirsch(Y, solarSystem.system_function, h, j_max)
        Y_list = Y.tolist()
        for pl in solarSystem.planets:
            i = solarSystem.planets.index(pl)
            pl.update_coords((Y_list[6*i][0], Y_list[6*i+1][0], Y_list[6*i+2][0]),
                            (Y_list[6*i+3][0], Y_list[6*i+4][0], Y_list[6*i+5][0]))
        t += h
        sysLogger.write_system_state(t, solarSystem.get_state())

    sysLogger.close_logger()
    # solarSystem.plot()
    sysLogReader = SysLogReader(sysLogger.file_name)
    # sysLogReader.plot_log([1, 2], ['x', 'fx'])
    # sysLogReader.plot_log([1, 2], ['y', 'fy'])
    # sysLogReader.plot_log([1, 2], ['z', 'fz'])
    # sysLogReader.plot_system()
    sysLogReader.plot_system_3d()

    print("done")


if __name__ == "__main__":
    main()