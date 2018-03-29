from chunk_delay.const import *
import matplotlib.pyplot as plt


def test():
    file_name = LOCAL_RESULT_PATH + '/' + 'tcp_classification-1496197005589'
    d_list = []
    n_list = []
    with open(file_name, 'r') as reader:
        lines = reader.readlines()
    for line in lines:
        delay, num = line.strip('\n').split(', ')
        d_list.append(delay)
        n_list.append(num)
    print d_list
    print n_list
    return d_list, n_list


def test_painter():
    x, y = test()
    plt.figure(figsize=(16, 8))
    plt.plot(x, y, linewidth=1)
    plt.xlabel("delay(ms)")
    plt.ylabel("number")
    plt.title("test")
    plt.savefig("line.jpg")
    # plt.show()

if __name__ == '__main__':
    test_painter()
