#-*- coding: utf-8 -*-
import datetime
import time
import os
import errno
import sys
import gtk.gdk
import chilkat

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
        Fonction de Prise de photos
        Retourne une dictionnaire value qui contient le path, le nom et la date_heure dont la photo a été générée
        l'objet 'value' sera complété au moment de faire le post vers Apache
            value["position"]
            value["position_pts"]
    """
    def getPicture(self, NamePicture = "Drone", Intervention = 1, Extension = "jpeg"):
        try:
            value = {}
            print("Drone Project : Creating picture ...")
            w = gtk.gdk.get_default_root_window()
            sz = w.get_size()
            print ("The size of the window is %d x %d" % sz)
            pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
            pb = pb.get_from_drawable(w, w.get_colormap(), 0, 0, 0, 0, sz[0], sz[1])
            if (pb != None):
                #Le temps actuel de la prise de photos
                datepicture = str(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%Z"))
                racine = "./"
                suffix = str(Intervention)+"/"+str(NamePicture)+"_"+str(datepicture)+"."+str(Extension)
                filename = racine + suffix
                #Crée le fichier avec son arboresence même s'il n'existe pas
                if not os.path.exists(os.path.dirname(filename)):
                    try:
                        os.makedirs(os.path.dirname(filename))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                #Sauvegarde de la photo prise avec l'extension indiquée
                pb.save(filename, str(Extension))
                value["path"] = filename
                value["date_heure"] = datepicture
                value["nom"] = NamePicture
                print "Screenshot saved to " + os.path.basename(filename)
                self.sendToTheServer(filename, suffix)
                print(value)
                #return value
            else:
                print "Unable to get the screenshot."
        except Exception as x:
            print(x)

    """
        Posting the generated picture to the Apache server
    """
    def sendToTheServer(self, localPath, suffix = None):
        #  Important: It is helpful to send the contents of the
        #  ssh.LastErrorText property when requesting support.
        ssh = chilkat.CkSsh()
        remotePath = "/var/www/html/projet/"
        if suffix == None:
            dstfolder = remotePath
        else:
            dstfolder = remotePath+str(suffix)

        #  Any string automatically begins a fully-functional 30-day trial.
        success = ssh.UnlockComponent("30-day trial")
        if (success != True):
            print(ssh.lastErrorText())
            sys.exit()
        # Connect to an SSH server:
        #  Hostname may be an IP address or hostname:
        hostname = "148.60.11.238"
        port = 22
        success = ssh.Connect(hostname, port)
        if (success != True):
            print(ssh.lastErrorText())
            sys.exit()
        # Wait a max of 5 seconds when reading responses..
        ssh.put_IdleTimeoutMs(5000)
        #  Authenticate using login/password:
        success = ssh.AuthenticatePw("sitproject", "project")
        if (success != True):
            print(ssh.lastErrorText())
            sys.exit()
        try:
            #print(os.path.dirname(dstfolder))
            ssh.quickCommand("mkdir -p "+str(os.path.dirname(dstfolder)), "utf8")
        except Exception as x:
            print(x)
        # Once the SSH object is connected and authenticated, we use it
        #  as the underlying transport in our SCP object.
        scp = chilkat.CkScp()
        success = scp.UseSsh(ssh)
        if (success != True):
            print(scp.lastErrorText())
            sys.exit()
        #remotePath = "/var/www/html/projet/test.txt"
        #localPath = "/home/kirikou/test.txt"
        success = scp.UploadFile(localPath, dstfolder)
        if (success != True):
            print(scp.lastErrorText())
            sys.exit()
        print("SCP upload file success.")
        #  Disconnect
        ssh.Disconnect()

    """
        Notification de NodeJS sur l'objet Photo
    """
    def notifyNodeJS(self):
        try:
            print("Notifying NodeJS for new Photo Object ...")

        except Exception as x:
            print(x)


    """
        Fonction de capture du flux Vidéo - TODO
    """
    def getVideoDrone(self):
        try:
            print("Flux vidéo ...")
        except Exception as x:
            print(x)

    """
    TESTS DE NOTRE MODULE
    """
#Création d'un objet dronepicture
dronepic = DronePicture()
#Génére un screeshot et l'envoi automatiquement vers le serveur apache
#valeur = dronepic.getPicture()
while True:
    dronepic.getPicture()
    #Pause
    time.sleep(10)
#valeur est un objet json du Photo dans la base NodeJS
#print(valeur)