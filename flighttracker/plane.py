from enum import Enum

class Plane_Status(Enum):
    GROUNDED        = 0
    IN_MAINTENENCE  = 1
    FLIGHT_READY    = 2


    
    
class Plane:
    model = ""
    passener_capacity = 0
    cargo_capacity = 0
    current_status = Plane_Status(0)

    def __init__(self,model,passenger_cap,cargo_cap):
        self.model = model
        self.passener_capacity = passenger_cap
        self.cargo_capacity = cargo_cap
        self.current_status = Plane_Status.GROUNDED

    def update_status(self ,status):
        self.current_status = status
