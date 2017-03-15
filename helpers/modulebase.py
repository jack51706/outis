
from helpers.log import print_error


class ModuleBase:
    """
    Base class for all modules (handler, transport, platform, ...)
    Allows functions for options
    """

    def __init__(self):
        """
        Initialize Module, should be overwritten and options should be added
        """
        
        self.options = {}
    
    def setoption(self, name, value):
        """
        Sets option <name> to value <value> if possible.
        Can be overwritten and expanded by modules.
        """
        
        # name and value must be set and must be string
        if not name or not isinstance(name, str):
            print_error("Option name not understood")
            return False
        if not value or not isinstance(value, str):
            print_error("Option value not understood")
            return False

        # check whether there is an option of that name
        if name and isinstance(name, str) and name.upper() in self.options:

            values = self.options[name.upper()]

            # if it is an option with fixed values, check whether the value matches
            if 'Options' in values and values['Options'] and not(value.upper() in values['Options']):
                print_error(str(name.upper())+" must be one of "+(", ".join(values['Options'])))
                return True  # ok, strange, but True only means we found it, even if setting failed
            elif 'Options' in values and values['Options']:
                # and if so, set the value to upper case
                value = value.upper()

            # finally set the value
            self.options[name.upper()]['Value'] = value
            return True
        else:
            # no option of that name here
            # no error now, module should catch that
            return False

    def validate_options(self):
        """
        Validate all currently set module options.
        Can be overwritten and expanded by modules.
        """
        
        valid = True

        # check for each option
        for option, values in self.options.items():
            # make sure all options are set
            if values['Required'] and not(values['Value']) or (values['Value'] == ''):
                print_error(str(option)+" must be set")
                valid = False
            # make sure all options with listed alternatives are correct
            if 'Options' in values and values['Options'] and not(values['Value'] in values['Options']):
                print_error(str(option)+" must be one of "+(", ".join(values['Options'])))
                valid = False

        return valid

