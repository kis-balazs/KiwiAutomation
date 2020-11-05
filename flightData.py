# values to be taken out/modified from the HTML file
toDeleteGlobal = ['search_id', 'currency_rate', 'connections', 'time', 'fx_rate', 'refresh', 'del', 'ref_tasks',
                  'all_stopover_airports', 'all_airlines']

toDeleteLocal = ['id', 'dTime', 'aTime', 'dTimeUTC', 'aTimeUTC', 'mapIdfrom', 'mapIdto',
                 'pnr_count', 'found_on', 'booking_token', 'quality', 'type_flights', 'p1', 'p2', 'p3', 'duration',
                 'virtual_interlining', 'transfers', 'technical_stops', 'cityCodeFrom', 'cityCodeTo', 'flyFrom',
                 'flyTo', 'routes']
delFromRoute = ['id', 'combination_id', 'return', 'original_return', 'source', 'found_on', 'fare_classes',
                'fare_family', 'mapIdto', 'mapIdfrom', 'fare_basis', 'fare_category', 'last_seen',
                'refresh_timestamp', 'guarantee', 'aTime', 'dTime', 'aTimeUTC', 'dTimeUTC', 'cityCodeFrom',
                'cityCodeTo', 'operating_carrier', 'equipment', 'latFrom', 'lngFrom', 'latTo', 'lngTo',
                'operating_flight_no']


flightData = {}

# Kiwi api ID of the departure location.
flightData.update({'fly_from': 'CLJ'})
# Kiwi api ID of the arrival destination.
flightData.update({'fly_to': 'CVG'})
# geographical data API version.
flightData.update({'v': '3'})
# search flights from this date (dd/mm/YYYY).
flightData.update({'date_from': '20/10/2019'})
# search flights upto this date (dd/mm/YYYY).
flightData.update({'date_to': flightData.get('date_from')})
# min return date of the whole trip (dd/mm/YYYY).
flightData.update({'return_from': '30/10/2019'})
# max return date of the whole trip (dd/mm/YYYY).
flightData.update({'return_to': flightData.get('return_from')})
# the minimal length of stay in the destination given in the fly_to parameter.
flightData.update({'nights_in_dst_from': ''})
# the maximal length of stay in the destination given in the fly_to parameter.
flightData.update({'nights_in_dst_to': ''})
# max flight duration in hours, min value 0.
flightData.update({'max_fly_duration': '0'})
# switch for oneway/round flights search - will be deprecated in the near future
# (until then, you have to use the round parameter if one from the nights_in_dst of return date parameters is given.)
flightData.update({'flight_type': 'return'})
# returns the cheapest flights to every city covered by the to parameter.
flightData.update({'one_for_city': '0'})
# returns the cheapest flights for one date.
flightData.update({'one_per_date': '0'})
# Used to specify the number of adults.
flightData.update({'adults': '1'})  # todo change here for number
# It is used to specify the number of children.
flightData.update({'children': ''})
# It is used to specify number of infants.
flightData.update({'infants': ''})
# This parameter is used to specify the preferred classes.
# M (economy), W (economy premium), C (business), F (first class).
flightData.update({'selected_cabins': 'M'})
# This parameter allows the client to specify and combine two different classes in their request.
flightData.update({'mix_with_cabins': ''})
# Number of adult hold bags separated by commas.
flightData.update({'adult_hold_bag': ''})
# Number of adult hand bags separated by commas.
flightData.update({'adult_hand_bag': ''})
# Number of child hold bags separated by commas.
flightData.update({'child_hold_bag': ''})
# Number of child hand bags separated by commas.
flightData.update({'child_hand_bag': ''})
# the list of week days for the flight, where 0 is Sunday, 1 is Monday, etc.
flightData.update({'fly_days': ''})
# type of set fly_days; It is used to specify whether the flight is an arrival or a departure.
flightData.update({'fly_days_type': 'departure'})
# the list of week days for the flight, where 0 is Sunday, 1 is Monday, etc.
flightData.update({'ret_fly_days': ''})
# type of set ret_fly_days; It is used to specify whether the flight is an arrival or a departure.
flightData.update({'ret_fly_days_type': 'arrival'})
# search flights with departure only on working days.
flightData.update({'only_working_days': 'false'})
# search flights with departure only on weekends.
flightData.update({'only_weekends': 'false'})
# partner ID. If present, the result will include a link to a specific trip directly to Kiwi.com,
# with the affiliate ID included (use picky partner ID for testing)
flightData.update({'partner': 'picky'})
# use this parameter to change the currency in the response
flightData.update({'curr': 'EUR'})
# result filter, minimal price
flightData.update({'price_from': ''})
# result filter, maximal price
flightData.update({'price_to': ''})
# result filter, min. departure time (11:00 means 11AM, 23:00 means 11PM)
flightData.update({'dtime_from': ''})
# whether or not to search for connections on different airport, can be set to 0 or 1, 1 is default.
flightData.update({'conn_on_diff_airport': '0'})
# whether or not to search for flights leaving from a different airport than where the customer landed,
# can be set to 0 or 1, 1 is default.
flightData.update({'ret_from_diff_airport': '0'})
# whether or not to search for flights returning to a different airport than the one from where the customer departed,
# can be set to 0 or 1, 1 is default.
flightData.update({'ret_to_diff_airport': '0'})
# a list of airlines (IATA codes) separated by ‘,’ (commas) that should / should not be included in the search
flightData.update({'select_airlines': ''})
# it can be thought of as a switch for the ‘select_airlines’ parameter where ‘False=select’ and ‘True=omit’.
flightData.update({'select_airlines_exclude': 'false'})
# a list of stopover airports (IATA codes) separated by ‘,’ (commas) that should / should not be included.
flightData.update({'select_stop_airport_exclude': 'false'})
# this parameter allows you to specify the vehicle type.
flightData.update({'vehicle_type': 'aircraft'})
# limit number of results; the default value is 200; max is up to the partner (500 or 1000)
flightData.update({'limit': '0'})
# sorts the results by quality, price, date or duration.
flightData.update({'sort': 'price'})


def get_attribute(key):
    return flightData[key]


def print_attributes():
    for i in flightData:
        print(i, "=", flightData[i])


def update_element(key, value):
    if key not in flightData.keys():
        print("CANNOT UPDATE, CHECK KEY:", key, value)
    else:
        flightData.update({key: value})
        print("UPDATED, BEWARE OF POSSIBLE BACKEND CORRECTIONS:",  key, value)
