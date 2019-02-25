import random
import math
import queue
import matplotlib.pyplot as plt
import time

coordinate_x = []
coordinate_y = []

IF_SHOW_FIGURE = False
PAUSE_TIME = 0.001

MAX_NUM = 10000000
MAX_GENERATION = 10000


class Individual(object):
    def __init__(self, score, point_list):
        self.score = score
        self.point_list = point_list

    def __lt__(self, other):
        return self.score < other.score


def cycle_shift(point_list, point):
    i = 0
    temp = []
    while point_list[i] != point:
        i += 1
    for j in range(i, len(point_list)):
        temp.append(point_list[j])
    for j in range(0, i):
        temp.append(point_list[j])
    return temp


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


def get_path_length(point_list):
    path_length = 0
    for i in range(0, len(point_list)-1):
        path_length += get_distance(point_list[i], point_list[i+1])
    path_length += get_distance(point_list[len(point_list)-1], point_list[0])
    return path_length


def generate_greedy_list(point_num):
    point_list = []
    visit_list = [0]*point_num

    pre = 0
    visit_list[pre] = 1
    point_list.append(pre)

    for i in range(1, point_num):
        closest_neighbor = MAX_NUM
        index = -1
        for j in range(0, point_num):
            if visit_list[j] == 1:
                continue
            temp = get_distance(pre, j)
            if temp < closest_neighbor:
                closest_neighbor = temp
                index = j
        pre = index
        visit_list[pre] = 1
        point_list.append(pre)

    point_list.append(0)
    return point_list


class GenericAlgorithm:
    def __init__(self, problem_size):
        self.problem_size = problem_size

        self.population_size = 50
        self.population = queue.PriorityQueue()
        self.population_roulette = 0
        self.greedy_num = 0
        for i in range(0, self.greedy_num):
            temp = generate_greedy_list(self.problem_size)
            temp = self.mutation(temp)
            self.population.put(Individual(get_path_length(temp), temp))
        for i in range(0, self.population_size - self.greedy_num):
            temp = generate_random_list(self.problem_size)
            self.population.put(Individual(get_path_length(temp), temp))

        self.generation_count = 0
        self.crossover_rate = 1
        self.mutation_rate = 0.9
        self.preserve_rate = 0.2

        # 用于画图，存储
        self.best_solution = []
        self.min_cost = MAX_NUM
        self.min_cost_set = []

    def evaluate(self):
        self.population_roulette = 0
        for i in range(0, self.population_size):
            self.population_roulette += 1/self.population.queue[i].score
        # for i in range(0, self.population_size):
        #     print(i, 'th sol:', self.population.queue[i].score, 'in ', self.generation_count, 'generation')
        if IF_SHOW_FIGURE and self.population.queue[0].score < self.min_cost:
            self.min_cost = self.population.queue[0].score
            self.min_cost_set.append(self.min_cost)
            self.best_solution = self.population.queue[0].point_list
            self.show_figure()
        elif self.population.queue[0].score < self.min_cost:
            self.min_cost = self.population.queue[0].score
            self.min_cost_set.append(self.min_cost)
            self.best_solution = self.population.queue[0].point_list
        print('best sol:', self.population.queue[0].score, 'in ', self.generation_count, 'generation')

    # selection
    def get_three_parent(self):
        parent1 = -1
        parent2 = -1
        parent3 = -1
        while parent1 == parent2 or parent2 == parent3 or parent1 == parent3:
            roulette_value1 = random.uniform(0, self.population_roulette)
            for i in range(0, self.population_size):
                roulette_value1 -= 1/self.population.queue[i].score
                if roulette_value1 < 0:
                    parent1 = i
                    break

            roulette_value2 = random.uniform(0, self.population_roulette)
            for i in range(0, self.population_size):
                roulette_value2 -= 1/self.population.queue[i].score
                if roulette_value2 < 0:
                    parent2 = i
                    break

            roulette_value3 = random.uniform(0, self.population_roulette)
            for i in range(0, self.population_size):
                roulette_value3 -= 1 / self.population.queue[i].score
                if roulette_value3 < 0:
                    parent3 = i
                    break
        if parent1 == -1 or parent2 == -1 or parent3 == -1:
            print('error')
            exit(0)
        return parent1, parent2, parent3

    # selection
    def get_two_parent(self):
        parent1 = -1
        parent2 = -1
        while parent1 == parent2:
            roulette_value1 = random.uniform(0, self.population_roulette)
            for i in range(0, self.population_size):
                roulette_value1 -= 1/self.population.queue[i].score
                if roulette_value1 < 0:
                    parent1 = i
                    break

            roulette_value2 = random.uniform(0, self.population_roulette)
            for i in range(0, self.population_size):
                roulette_value2 -= 1/self.population.queue[i].score
                if roulette_value2 < 0:
                    parent2 = i
                    break
        if parent1 == -1 or parent2 == -1:
            print('error')
            exit(0)
        return parent1, parent2

    # crossover
    def crossover(self, parent1, parent2, parent3):
        temp_child1 = []
        temp_child2 = []
        temp_child3 = []
        for i in range(0, self.problem_size+1):
            temp_child1.append(self.population.queue[parent1].point_list[i])
            temp_child2.append(self.population.queue[parent2].point_list[i])
            temp_child3.append(self.population.queue[parent3].point_list[i])

        for i in range(1, self.problem_size):
            temp_dist = min(get_distance(temp_child1[i - 1], temp_child1[i]),
                            get_distance(temp_child2[i - 1], temp_child2[i]),
                            get_distance(temp_child3[i - 1], temp_child3[i]))
            if temp_dist == get_distance(temp_child1[i-1], temp_child1[i]):
                temp_child2[i:self.problem_size] = cycle_shift(temp_child2[i:self.problem_size], temp_child1[i])
                temp_child3[i:self.problem_size] = cycle_shift(temp_child3[i:self.problem_size], temp_child1[i])
            elif temp_dist == get_distance(temp_child2[i-1], temp_child2[i]):
                temp_child1[i:self.problem_size] = cycle_shift(temp_child1[i:self.problem_size], temp_child2[i])
                temp_child3[i:self.problem_size] = cycle_shift(temp_child3[i:self.problem_size], temp_child2[i])
            else:
                temp_child1[i:self.problem_size] = cycle_shift(temp_child1[i:self.problem_size], temp_child3[i])
                temp_child2[i:self.problem_size] = cycle_shift(temp_child2[i:self.problem_size], temp_child3[i])

        return temp_child1

    def crossover_1(self, parent1, parent2):
        temp_child1 = []
        temp_child2 = []
        for i in range(0, self.problem_size+1):
            temp_child1.append(self.population.queue[parent1].point_list[i])
            temp_child2.append(self.population.queue[parent2].point_list[i])

        for i in range(1, self.problem_size):
            temp_dist = min(get_distance(temp_child1[i - 1], temp_child1[i]),
                            get_distance(temp_child2[i - 1], temp_child2[i]))
            if temp_dist == get_distance(temp_child1[i-1], temp_child1[i]):
                temp_child2[i:self.problem_size] = cycle_shift(temp_child2[i:self.problem_size], temp_child1[i])
            elif temp_dist == get_distance(temp_child2[i-1], temp_child2[i]):
                temp_child1[i:self.problem_size] = cycle_shift(temp_child1[i:self.problem_size], temp_child2[i])

        return temp_child1

    def mutation(self, new_child):
        index1 = random.randint(1, self.problem_size - 1)
        index2 = random.randint(1, self.problem_size - 1)
        for i in range(index1, math.floor((index1+index2)/2) + 1):
            temp = new_child[i]
            new_child[i] = new_child[index1+index2-i]
            new_child[index1+index2-i] = temp
        return new_child

    # different mutation strategy by swap two point
    def mutation_1(self, new_child):
        index1 = random.randint(1, self.problem_size - 1)
        index2 = random.randint(1, self.problem_size - 1)
        temp = new_child[index1]
        new_child[index1] = new_child[index2]
        new_child[index2] = temp
        return new_child

    def get_children(self):
        new_children = []
        # selection
        parent1, parent2 = self.get_two_parent()
        # crossover
        new_children = self.crossover_1(parent1, parent2)
        # mutation
        if random.random() < self.mutation_rate:
            new_children = self.mutation(new_children)
        return new_children

    def generate_next_generation(self):
        self.evaluate()

        new_generation = queue.PriorityQueue()

        # generate child
        while len(new_generation.queue) < self.population_size*(1 - self.preserve_rate):
            temp = self.get_children()
            new_generation.put(Individual(get_path_length(temp), temp))

        # add children individual and parent individual:
        for i in range(0, int(self.population_size*self.preserve_rate)):
            new_generation.put(self.population.get())

        # change generation
        self.population = new_generation
        # next_generation = queue.PriorityQueue()
        # for i in range(0, self.population_size):
        #     next_generation.put(new_generation.get())
        # self.population = next_generation

        self.generation_count += 1

    def solve(self):
        while self.generation_count < MAX_GENERATION:
            self.generate_next_generation()
        self.store_result()

    def show_figure(self):
        temp_coordinate_x = []
        temp_coordinate_y = []
        for i in range(0, self.problem_size+1):
            temp_coordinate_x.append(coordinate_x[self.best_solution[i]])
            temp_coordinate_y.append(coordinate_y[self.best_solution[i]])
        plt.figure('GA Algorithm')
        plt.scatter(temp_coordinate_x, temp_coordinate_y)
        plt.plot(temp_coordinate_x, temp_coordinate_y)
        plt.draw()
        plt.figure('path length 4')
        plt.plot(self.min_cost_set)
        time.sleep(PAUSE_TIME)
        plt.pause(PAUSE_TIME)
        plt.figure('GA Algorithm')
        plt.cla()
        plt.figure('path length 4')
        plt.cla()

    # 包括保存结果图片和结果路径
    def store_result(self):
        temp_coordinate_x = []
        temp_coordinate_y = []
        for i in range(0, self.problem_size + 1):
            temp_coordinate_x.append(coordinate_x[self.best_solution[i]])
            temp_coordinate_y.append(coordinate_y[self.best_solution[i]])
        plt.figure('GA Algorithm result')
        plt.scatter(temp_coordinate_x, temp_coordinate_y)
        plt.plot(temp_coordinate_x, temp_coordinate_y)
        plt.savefig("GA Algorithm result.png")
        plt.figure('path length 4')
        plt.plot(self.min_cost_set)
        plt.savefig("path length 4.png")
        plt.close('all')

        fp = open("GA Algorithm result.txt", 'w')
        fp.write('result path length:' + str(self.min_cost) + '\n')
        fp.write('result path:\n')
        for i in range(0, self.problem_size+1):
            fp.write(str(self.best_solution[i]))
            fp.write('\n')


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

    print('使用遗传算法：')
    solution1 = GenericAlgorithm(problem_size)
    solution1.solve()
    return


if __name__ == '__main__':
    main()
