from app import IceMaker
import webserver

if __name__ == '__main__':
    application = IceMaker()
    webserver.set_application(application)
    mws = webserver.startWebServer()
    application.main_loop()
