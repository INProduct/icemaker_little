import network
from logger import Logger
from config_manager import ConfigParser

ConfigParser.read_config()

Logger.init(ConfigParser.get_config_for('debug_level'))

wlan_st = network.WLAN(network.STA_IF)
wlan_st.active(False)

wlan_ap = network.WLAN(network.AP_IF)
wap_ssid = ConfigParser.get_config_for('network')['ssid']
wap_pass = ConfigParser.get_config_for('network')['password']
wap_authmode = ConfigParser.get_config_for('network')['auth-mode']
wap_hidden = ConfigParser.get_config_for('network')['hidden']

wlan_ap.config(essid=wap_ssid, authmode=wap_authmode, hidden=wap_hidden, password=wap_pass)
wap_ip = ConfigParser.get_config_for('network')['ip']

wlan_ap.ifconfig((wap_ip, '255.255.255.0', '192.168.0.1', '8.8.8.8'))
wlan_ap.active(True)
