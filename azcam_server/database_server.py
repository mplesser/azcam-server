"""
Contains the azcam database class for azcamserver.

There is only one instance of this class which is referenced as `azcam.db` and contains
temporary data for this current process.
"""

from dataclasses import dataclass, field

from typing import Any, Union

from azcam.database import AzcamDatabase
from azcam.logger import Logger
from azcam_server.parameters_server import ParametersServer
from azcam_server.cmdserver import CommandServer


class AzcamDatabaseServer(AzcamDatabase):
    """
    The azcam database class.
    """

    headers: dict = {}
    """header objects"""

    headerorder: list = []
    """header order in image header"""

    logger: Logger = Logger()
    """logger object"""

    parameters: ParametersServer = None
    """parameters object"""

    cmdserver: CommandServer = None
    """system header object"""


@dataclass
class Database:
    """
    AzCam server database dataclass.
    """

    tools: dict[str, int] = field(default_factory=dict)

    #: working folder
    wd: str = ""  #:working folder

    def get(self, name: str) -> Any:
        """
        Returns a database attribute by name.
        Args:
          name: name of attribute to return
        Returns:
          value or None if *name* is not defined
        """

        try:
            obj = getattr(self, name)
        except AttributeError:
            obj = None

        return obj

    def set(self, name: str, value: Any) -> None:
        """
        Sets a database attribute value.
        Args:
          name: name of attribute to set
          value: value of attribute to be set
        """

        # if not hasattr(self, name):
        #    return

        setattr(self, name, value)

        return
