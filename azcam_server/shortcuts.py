"""
CLI shortcuts for azcam-server.
"""


import azcam


def sf_server():
    """Shortcut to Set image folder"""

    try:
        folder = azcam.utils.curdir()
        azcam.db.tools["exposure"].folder = folder
    except Exception:
        pass

    return


def gf_server():
    """
    Shortcut to Go to image folder.
    Also issues sav() command to save folder location.
    """

    folder = azcam.db.tools["exposure"].folder
    azcam.utils.curdir(folder)
    azcam.db.wd = folder
    sav_server()

    return


def sav_server():
    """Shortcut for parfile_write() saving current folder in database."""
    azcam.db.parameters.set_par("wd", azcam.utils.curdir())
    azcam.db.parameters.update_pars(1, "azcamserver")
    azcam.db.parameters.write_parfile()

    return None


def pp():
    """Shortcut to toggle cmdserver printing."""

    old = azcam.db.cmdserver.logcommands
    new = not old
    azcam.db.cmdserver.logcommands = new
    print("cmdserver logcommands is now %s" % ("ON" if new else "OFF"))

    return


def wc():
    """Shortcut to toggle webserver command logging to console."""

    old = azcam.db.tools["webserver"].logcommands
    new = not old
    azcam.db.tools["webserver"].logcommands = new
    print("webserver logcommands is now %s" % ("ON" if new else "OFF"))

    return


azcam.db.shortcuts.update({"sav": sav_server, "pp": pp, "sf": sf_server, "gf": gf_server, "wc": wc})
