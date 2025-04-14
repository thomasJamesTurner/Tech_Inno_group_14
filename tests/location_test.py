from flighttracker.location import Location

def test_distance_to():
    point = Location(0,0)
    assert point.distance_to(Location(6,0)) == 6