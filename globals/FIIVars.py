import threading

class FIIVars:
    """ All variables that are globals to elsewhere in the program """
    downloaderBusy = threading.Condition()
    uploaderBusy = threading.Condition()
    uploading = False
    stop = False