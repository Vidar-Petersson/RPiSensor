from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib import style
import csv

with open("plot\..\data\data.csv", "r") as data:
    reader = csv.DictReader(data)
    time_x=[]
    speed_y=[]
    for row in reader:
        time_x.append(str(dict(row)["time"]))
        speed_y.append(float(dict(row)["speed"]))
data.close()

plt.plot(time_x, speed_y, label="Speed")

style.use('fivethirtyeight')
plt.xticks(rotation=45, ha="right")
plt.xlabel("Time (H:M:S)")
plt.ylabel("Speed km/s")
plt.title("Speed of logger")
plt.legend()
plt.show()

""" def animate(x,y):
    plt.clear()
    plt.plot(x,y)
    
    style.use('fivethirtyeight')
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Time (H:M:S)")
    plt.ylabel("Speed km/s")
    plt.title("Speed of logger")
    plt.legend()
    plt.show() """

plt.show()