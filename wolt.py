import json
import requests


class Wolt:
    HEADERS = {
        'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.68 Safari/537.36'
    }

    PLACES_URL = 'https://restaurant-api.wolt.com/v1/google/places/autocomplete/json'
    GOOGLE_GEOCODE_URL = 'https://restaurant-api.wolt.com/v1/google/geocode/json'
    DELIVERY_URL = 'https://restaurant-api.wolt.com/v1/pages/delivery'

    def get_matching_cities(self, street):
        """
        :param street: a street name
        :return: a list of dictionaries containing the all the cities that has the passed street name and its id
        """
        params = {'input': street}
        response = json.loads(requests.get(self.PLACES_URL, headers=self.HEADERS, params=params).text)
        predictions = response['predictions']

        return [
            {
                'street': result['description'],
                'place_id': result['place_id']} for result in predictions] if response else None

    def get_lat_lon(self, city_id):
        """
        :param city_id: the ID of the city you want to get the latitude and longitude of
        :return: dictionary containing the lat and lon of the
        """
        params = {'place_id': city_id}
        response = json.loads(requests.get(self.GOOGLE_GEOCODE_URL, headers=self.HEADERS, params=params).text)
        lat_lon = response['results'][0]['geometry']['location']
        return lat_lon

    def get_nearby_restaurants(self, lat, lon):
        """
        :param lat: latitude of the street
        :param lon: longitude of the street
        :return: list of dictionaries containing all the available information about nearby restaurant
        """
        params = {'lat': lat, 'lon': lon}
        response = requests.get(self.DELIVERY_URL, headers=self.HEADERS, params=params).text
        restaurants = json.loads(response)['sections'][0]['items']
        return restaurants


if __name__ == '__main__':
    wolt = Wolt()

    # Get the matching streets
    cities = wolt.get_matching_cities('Allenby')

    # Select the first place (Allenby, Tel-Aviv Yafo)
    # and get the latitude and longitude of it
    city = cities[0]['place_id']
    lat_lon = wolt.get_lat_lon(city)

    # Pass the latitude and longitude to get all nearby restaurants
    restaurants = wolt.get_nearby_restaurants(lat_lon['lat'], lat_lon['lng'])
    print(restaurants)
