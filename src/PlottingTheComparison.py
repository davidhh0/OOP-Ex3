import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def iplot():
    labels = ['Shortest Path', 'Connected Components', 'Connected Component']
    networkx_time = [0.0646604,0.0000198,0.0930230]
    python_time = [0.0618498,0.609384,0.3606705]
    java_time =[0.0556442,0.23009,0.189588]

    x = np.arange(len(labels))  # the label locations
    width = 0.15
    fig, ax = plt.subplots()
    rectNetworkX = ax.bar(x + width/3-0.05, networkx_time, width, label='NetworkX')
    rectPython = ax.bar(x - width/3 - 0.1, python_time, width, label='Python DiGraph')
    rectJava = ax.bar(x - 3*width/3 - 0.15, java_time, width, label='Java Graph')
    ax.set_ylabel('Average time for 6 graphs')
    ax.set_title('Time Comparison')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rectPython)
    autolabel(rectNetworkX)
    autolabel(rectJava)
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    iplot()