from DaikinLib import Daikin
from datetime import datetime
import time
from dbConnection import insertStatus

switch = 0

MODES= {
    0: "AUTO",
    1: "AUTO",
    2: "DEHUMIDIFY",
    3: "COOL",
    4: "HEAT",
    6: "FAN",
    7: "AUTO"

}


def get_info(ip):
    API = Daikin(str(ip))

    res = dict()
    res["name"] = API.name
    res["time"] = datetime.now()
    res["target"] = API.target_temperature
    res["inside"] = API.inside_temperature
    res["outside"] = API.outside_temperature
    res["heat"] = API.current_day_power_consumption_heat
    res["cool"] = API.current_day_power_consumption_cool
    res["mode"] = MODES.get(API.mode)
    res["power"] = int(API.power)

    return res

if __name__ == '__main__':

    while True:
        try:
            status_stijn = get_info('192.168.50.50')
            insertStatus(status_stijn)
        except Exception as e:
            print(e)

        try:
            status_senne = get_info('192.168.50.76')
            insertStatus(status_senne)
        except Exception as e:
            print(e)

        print("sleep 5 minutes")
        time.sleep(60*5)
