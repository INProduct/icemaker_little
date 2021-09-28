import network
from logger import LogLevel, Logger
from config_manager import ConfigParser

ConfigParser.read_config()

Logger.init(ConfigParser.get_config_for('debug_level'))  # todo read from config

wlan_st = network.WLAN(network.STA_IF)
wlan_st.active(False)
wlan_ap = network.WLAN(network.AP_IF)
wlan_ap.active(False)
