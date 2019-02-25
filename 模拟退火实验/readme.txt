（1）src文件夹存放python3源代码，运行环境为Windows下python3；
（2）tc文件夹下存分测试样例，ch130、ch150以及a280，分别是130、150、280个城市的tsp问题（还可以下载其它测试样例放到源代码同一文件夹下，运行）python代码即可求解；
（3）没有编译产生的文件，所以不设置bin文件夹；
（4）res文件夹存放实验产生的结果文件，包括随迭代次数增加，tsp解对应路径长度变化曲线'path.png'、tsp最终解'result.txt'、tsp问题求解的连线图'result.png'；
	不同的类方法求解结果对应不同的命名文件，比如Exchange Local Search result.png对应ExchangeLocalSearch类求解所得最终解的连线图
更多详情见实验报告