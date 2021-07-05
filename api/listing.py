class Listing:
    def __init__(self, id, name, description, floor_area, price, rooms, bathrooms, created_on, latitude, longitude):
        self.id = id
        self.name = name
        self.description = description
        self.floor_area = floor_area
        self.price = price
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.created_on = created_on
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "floor_area": self.floor_area,
            "price": self.price,
            "rooms": self.rooms,
            "bathrooms": self.bathrooms,
            "created_on": self.created_on.isoformat(),
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
