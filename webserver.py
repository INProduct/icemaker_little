from microWebSrv import MicroWebSrv
import json


application = None


def set_application(app):
    global application
    application = app


@MicroWebSrv.route('/')
def index_redirect(http_client, http_response):
    http_response.WriteResponseRedirect('/index')


@MicroWebSrv.route('/index')
def index_handler(http_client, http_response):
    http_response.WriteResponsePyHTMLFile('www/index.html')


@MicroWebSrv.route('/style.css')
def get_style_css(http_client, http_response):
    http_response.WriteResponseFile('www/css/style.css', contentType='text/css')


@MicroWebSrv.route('/jquery.min.js')
def get_jquery(http_client, http_response):
    http_response.WriteResponseFile('www/js/jquery.min.js', contentType='text/javascript')


@MicroWebSrv.route('/index_script.js')
def get_index_script(http_client, http_response):
    http_response.WriteResponseFile('www/js/index_script.js', contentType='text/javascript')


@MicroWebSrv.route('/index_info')
def get_index_info(http_client, http_response):
    http_response.WriteResponseJSONOk(obj=application.get_info())


@MicroWebSrv.route('/toggle_water')
def toggle_water_inlet_handler(http_client, http_response):
    application.hand_toggle_water_valve()
    http_response.WriteResponseOk()


@MicroWebSrv.route('/toggle_compressor')
def toggle_compressor_handler(http_client, http_response):
    application.hand_toggle_compressor()
    http_response.WriteResponseOk()


@MicroWebSrv.route('/toggle_pump')
def toggle_pump_handler(http_client, http_response):
    application.hand_toggle_water_pump()
    http_response.WriteResponseOk()


@MicroWebSrv.route('/clean_start')
def clean_start_handler(http_client, http_response):
    application.clean_start()
    http_response.WriteResponseOk()


@MicroWebSrv.route('/clean_stop')
def clean_stop_handler(http_client, http_response):
    application.clean_stop()
    http_response.WriteResponseOk()


@MicroWebSrv.route('/automatic_start')
def automatic_start_handler(http_client, http_response):
    application.automatic_start()
    http_response.WriteResponseOk()


@MicroWebSrv.route('/automatic_stop')
def automatic_stop_handler(http_client, http_response):
    application.automatic_stop()
    http_response.WriteResponseOk()


@MicroWebSrv.route('/set_mode/<mode>')
def set_mode_handler(http_client, http_response, routeArgs):
    mode = int(routeArgs['mode'])
    application.switch_mode(mode)
    http_response.WriteResponseOk()


def startWebServer():
    mws = MicroWebSrv()
    mws.SetNotFoundPageUrl('/notfound')
    mws.Start(threaded=True)
    return mws

