from matplotlib import pyplot as plt
import csv

with open("plot\..\data\data.csv", "r") as data:
    reader = csv.DictReader(data)
    time_x=[]
    speed_y=[]
    for row in reader:
        time_x.append(str(dict(row)["time"]))
        speed_y.append(float(dict(row)["speed"]))
data.close()

print(time_x, speed_y)