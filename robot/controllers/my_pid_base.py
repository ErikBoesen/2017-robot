from networktables import NetworkTable

class BasePIDComponent:
    '''
        Base for a component that has a PIDController controlling its output.
        
        readonly variables for subclasses:
        
        * self.enabled: set to True if enabled (only read this)
        * self.rate: set to the calculated rate if enabled, None otherwise
        
        variables that subclasses should set:
        
        * self.setpoint: must be set each period to enable the controller
        
        # TODO: add a 'settle time' output variable
    '''
    
    ramp = 0.1
    
    MIN_RAW_OUTPUT = -1.0
    MAX_RAW_OUTPUT = 1.0
    
    def __init__(self, pid_input, table_name):
        
        self.enabled = False
        self.rate = None
        
        self.err = 0
        
        self._has_setpoint = False
        self._setpoint = None
        
        self._pid_input = pid_input
        
        self._min = -1.0
        self._max = 1.0
  
    @property
    def setpoint(self):
        return self._setpoint
    
    @setpoint.setter
    def setpoint(self, value):
        self._setpoint = value
        self._has_setpoint = True
        
    def compute_error(self, setpoint, pid_input):
        return setpoint - pid_input
    
    def pidWrite(self, output):
        self.rate = output
        
    def set_output_range(self, min, max):
        self._min = min
        self._max = max
        
        
    def execute(self):
        
        if self._has_setpoint:
            
            if not self.enabled:
                self.enabled = True
                self._last_output = 0
                self._last_err = 0
                self.err = 0
            
            # homemade PID
            err = self.compute_error(self._setpoint, self._pid_input())
            if abs(err) < self.kIzone:
                self.err = 0
            else:
                self.err += err
            
            print("Error: ", err, " P: ", self.kP," I: ", self.kI, " D: ", self.kD)
            output = err*self.kP + self.kI*self.err + self.kD*(err - self._last_err)
            output = min(self.MAX_RAW_OUTPUT, max(output, self.MIN_RAW_OUTPUT))
            
            #Scale to min and max output
            #output = ((output - self.MIN_RAW_OUTPUT) / (self.MAX_RAW_OUTPUT - self.MIN_RAW_OUTPUT) * (self._max - self._min)) + self._min
            
            self._last_output = output
            self._last_err = err
            
            self.pidWrite(output)
        
        else:
            if self.enabled:
                #self.pid.disable()
                self.enabled = False
                self.rate = None
        
        self._has_setpoint = False

