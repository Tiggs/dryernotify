import cherrypy
import json
import datetime

class DryerStatus(object):
    global status

    @cherrypy.expose
    def index(self):
        global status
        currently = sorted(status.items(), reverse=True)[0]
        yield str(currently)

    def ordered_list(scale, width):
        global status
        # create a list of points and a list of labels for the chart software to use
        # scale is based on seconds, width is a tuple of (start, end)
        start, end = width

        return status


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def dryer(self):
        global status
        cl = cherrypy.request.json

        print ("got dryer status")
        if cl['status'] == 'on':
            status[datetime.datetime.now()] = 'on'
        elif cl['status'] == 'off':
            status[datetime.datetime.now()] = 'off'

        return "ok"
        
if __name__ == '__main__':
    status = dict()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(DryerStatus())
