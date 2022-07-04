from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np

from constants import CONST_G


class Planet:
    def __init__(self, name, mass=1, pos=(0, 0, 0), vel=(0, 0, 0), is_sun = False) -> None:
        self.name  = name
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.is_sun = is_sun
        self.pos_record = []
        self.vel_record = []

    def get_info(self):
        print("------------------------------------------")
        print(f"Name: {self.name}")
        print(f"Mass: {self.mass}")
        print(f"Pos: {self.pos}")
        print(f"Vel: {self.vel}")

    def get_distance(self, planet):
        # if planet == 0:
        #     planet = self
        distance = np.sqrt((self.pos[0]-planet.pos[0])**2+(self.pos[1]-planet.pos[1])**2+(self.pos[2]-planet.pos[2])**2)
        return distance

    def get_force(self, planet):
        # if type(planet) == int:
        #     planet = self
        d = self.get_distance(planet)**3
        # K = -CONST_G * self.mass * planet.mass / d
        K = -CONST_G * planet.mass / d
        fx = K * (self.pos[0] - planet.pos[0])
        fy = K * (self.pos[1] - planet.pos[1])
        fz = K * (self.pos[2] - planet.pos[2])
        return [fx, fy, fz]

    def get_y_matrix(self):
        return np.array([[self.pos[0]],
                        [self.pos[1]],
                        [self.pos[2]],
                        [self.vel[0]],
                        [self.vel[1]],
                        [self.vel[2]]])

    def update_coords(self, new_pos, new_vel):
        self.pos_record.append([self.pos[0], self.pos[1], self.pos[2]])
        self.vel_record.append([self.vel[0], self.vel[1], self.vel[2]])
        self.pos = new_pos
        self.vel = new_vel

    def get_pos_record(self):
        pos_r_x, pos_r_y, pos_r_z = [], [], []
        for pos in self.pos_record:
            pos_r_x.append(pos[0])
            pos_r_y.append(pos[1])
            pos_r_z.append(pos[2])
        return [pos_r_x, pos_r_y, pos_r_z]


class System:
    def __init__(self, name = "Default", planets = []) -> None:
        self.name = name
        self.planets = planets
        self.nb_planets = len(planets)

    def add_planet(self, planet):
        self.planets.append(planet)
        self.nb_planets += 1

    def get_info(self):
        print("==========================================")
        print(f"Name: {self.name}")
        for planet in self.planets:
            planet.get_info()
        print("==========================================")

    def get_info_value(self):
        info = ["=========================================="]
        info.append(f"Name: {self.name}")
        for planet in self.planets:
            info.append('------------------------------------------')
            info.append(f"Name: {planet.name}")
            info.append(f"Mass: {planet.mass}")
            info.append(f"Pos: {planet.pos}")
            info.append(f"Vel: {planet.vel}")
        info.append("==========================================")
        return info

    def get_state(self):
        state = []
        for planet in self.planets:
            for p in planet.pos:
                state.append(p)
            for v in planet.vel:
                state.append(v)
            for f in self.get_forces(self.planets.index(planet)):
                state.append(f)
        return state
    
    def get_forces(self, i_planet: int):
        force_x, force_y, force_z = 0, 0, 0
        for i in range(0, len(self.planets)):
            if i != i_planet:
                fx, fy, fz = self.planets[i_planet].get_force(self.planets[i])
                force_x += fx
                force_y += fy
                force_z += fz
        return [force_x, force_y, force_z]

    def get_y_matrix(self):
        matrix = self.planets[0].get_y_matrix()
        for planet in self.planets[1:]:
            matrix = np.append(matrix, planet.get_y_matrix(), axis=0)    
        return matrix

    def get_f_matrix(self, Y):
        fx, fy, fz = self.get_forces(0)
        # nbp = self.nb_planets-1
        # fxx, fyy, fzz = nbp*self.planets[0].get_force(0)
        # fx = fxx-fx
        # fy = fyy-fy
        # fz = fzz-fz
        print("bonjour")
        print(Y)
        matrix = np.array([[0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 1],
                           [fx/Y[0].astype(float), 0, 0, 0, 0, 0],
                           [0, fy/Y[1].astype(float), 0, 0, 0, 0],
                           [0, 0, fz/Y[2].astype(float), 0, 0, 0]])
        matrix = np.append(matrix, np.zeros((6, 6*(self.nb_planets-1))), axis=1)
        for planet in self.planets[1:-1]:
            fx, fy, fz = self.get_forces(self.planets.index(planet))
            # fxx, fyy, fzz = nbp*self.planets[self.planets.index(planet)].get_force(self.planets.index(planet))
            # fx = fxx-fx
            # fy = fyy-fy
            # fz = fzz-fz
            mat = np.array([[0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 1],
                            [fx/Y[0].astype(float), 0, 0, 0, 0, 0],
                            [0, fy/Y[1].astype(float), 0, 0, 0, 0],
                            [0, 0, fz/Y[2].astype(float), 0, 0, 0]])
            mat = np.append(np.zeros((6, 6*self.planets.index(planet))), mat, axis=1)
            mat = np.append(mat, np.zeros((6, 6*(self.nb_planets-(self.planets.index(planet)+1)))), axis=1)
            matrix = np.append(matrix, mat, axis=0)
        fx, fy, fz = self.get_forces(self.nb_planets-1)
        # fxx, fyy, fzz = nbp*self.planets[nbp].get_force(nbp)
        # fx = fxx-fx
        # fy = fyy-fy
        # fz = fzz-fz
        mat = np.array([[0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1],
                        [fx/Y[0].astype(float), 0, 0, 0, 0, 0],
                        [0, fy/Y[1].astype(float), 0, 0, 0, 0],
                        [0, 0, fz/Y[2].astype(float), 0, 0, 0]])
        mat = np.append(np.zeros((6, 6*(self.nb_planets-1))), mat, axis=1)
        matrix = np.append(matrix, mat, axis=0)
        return matrix

    def system_function(self, Y):
        matrix = np.zeros((6*self.nb_planets, 1))
        for i in range(self.nb_planets):
            matrix[i*6] = Y[i*6+3]
            matrix[i*6+1] = Y[i*6+4]
            matrix[i*6+2] = Y[i*6+5]
            fx, fy, fz = self.get_forces(i)
            matrix[i*6+3] = fx
            matrix[i*6+4] = fy
            matrix[i*6+5] = fz
        return matrix

    def plot(self):
        plt.figure(self.name)
        for planet in self.planets:
            pos = planet.get_pos_record()
            plt.plot(pos[0], pos[1], label=planet.name, marker='.')
        plt.xlabel("x (UA)")
        plt.ylabel("y (UA)")
        plt.axis('square')
        plt.grid()
        plt.legend()
        plt.show()