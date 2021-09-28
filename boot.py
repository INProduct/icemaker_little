import network
from logger import LogLevel, Logger
import config_manager


Logger.init(LogLevel.INFO)  # todo read from config

config_manager.ConfigParser.read_config()

wlan_st = network.WLAN(network.STA_IF)
wlan_st.active(False)
wlan_ap = network.WLAN(network.AP_IF)
wlan_ap.active(False)
