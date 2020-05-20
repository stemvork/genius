from math import pi, cos, sin


class Hex:
    cube_directions = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]
    axial_directions = [(+1, 0), (+1, -1), (0, -1), (-1, 0), (-1, +1), (0, +1)]
    axial_corners = [(6, 0), (6, -6), (0, -6), (-6, 0), (-6, 6), (0, 6)]
    cube_diagonals = [(+2, -1, -1), (+1, +1, -2), (-1, +2, -1), (-2, +1, +1), (-1, -1, +2), (+1, -2, +1)]

    def __constructor(self):
        pass

    @staticmethod
    def cube_add(cube1, cube2):  # trigonometry
        return [sum(x) for x in zip(cube1, cube2)]

    @staticmethod
    def cube_diagonal_neighbor(cube, direction):  # forward compatibility
        return Hex.cube_add(cube, Hex.cube_diagonals[direction])

    @staticmethod
    def cube_direction(direction):  # getter
        return Hex.cube_directions[direction]

    @staticmethod
    def cube_distance(a, b):  # trigonometry
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

    @staticmethod
    def cube_neighbor(cube, direction):  # sense-making
        return Hex.cube_add(cube, Hex.cube_direction(direction))

    @staticmethod
    def cube_round(cube):  # trigonometry
        rx = round(cube[0])
        ry = round(cube[1])
        rz = round(cube[2])

        x_diff = abs(rx - cube[0])
        y_diff = abs(ry - cube[1])
        z_diff = abs(rz - cube[2])

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry
        return rx, ry, rz

    @staticmethod
    def hex_corner(center, s, i):  # trigonometry
        angle_deg = 60 * i  # add - 30 for pointy topped
        angle_rad = pi / 180 * angle_deg
        return (center[0] + s * cos(angle_rad),
                center[1] + s * sin(angle_rad))

    @staticmethod
    def hex_direction(direction):  # getter
        return Hex.axial_directions[direction]

    @staticmethod
    def hex_distance(a, b):  # trigonometry
        ac = Hex.axial_to_cube(a)
        bc = Hex.axial_to_cube(b)
        return Hex.cube_distance(ac, bc)

    @staticmethod
    def hex_neighbor(h, direction):  # sense-making
        dr = Hex.hex_direction(direction)
        return Hex.cube_add(h, dr)

    @staticmethod
    def hex_ring(center, n):  # forward compatibility
        results = []
        for x in range(-n, n + 1):
            for y in range(-n, n + 1):
                if Hex.hex_distance(center, (x, y)) == n:
                    results.append(Hex.cube_add(center, Hex.axial_to_cube((x, y))))
        return results

    @staticmethod
    def hex_round(h):
        return Hex.cube_to_axial(Hex.cube_round(Hex.axial_to_cube(h)))

    @staticmethod
    def hex_spiral(center, radius):  # forward compatibility
        if radius == 0:
            return center
        results = [center]
        for k in range(1, radius):
            results += Hex.hex_ring(center, k)
        return results

    @staticmethod
    def axial_to_cube(h):  # conversion axial to cube
        return h[0], -h[0] - h[1], h[1]

    @staticmethod
    def cube_to_axial(cube):  # conversion cube to axial
        return cube[0], cube[2]

    @staticmethod
    def cube_to_oddq(cube):  # conversion cube to odd_q
        return cube[0], cube[2] + (cube[0] - (cube[0] & 1)) / 2

    @staticmethod
    def oddq_to_cube(h):  # conversion odd_q to cube
        z = h[1] - (h[0] - (h[0] & 1)) / 2
        return h[0], -h[0] - z, z

    @staticmethod
    def test_neighbors(cube):  # testing
        [print(Hex.cube_neighbor(cube, k)) for k in range(6)]
        [print(Hex.hex_neighbor(cube, k)) for k in range(6)]
