from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Any-user")
location = geolocator.reverse("25.122222, 55.135497")
print(location.address)
