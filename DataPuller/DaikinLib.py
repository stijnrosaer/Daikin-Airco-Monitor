"""
Python module to get metrics from and control Daikin airconditioners
Source: https://github.com/arska/python-daikinapi/blob/d98d2f2217b59b4243900319b2af9ed22ecdbdc6/daikinapi.py#L243
"""

import logging
import urllib.parse

import requests


class Daikin:
    """
    Class to get information from Daikin Wireless LAN Connecting Adapter
    """

    _CONTROL_FIELDS = ["f_dir", "f_rate", "mode", "pow", "shum", "stemp"]
    """list of fields that need to be defined for a change request"""

    ATTRIBUTES = [
        "power",
        "target_temperature",
        "target_humidity",
        "mode",
        "mac",
        "name",
        "rev",
        "ver",
        "type",
        "current_month_power_consumption",
        "inside_temperature",
        "outside_temperature",
    ]

    _host = None

    def __init__(self, host):
        """
        Initialize Daikin Aircon API
        :param host: host name/IP address to connect to
        """
        self._host = host

    def _get(self, path):
        """ Internal function to connect to and get any information"""
        response = requests.get("http://" + self._host + path)
        response.raise_for_status()
        logging.debug(response.text)
        if not len(response.text) > 0 or not response.text[0:4] == "ret=":
            return None
        fields = {}
        for group in response.text.split(","):
            element = group.split("=")
            if element[0] == "name":
                fields[element[0]] = urllib.parse.unquote(element[1])
            else:
                fields[element[0]] = element[1]
        return fields

    def _set(self, path, data):
        """ Internal function to connect to and update information"""
        logging.debug(data)
        response = requests.get("http://" + self._host + path, data)
        response.raise_for_status()
        logging.debug(response.text)

    def _get_basic(self):
        """
        Example information:
        ret=OK,type=aircon,reg=eu,dst=1,ver=1_2_51,rev=D3A0C9F,pow=1,err=0,location=0,
        name=%79%6c%c3%a4%61%75%6c%61,icon=0,method=home only,port=30050,id=,pw=,
        lpw_flag=0,adp_kind=3,pv=2,cpv=2,cpv_minor=00,led=1,en_setzone=1,
        mac=D0C5D3042E82,adp_mode=run,en_hol=0,grp_name=,en_grp=0
        :return: dict
        """
        return self._get("/common/basic_info")

    def _get_week(self):
        """
        Example:
        ret=OK,today_runtime=601,datas=0/0/0/0/0/0/1000
        :return: dict
        """
        return self._get("/aircon/get_week_power")

    def _get_week_ex(self):
        """
        Example:
        ret=OK,today_runtime=601,datas=0/0/0/0/0/0/1000
        :return: dict
        """
        return self._get("/aircon/get_week_power_ex")

    def _get_sensor(self):
        """
        Example:
        ret=OK,htemp=24.0,hhum=-,otemp=-7.0,err=0,cmpfreq=40
        :return: dict
        """
        return self._get("/aircon/get_sensor_info")

    def _get_control(self, all_fields=False):
        """
        Example:
        ret=OK,pow=1,mode=4,adv=,stemp=21.0,shum=0,dt1=25.0,dt2=M,dt3=25.0,dt4=21.0,
        dt5=21.0,dt7=25.0,dh1=AUTO,dh2=50,dh3=0,dh4=0,dh5=0,dh7=AUTO,dhh=50,b_mode=4,
        b_stemp=21.0,b_shum=0,alert=255,f_rate=A,f_dir=0,b_f_rate=A,b_f_dir=0,dfr1=5,
        dfr2=5,dfr3=5,dfr4=A,dfr5=A,dfr6=5,dfr7=5,dfrh=5,dfd1=0,dfd2=0,dfd3=0,dfd4=0,
        dfd5=0,dfd6=0,dfd7=0,dfdh=0
        :param all_fields: return all fields or just the most relevant f_dir, f_rate,
        mode, pow, shum,
        stemp
        :return: dict
        """
        data = self._get("/aircon/get_control_info")
        if all_fields:
            return data
        return {key: data[key] for key in self._CONTROL_FIELDS}

    def _get_model(self):
        """
        Example:
        ret=OK,model=0ABB,type=N,pv=2,cpv=2,cpv_minor=00,mid=NA,humd=0,s_humd=0,
        acled=0,land=0,elec=0,temp=1,temp_rng=0,m_dtct=1,ac_dst=--,disp_dry=0,dmnd=0,
        en_scdltmr=1,en_frate=1,en_fdir=1,s_fdir=3,en_rtemp_a=0,en_spmode=0,
        en_ipw_sep=0,en_mompow=0
        :return: dict
        """
        return self._get("/aircon/get_model_info")

    @property
    def power(self):
        """
        unit on/off
        :return: "1" for ON, "0" for OFF
        """
        return int(self._get_control()["pow"])

    @property
    def target_temperature(self):
        """
        target temperature
        range of accepted values determined by mode: AUTO:18-31, HOT:10-31, COLD:18-33
        :return: degrees centigrade
        """
        ret_val = self._get_control()["stemp"]
        try:
            return float(ret_val)
        except:
            return None

    @property
    def mode(self):
        """
        operation mode
        :return: "0": "AUTO", "1": "AUTO", "2": "DEHUMIDIFICATOR", "3": "COLD",
        "4": "HOT", "6": "FAN", "7": "AUTO"
        """
        return int(self._get_control()["mode"])

    @property
    def mac(self):
        """
        wifi module mac address
        :return: A0B1C2D3E4F5G6 formatted mac address
        """
        return self._get_basic()["mac"]

    @property
    def name(self):
        """
        user defined unit name
        :return: string
        """
        return self._get_basic()["name"]

    @property
    def rev(self):
        """
        hardware revision
        :return: e.g. D3A0C9F
        """
        return self._get_basic()["rev"]

    @property
    def ver(self):
        """
        wifi module software version
        :return: e.g. 1_2_51
        """
        return self._get_basic()["ver"]

    @property
    def type(self):
        """
        unit type
        :return: e.g. "aircon"
        """
        return self._get_basic()["type"]

    @property
    def current_day_power_consumption_heat(self):
        ret = self._get_week_ex()["week_heat"].split("/")[0]
        return ret

    @property
    def current_day_power_consumption_cool(self):
        return self._get_week_ex()["week_cool"].split("/")[0]

    @property
    def inside_temperature(self):
        """
        inside current temperature
        :return: degrees centigrade
        """
        return float(self._get_sensor()["htemp"])

    @property
    def outside_temperature(self):
        """
        outside current temperature
        :return: degrees centigrade
        """
        return float(self._get_sensor()["otemp"])

    def __str__(self):
        return "Daikin(host={0},name={1},mac={2})".format(
            self._host, self.name, self.mac
        )
