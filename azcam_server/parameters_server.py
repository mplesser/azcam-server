"""
Parameter handling tool for azcam-server.
"""

import typing

import azcam
from azcam.parameters import Parameters


class ParametersServer(Parameters):
    """
    Main class for server parameters tool.
    """

    def __init__(self):
        """
        Creates parameters tool, optionally setting default parameter dictionary name.
        """

        Parameters.__init__(self, "azcamserver")

    def get_par(self, parameter: str) -> typing.Any:
        """
        Return the value of a parameter in the parameters dictionary.


        Args:
            parameter (str): name of the parameter

        Returns:
            value (Any): value of the parameter
        """

        parameter = parameter.lower()
        value = None

        # special cases
        if parameter == "imagefilename":
            value = azcam.db.tools["exposure"].get_filename()
            return value
        elif parameter == "imagetitle":
            value = azcam.db.tools["exposure"].get_image_title()
            return value
        elif parameter == "exposuretime":
            value = azcam.db.tools["exposure"].get_exposuretime()
            return value
        elif parameter == "exposurecompleted":
            value = azcam.db.tools["exposure"].finished()
            return value
        elif parameter == "exposuretimeremaining":
            value = azcam.db.tools["exposure"].get_exposuretime_remaining()
            return value
        elif parameter == "pixelsremaining":
            value = azcam.db.tools["exposure"].get_pixels_remaining()
            return value
        elif parameter == "camtemp":
            value = azcam.db.tools["tempcon"].get_temperatures()[0]
            return value
        elif parameter == "dewtemp":
            value = azcam.db.tools["tempcon"].get_temperatures()[1]
            return value
        elif parameter == "temperatures":
            camtemp = azcam.db.tools["tempcon"].get_temperatures()[0]
            dewtemp = azcam.db.tools["tempcon"].get_temperatures()[1]
            return [camtemp, dewtemp]
        elif parameter == "logcommands":
            value = azcam.db.cmdserver.logcommands
            return value
        elif parameter == "wd":
            value = azcam.utils.curdir()
            return value
        elif parameter == "logdata":
            value = azcam.db.logger.get_logdata()
            return value

        # parameter must be in par_table
        try:
            attribute = azcam.db.par_table[parameter]
        except KeyError:
            azcam.AzcamWarning(f"Parameter {parameter} not available for get_par")
            return None

        tokens = attribute.split(".")
        numtokens = len(tokens)

        # a tool and attribute is required
        if numtokens == 1:
            return None

        object1 = tokens[0]

        # object1 must be a tool
        try:
            obj = azcam.db.tools[object1]
            for i in range(1, numtokens):
                try:
                    obj = getattr(obj, tokens[i])
                except AttributeError:
                    pass
            value = obj  # last time is value
        except KeyError:
            value = None

        return value

    def set_par(self, parameter: str, value: typing.Any = None) -> None:
        """
        Set the value of a parameter in the parameters dictionary.

        Args:
            parameter (str): name of the parameter
            value (Any): value of the parameter. Defaults to None.
        Returns:
            None
        """

        parameter = parameter.lower()

        # special cases
        if parameter == "imagefilename":
            azcam.db.tools["exposure"].image.filename = value
            return None
        elif parameter == "imagetitle":
            if value is None or value == "" or value == "None":
                azcam.db.tools["exposure"].set_image_title("")
            else:
                azcam.db.tools["exposure"].set_image_title(f"{value}")
            return None
        elif parameter == "exposuretime":
            azcam.db.tools["exposure"].set_exposuretime(value)
            return None
        elif parameter == "logcommands":
            azcam.db.cmdserver.logcommands = int(value)
            return None
        elif parameter == "wd":
            azcam.utils.curdir(value)
            return None

        # parameter must be in par_table
        try:
            attribute = azcam.db.par_table[parameter]
        except KeyError:
            azcam.AzcamWarning(f"Parameter {parameter} not available for set_par")
            return None

        # object must be a tool
        tokens = attribute.split(".")
        numtokens = len(tokens)
        if numtokens < 2:
            azcam.log("%s not valid for parameter %s" % (attribute, parameter))
            return None

        # first try to set value type
        _, value = azcam.utils.get_datatype(value)
        object1 = tokens[0]

        # run through tools
        try:
            obj = azcam.db.tools[object1]
            for i in range(1, numtokens - 1):
                obj = getattr(obj, tokens[i])
            # last time is actual object
            try:
                setattr(obj, tokens[-1], value)
            except AttributeError:
                pass
                # azcam.AzcamWarning(f"Could not set parameter: {parameter}")
        except KeyError:
            pass
        except Exception:  # new
            pass

        return None

    # TODO - below is for compatibility with azcamtool only - to be removed

    def set_script_par(self, attribute, value, par_dict_id) -> None:
        azcam.db.parameters.par_dict[par_dict_id][attribute] = value
        return

    def get_script_par(self, par_dict_id, attribute) -> typing.Any:
        reply = azcam.db.parameters.par_dict[par_dict_id][attribute]
        return reply
