# Use this as a reporting feature from training, only report from which goes to log.txt

import matplotlib.pyplot as plt
import seaborn as sns


class Report:

    def __init__(self):
        self.x = []
        self.y = []

    # Reporting history function that takes in fitness added to log.txt
    # and timestamp of given report time.
    def add_history(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def show(self, head="Time vs Fitness", xlabel="Timestamp (s)", ylabel="Fitness"):
        plt.plot(self.x, self.y, linestyle='-', marker='o')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(head)
        plt.show()