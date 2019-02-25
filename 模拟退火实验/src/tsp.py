import matplotlib.pyplot as plt
import random
import math
import time

MAX_TEMPERATURE = 0.4   # 如果是超过250个点就改成1
MIN_TEMPERATURE = 0.01    # 如果是超过250个点就改成0.01
MARKOV_LENGTH = 2000        # 越大越好，写文件的时候设置大一点，显示图片的时候设置小一点
ATTENUATION_QUOTIENT = 0.99

PAUSE_TIME = 0.00001

IF_SHOW_FIGURE = False

coordinate_x = []
coordinate_y = []


def generate_random_list(point_num):
    point_list = [0]*(point_num - 1)
    for i in range(0, point_num - 1):
        point_list[i] = i+1
    random.shuffle(point_list)
    point_list.insert(0, 0)
    point_list.append(0)
    return point_list


def get_distance(point_a, point_b):
    temp1 = math.pow(coordinate_x[point_a] - coordinate_x[point_b], 2)
    temp2 = math.pow(coordinate_y[point_a] - coordinate_y[point_b], 2)
    return math.pow(temp1 + temp2, 0.5)


class ExchangeLocalSearch:

    def __init__(self, problem_size):
        self.problem_size = problem_size
        # 初始化一个随机解
        self.point_list = generate_random_list(self.problem_size)

        self.path_count = 0.0
        self.coordinate_x = []
        self.coordinate_y = []
        for i in range(0, self.problem_size):
            self.path_count += get_distance(self.point_list[i], self.point_list[i + 1])
            self.coordinate_x.append(coordinate_x[self.point_list[i]])
            self.coordinate_y.append(coordinate_y[self.point_list[i]])
        self.coordinate_x.append(coordinate_x[0])
        self.coordinate_y.append(coordinate_y[0])

        self.path_count_set = []

        self.path_count_set.append(self.path_count)
        if IF_SHOW_FIGURE:
            self.show_figure()

    def show_figure(self):
        plt.figure('Exchange Local Search')
        plt.scatter(self.coordinate_x, self.coordinate_y)
        plt.plot(self.coordinate_x, self.coordinate_y)
        plt.draw()
        plt.figure('path length 1')
        plt.plot(self.path_count_set)
        time.sleep(PAUSE_TIME)
        plt.pause(PAUSE_TIME)
        plt.figure('Exchange Local Search')
        plt.cla()
        plt.figure('path length 1')
        plt.cla()

    # 包括保存结果图片和结果路径
    def store_result(self):
        plt.figure('Exchange Local Search result')
        plt.scatter(self.coordinate_x, self.coordinate_y)
        plt.plot(self.coordinate_x, self.coordinate_y)
        plt.savefig("Exchange Local Search result.png")
        plt.figure('path length 1')
        plt.plot(self.path_count_set)
        plt.savefig("path length 1.png")
        plt.close('all')

        fp = open("Exchange Local Search result.txt", 'w')
        fp.write('result path length:' + str(self.path_count) + '\n')
        fp.write('result path:\n')
        for i in range(0, self.problem_size+1):
            fp.write(str(self.point_list[i]))
            fp.write('\n')

    def swap_two_point(self):
        index1 = random.randint(1, self.problem_size - 1)
        index2 = random.randint(1, self.problem_size - 1)
        while index1 == index2:
            index1 = random.randint(1, self.problem_size - 1)
            index2 = random.randint(1, self.problem_size - 1)

        path_count_before = get_distance(self.point_list[index1-1], self.point_list[index1]) \
                            + get_distance(self.point_list[index1+1], self.point_list[index1]) \
                            + get_distance(self.point_list[index2-1], self.point_list[index2]) \
                            + get_distance(self.point_list[index2+1], self.point_list[index2])

        temp = self.point_list[index1]
        self.point_list[index1] = self.point_list[index2]
        self.point_list[index2] = temp

        path_count_after = get_distance(self.point_list[index1-1], self.point_list[index1]) \
                            + get_distance(self.point_list[index1+1], self.point_list[index1]) \
                            + get_distance(self.point_list[index2-1], self.point_list[index2]) \
                            + get_distance(self.point_list[index2+1], self.point_list[index2])

        if path_count_before <= path_count_after:
            temp = self.point_list[index1]
            self.point_list[index1] = self.point_list[index2]
            self.point_list[index2] = temp
            return False

        self.path_count = self.path_count - path_count_before + path_count_after
        temp = self.coordinate_x[index1]
        self.coordinate_x[index1] = self.coordinate_x[index2]
        self.coordinate_x[index2] = temp
        temp = self.coordinate_y[index1]
        self.coordinate_y[index1] = self.coordinate_y[index2]
        self.coordinate_y[index2] = temp
        return True

    def solve(self):
        # 进行迭代求解
        for i in range(0, 100*MARKOV_LENGTH):
            if self.swap_two_point():
                print('使用交换点策略的局部搜索 ', ' 第', i, '轮 ', '路径长度更新为：', self.path_count)

                self.path_count_set.append(self.path_count)
                if IF_SHOW_FIGURE:
                    self.show_figure()
        self.store_result()


class InverseLocalSearch:

    def __init__(self, problem_size):
        self.problem_size = problem_size
        # 初始化一个随机解
        self.point_list = generate_random_list(self.problem_size)

        self.path_count = 0.0
        self.coordinate_x = []
        self.coordinate_y = []
        for i in range(0, self.problem_size):
            self.path_count += get_distance(self.point_list[i], self.point_list[i + 1])
            self.coordinate_x.append(coordinate_x[self.point_list[i]])
            self.coordinate_y.append(coordinate_y[self.point_list[i]])
        self.coordinate_x.append(coordinate_x[0])
        self.coordinate_y.append(coordinate_y[0])

        self.path_count_set = []

        self.path_count_set.append(self.path_count)
        if IF_SHOW_FIGURE:
            self.show_figure()

    def show_figure(self):
        plt.figure('Inverse Local Search')
        plt.scatter(self.coordinate_x, self.coordinate_y)
        plt.plot(self.coordinate_x, self.coordinate_y)
        plt.draw()
        plt.figure('path length 2')
        plt.plot(self.path_count_set)
        time.sleep(PAUSE_TIME)
        plt.pause(PAUSE_TIME)
        plt.figure('Inverse Local Search')
        plt.cla()
        plt.figure('path length 2')
        plt.cla()

    # 包括保存结果图片和结果路径
    def store_result(self):
        plt.figure('Inverse Local Search result')
        plt.scatter(self.coordinate_x, self.coordinate_y)
        plt.plot(self.coordinate_x, self.coordinate_y)
        plt.savefig("Inverse Local Search result.png")
        plt.figure('path length 2')
        plt.plot(self.path_count_set)
        plt.savefig("path length 2.png")
        plt.close('all')

        fp = open("Inverse Local Search result.txt", 'w')
        fp.write('result path length:' + str(self.path_count) + '\n')
        fp.write('result path:\n')
        for i in range(0, self.problem_size + 1):
            fp.write(str(self.point_list[i]))
            fp.write('\n')

    def swap_sub_path(self):
        index1 = random.randint(1, self.problem_size - 2)
        index2 = random.randint(index1 + 1, self.problem_size - 1)

        path_count_before = get_distance(self.point_list[index1 - 1], self.point_list[index1]) \
                             + get_distance(self.point_list[index2 + 1], self.point_list[index2])
        path_count_after = get_distance(self.point_list[index1 - 1], self.point_list[index2]) \
                             + get_distance(self.point_list[index2 + 1], self.point_list[index1])

        if path_count_before > path_count_after:
            self.path_count = self.path_count - path_count_before + path_count_after
            for i in range(index1, math.floor((index1 + index2)/2) + 1):
                temp = self.point_list[i]
                self.point_list[i] = self.point_list[index1 + index2 - i]
                self.point_list[index1 + index2 - i] = temp
                temp = self.coordinate_x[i]
                self.coordinate_x[i] = self.coordinate_x[index1 + index2 - i]
                self.coordinate_x[index1 + index2 - i] = temp
                temp = self.coordinate_y[i]
                self.coordinate_y[i] = self.coordinate_y[index1 + index2 - i]
                self.coordinate_y[index1 + index2 - i] = temp
            return True

        return False

    def solve(self):
        # 进行迭代求解
        for i in range(0, 100*MARKOV_LENGTH):
            if self.swap_sub_path():
                print('使用交换路径策略的局部搜索 ', ' 第', i, '轮 ', '路径长度更新为：', self.path_count)

                self.path_count_set.append(self.path_count)
                if IF_SHOW_FIGURE:
                    self.show_figure()
        self.store_result()


class SimulateAnneal:

    def __init__(self, problem_size):
        self.problem_size = problem_size
        # 初始化一个随机解
        self.point_list = generate_random_list(self.problem_size)

        self.path_count = 0.0
        self.coordinate_x = []
        self.coordinate_y = []
        for i in range(0, self.problem_size):
            self.path_count += get_distance(self.point_list[i], self.point_list[i + 1])
            self.coordinate_x.append(coordinate_x[self.point_list[i]])
            self.coordinate_y.append(coordinate_y[self.point_list[i]])
        self.coordinate_x.append(coordinate_x[0])
        self.coordinate_y.append(coordinate_y[0])

        self.path_count_set = []

        self.path_count_set.append(self.path_count)
        if IF_SHOW_FIGURE:
            self.show_figure()

        self.temperature = MAX_TEMPERATURE

    def show_figure(self):
        plt.figure('Simulate Anneal')
        plt.scatter(self.coordinate_x, self.coordinate_y)
        plt.plot(self.coordinate_x, self.coordinate_y)
        plt.draw()
        plt.figure('path length 3')
        plt.plot(self.path_count_set)
        time.sleep(PAUSE_TIME)
        plt.pause(PAUSE_TIME)
        plt.figure('Simulate Anneal')
        plt.cla()
        plt.figure('path length 3')
        plt.cla()

    # 包括保存结果图片和结果路径
    def store_result(self):
        plt.figure('Simulate Anneal result')
        plt.scatter(self.coordinate_x, self.coordinate_y)
        plt.plot(self.coordinate_x, self.coordinate_y)
        plt.savefig("Simulate Anneal result.png")
        plt.figure('path length 3')
        plt.plot(self.path_count_set)
        plt.savefig("path length 3.png")
        plt.close('all')

        fp = open("Simulate Anneal result.txt", 'w')
        fp.write('result path length:' + str(self.path_count) + '\n')
        fp.write('result path:\n')
        for i in range(0, self.problem_size + 1):
            fp.write(str(self.point_list[i]))
            fp.write('\n')

    def swap_sub_path(self):
        index1 = random.randint(1, self.problem_size - 2)
        index2 = random.randint(index1 + 1, self.problem_size - 1)

        path_count_before = get_distance(self.point_list[index1 - 1], self.point_list[index1]) \
                           + get_distance(self.point_list[index2 + 1], self.point_list[index2])
        path_count_after = get_distance(self.point_list[index1 - 1], self.point_list[index2]) \
                           + get_distance(self.point_list[index2 + 1], self.point_list[index1])

        if path_count_before > path_count_after or \
                random.random() < math.exp((path_count_before - path_count_after)/path_count_before/self.temperature):
            self.path_count = self.path_count - path_count_before + path_count_after
            for i in range(index1, math.floor((index1 + index2) / 2) + 1):
                temp = self.point_list[i]
                self.point_list[i] = self.point_list[index1 + index2 - i]
                self.point_list[index1 + index2 - i] = temp
                temp = self.coordinate_x[i]
                self.coordinate_x[i] = self.coordinate_x[index1 + index2 - i]
                self.coordinate_x[index1 + index2 - i] = temp
                temp = self.coordinate_y[i]
                self.coordinate_y[i] = self.coordinate_y[index1 + index2 - i]
                self.coordinate_y[index1 + index2 - i] = temp
            return True

        return False

    def solve(self):
        # 进行迭代求解
        while self.temperature > MIN_TEMPERATURE:
            for i in range(0, MARKOV_LENGTH):
                if self.swap_sub_path():
                    print('使用模拟退火', ' 当前温度：', self.temperature, ' 第', i, '轮 ', '路径长度更新为：', self.path_count)
                    self.path_count_set.append(self.path_count)
                    if IF_SHOW_FIGURE:
                        self.show_figure()
            self.temperature *= ATTENUATION_QUOTIENT
        self.store_result()


def main():
    filename = input('请输入tsp问题的数据文件名：')
    fp = open(filename)
    problem_name = (fp.readline().split())[1]
    problem_type = (fp.readline().split())[1]
    fp.readline()
    problem_size = int((fp.readline().split())[1])
    print(problem_size)
    fp.readline()
    fp.readline()

    for i in range(0, problem_size):
        point = fp.readline().split()
        coordinate_x.append(float(point[1]))
        coordinate_y.append(float(point[2]))

    print('问题名称：', problem_name, '\n', '问题类型：', problem_type)
    print('节点个数：', problem_size, '\n', )

    choose = input('显示路径变化过程输入并将结果写入文件1， 仅仅将结果写入文件输入2：')
    if choose == '1':
        global IF_SHOW_FIGURE
        IF_SHOW_FIGURE = True

    print('使用交换节点操作的局部搜索：')
    solution1 = ExchangeLocalSearch(problem_size)
    solution1.solve()

    print('使用反转路径操作的局部搜索：')
    solution2 = InverseLocalSearch(problem_size)
    solution2.solve()

    print('使用模拟退火得出的解：')
    solution3 = SimulateAnneal(problem_size)
    solution3.solve()
    return


if __name__ == '__main__':
    main()
