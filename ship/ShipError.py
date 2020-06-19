class ShipError_(Exception):
    """Custom Execption for Ship

    Args:
        Exception (): Python builtin Execption
    """
    def __call__(self, output_line, cur_line):
        self.output_line = output_line
        self.cur_line = cur_line
        return SystemExit("Ship Error: line {}: {}".format(self.cur_line, self.output_line))
    
ShipError = ShipError_()  