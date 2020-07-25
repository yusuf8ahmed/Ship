import sys 

if sys.version_info >= (3, 0):  
    # local imports
    if str(__package__) == "ship":
        # relative import work only when using pip (Or when str(__package__) == "ship")
        # very bad solution
        from .colors import Colors  # Color for terminal

    else:
        # absolute import only when running locally 
        from colors import Colors 
else:
    raise SystemExit("Ship: Python must be greater that version 3") 


class ShipError_(Exception):
    """Custom Exception for Ship

    Args:
        Exception (): Python builtin Exception
    """
    def __call__(self, output_line, cur_line):
        """
        Args:
            output_line (str): [description] a string that show a message
            cur_line (str): (current_line) a string that has the line error happend on 

        Returns:
            SystemExit: this is raised "raise" immediately
        """
        self.output_line = output_line
        self.cur_line = cur_line
        return SystemExit("{}Ship Error{}: line {}: {}".format(Colors.Red, Colors.Reset, self.cur_line, self.output_line))
    
class ShipPrint_():
    """Custom Print for Ship

    Args:
        Exception (): Python builtin Exception
    """
    def __call__(self, message):
        """Custom Print for Ship

        Args:
            message_line (str): a string that show the message
        """
        self.message = message
        print("{}Ship{}: {}".format(Colors.Blue, Colors.Reset,self.message))
        
class ShipExit_(Exception):
    """Custom Exit for Ship

    Args:
        Exception (): Python builtin Exception
    """
    def __call__(self, message):
        """Custom Print for Ship

        Args:
            message_line (str): a string that show the message
        """
        self.message = message
        raise SystemExit("{}Ship{}:{}".format(Colors.Blue, Colors.Reset, self.message))
        
    
ShipError = ShipError_() 
ShipPrint = ShipPrint_() 
ShipExit = ShipExit_()