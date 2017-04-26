#-*- coding: utf-8 -*-

import datetime
import time
import os
import errno

class DronePicture:
    """
    Prise de Photos --> Transmission vers le Server Apache
    """
    def __init__(self, host = None , folder = None):
        try:
            print("Prendre et transmettre des photos ..")
            self.host = host
            self.folder = folder
        except Exception as x:
            print(x)

    """
        Fonction de création de photos
        Retourne une dictionnaire value qui contient le path, le nom et la date_heure dont la photo a été générée
        l'objet 'value' sera complété au moment de faire le post vers Apache
            value["position"]
            value["position_pts"]
    """
    def createPicture(self, NamePicture = "Drone", Intervention = 1, Extension = "png"):
        try:
            value = {}
            print("Drone Project : Creating picture ...")
            import gtk.gdk
            w = gtk.gdk.get_default_root_window()
            sz = w.get_size()
            print ("The size of the window is %d x %d" % sz)
            pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
            pb = pb.get_from_drawable(w, w.get_colormap(), 0, 0, 0, 0, sz[0], sz[1])
            if (pb != None):
                datepicture = str(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%Z"))
                filename = "./"+str(Intervention)+"/"+str(NamePicture)+"_"+str(datepicture)+"."+str(Extension)
                if not os.path.exists(os.path.dirname(filename)):
                    try:
                        os.makedirs(os.path.dirname(filename))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                pb.save(filename, str(Extension))
                value["path"] = filename
                value["date_heure"] = datepicture
                value["nom"] = NamePicture
                print "Screenshot saved to " + str(NamePicture)+"."+str(Extension)
                print(value)
                return value
            else:
                print "Unable to get the screenshot."
        except Exception as x:
            print(x)
    """
        Notification de NodeJS sur l'objet Photo
    """
    def notifyNodeJS(self):
        try:
            print("Notifying NodeJS for new Photo Object ...")
        except Exception as x:
            print(x)

    """
        Posting the generated picture to the Apache server
    """
    def postPicture(self):
        try:
            print("Posting the generated picture to apache server ...")
        except Exception as x:
            print(x)

    """
        Fonction de prise de photos depuis un dossier
    """
    def getPicture(self,folder,filename):
        try:
            print("Getting picture..")
        except Exception as x:
            print(x)


dronepic = DronePicture()
dronepic.createPicture()
#dronepic.postPicture()