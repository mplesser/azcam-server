"""
*azcam.server* is imported to define server mode, create azcamserver 
parameters dictionary, define a logger, and get local network information.
"""

import socket

import azcam
from azcam.logger import Logger
from azcam_server.parameters_server import ParametersServer
from azcam_server.database_server import AzcamDatabaseServer
from azcam_server.cmdserver import CommandServer

azcam.db = AzcamDatabaseServer()  # overwrite azcamdatabase

# server mode
azcam.db.set("servermode", "")

# parameters
azcam.db.parameters = ParametersServer()

# logging
azcam.db.logger = Logger()
azcam.log = azcam.db.logger.log  # to allow azcam.log()

# save this machine's hostname and ip address
hostname = socket.gethostname()
azcam.db.set("hostname", hostname)
azcam.db.set("hostip", socket.gethostbyname(hostname))

# tool_id's which are reset or initialized with exposure
azcam.db.set("tools_reset", {})
azcam.db.set("tools_init", {})

# command server
azcam.db.cmdserver = CommandServer()
