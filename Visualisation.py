import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

start_index = 1
end_index = -1
xmajorLocator = MultipleLocator(5)
xmajorFormatter = FormatStrFormatter('%1.1f')
xminorLocator = MultipleLocator(1)

ymajorLocator = MultipleLocator(1)
ymajorFormatter = FormatStrFormatter('%1.1f')
yminorLocator = MultipleLocator(0.1)


def img_plot(title, dataT, data1, data2=None, legend2="", label2="", mode='show', path=''):
    plt.close('all')
    T = dataT
    f1 = data1

    fig = plt.figure(dpi=100, figsize=(12.8, 8))

    ax = fig.add_subplot(111)
    ax.plot(T, f1, 'b', label='Voltage')
    ax.grid()
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + 0.02, box.width, box.height])

    if data2 is not None:
        f2 = data2
        ax2 = ax.twinx()
        ax2.set_position([box.x0, box.y0 + 0.02, box.width, box.height])
        ax2.plot(T, f2, 'r', label=legend2)
        ax2.set_ylabel(label2)
        ax.legend(loc='center', bbox_to_anchor=(0.065, 1.05), ncol=3)
        ax2.legend(loc='center', bbox_to_anchor=(0.935, 1.05), ncol=3)

    if mode == 'show':
        plt.show()
    elif mode == 'save':
        plt.savefig(path, dpi=100)
        plt.close()


if __name__ == '__main__':
    img_plot("gg",
             range(0, 7),
             [10, 5, 23, 34, 33, 76, 23],
             [9, 4, 4, 23, 235, 5, 43],
             "Current", path='./gg.png', mode='save')
