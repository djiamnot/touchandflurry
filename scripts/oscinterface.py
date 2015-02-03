import bge
import liblo
import sys


class OSCinterface():
    """
    Handle OSC communication
    """
    def __init__(self, logic, port=10000):
        """
        @param port: OSC UDP port number
        @type _context: object to send OSC messages to
        @return L{liblo.ServerThread}
        """
        print("starting OSC server thread")
        self.logic = logic
        self.server = liblo.Server(port)
        self.registerCallbacks()

    def registerCallbacks(self):
        self.server.add_method("/acc", "fff", self.accCallback)
        self.server.add_method("/orientation", "fff", self.orientCallback)
        self.server.add_method(None, None, self.fallback)

    def accCallback(self, path, args):
        print("accelerator", args)
        self.logic.globalDict['intonaData']["accel_x"] = args[0]
        self.logic.globalDict['intonaData']["accel_y"] = args[1]
        self.logic.globalDict['intonaData']["accel_z"] = args[2]


    def orientCallback(self, path, args):
        print("orientation", args)
        self.logic.globalDict['intonaData']["pitch"] = args[0]
        self.logic.globalDict['intonaData']['roll'] = args[1]
        self.logic.globalDict['intonaData']['yaw'] = args[2]

    def fallback(self, path, args):
        print ("received unknown message {0} ~ {1}".format(path, args))

    def recv(self, timeout):
        try: 
            self.server.recv(timeout)
        except Exception as e:
            print("can't receive because: {}".format(e))
        #self._context.updateContext(self._context)

    def stop(self):
        self.server.free()
        del self.server
