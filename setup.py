import network

wlan_st = network.WLAN(network.STA_IF)
wlan_st.active(False)
wlan_ap = network.WLAN(network.AP_IF)
wlan_ap.active(False)
