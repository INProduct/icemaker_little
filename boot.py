import network
from logger import Logger
from config_manager import ConfigParser

ConfigParser.read_config()

Logger.init(ConfigParser.get_config_for('debug_level'))

wlan_st = network.WLAN(network.STA_IF)
wlan_st.active(False)
wlan_ap = network.WLAN(network.AP_IF)
wlan_ap.active(False)
