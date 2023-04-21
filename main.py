# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import traci
import os
import sys
import optparse
import random
from xml.etree.ElementTree import parse
import numpy as np
import math
from sumolib import checkBinary  # noqa
import SUMO_vehicle
import socket
import time

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

Car_num = 100#设置所需车辆数量

# -------------------------设置与Unity之间的通信---------------------
# ------------------------------------------------------------------------
host, port = "127.0.0.1", 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------










# -----------------------------------------------随机部分--------------------------
# ----------------------------------------------------------------------------------------
def generate_random_integer(start, end):
    return random.randint(start, end)

def random_select(lst):#用于随机选择列表中的元素
    return random.choice(lst)

def random_pick_with_ratio(items, ratios):
    assert len(items) == len(ratios), "Number of items and ratios should be the same"
    population = []
    for i, item in enumerate(items):
        population.extend([i] * ratios[i])
    choices = [items[random.choice(population)] for _ in range(Car_num)]
    return choices
Vtype_list = ["autovehicle","ordinaryvehicle"]
# ------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

# 2023年3月24日，将路网中的所有车辆以字符串的形式将数据表达出来
def StepSumo(SumoObjects):
    SumoObjectsRaw0 = traci.vehicle.getIDList()  # get every vehicle ID
    SumoObjectNames = list(set(SumoObjectsRaw0))  # Make it unique
    # Remove SUMO objects from the list if they left the network
    for Obj in SumoObjects:
        if (not (any(ObjName == Obj.ID for ObjName in SumoObjectNames))):
            SumoObjects.remove(Obj)
    # Append new objects and update existing ones.
    for VehID in SumoObjectNames:
        if (not (any(Obj.ID == VehID for Obj in SumoObjects))):
            NewlyArrived = SUMO_vehicle.SumoObject(VehID)
            SumoObjects.append(NewlyArrived)
    # Update Sumo vehicle objects
    for Obj in SumoObjects:
        Obj.UpdateVehicle()
    return SumoObjects
def ToUnity(Vehicles):
    DataToUnity = "O1G"
    #Other vehicles in the simulation
    for veh in Vehicles:
            DataToUnity += veh.ID + ";" + "{0:.3f}".format(veh.PosX_Center) + ";" + "{0:.3f}".format(veh.PosY_Center) + ";" \
                           + "{0:.2f}".format(veh.Velocity) + ";" + "{0:.2f}".format(veh.Heading) + ";" + str(int(veh.VehicleType)) + "@"
    DataToUnity = DataToUnity + "&\n"
    return DataToUnity
# -----------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------


def run():
    #execute the TraCI control loop
    #按照不同比例随机产生自动驾驶车辆与普通车辆，随机选择路线行驶
    auto_num = 0
    ordinary_num = 0
    for i in range(Car_num):
            Vtype = random_pick_with_ratio(Vtype_list,[70,30])#产生列表，两个元素相加要与Car_num变量相等
            if Vtype[i] == "autovehicle":
                auto_num = auto_num + 1
            else:
                ordinary_num = ordinary_num + 1
            traci.vehicle.add(f"car{i + 2}", f"route{generate_random_integer(0, 21)}", Vtype[i])#此处修改可选路径
    print(f"自动驾驶车辆：{auto_num}辆")
    print(f"普通车辆：{ordinary_num}辆")

    # 生成车辆的数据
    SumoObjects = []
    for step in range(80000):
        traci.simulationStep()
        # 获取道路上自动驾驶车辆的ID信息
        Auto_veh = []#存取自动驾驶车辆ID的列表
        All_Vehicle = traci.vehicle.getIDList()
        for veh in All_Vehicle:
            if traci.vehicle.getTypeID(veh) == "autovehicle":
                Auto_veh.append(veh)
        SumoObjects01 = StepSumo(SumoObjects)
        All_Vehicle_message = ToUnity(SumoObjects01)#路网中所有车辆的信息（以字符串形式）
        print(All_Vehicle_message)
        sock.sendall(All_Vehicle_message.encode("UTF-8"))  # Converting string to Byte, and sending it to C#
        receivedData = sock.recv(1024).decode("UTF-8")  # receiveing data in Byte fron C#, and converting it to String
        # print(receivedData)















def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation


    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "wenyuanbei.sumocfg"])
    run()

