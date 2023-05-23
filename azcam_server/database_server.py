"""
Contains the azcam database class for azcamserver.

There is only one instance of this class which is referenced as `azcam.db` and contains
temporary data for this current process.
"""

from azcam.database import AzcamDatabase
from azcam_server.parameters_server import ParametersServer
from azcam.logger import Logger
from azcam_server.cmdserver import CommandServer


class AzcamDatabaseServer(AzcamDatabase):
    """
    The azcam database class.
    """

    parameters: ParametersServer
    """parameters object"""

    headers: dict
    """header objects"""

    headerorder: list
    """header order in image header"""

    logger: Logger
    """logger object"""

    cmdserver: CommandServer
    """system header object"""
