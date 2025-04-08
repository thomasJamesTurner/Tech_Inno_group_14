import location
class Airport(location.Location):
    name = ""
    IATA_code = ""
    ICAO_code = ""
    runways = 0
    security_capacity = 0
    def __init__(self, longitude, latitude,name,IATA,ICAO,runways,security_cap):
        super().__init__(longitude, latitude)
        self.name = name
        self.IATA_code = IATA
        self.ICAO_code = ICAO
        self.runways = runways
        self.security_capacity = security_cap
    