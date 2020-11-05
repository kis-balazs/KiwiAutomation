from kiwicom import kiwi
from my_kiwi import *

# configure kiwi
kiwi.configure_structlog()
# set up kiwi search
s = kiwi.Search()
# print the current flightData attributes
# printAttributes()

# ################################################################################################################
# sample for jsonHTML -- function
# updateElement('fly_to', 'OTP')
# res = s.search_flights(**flightData).text
# jsonHTML(json.loads(res), "samplejson", index=[])
# jsonHTML(json.loads(res), "samplejsonHTMLbags", index=[
#     lowestPrice_bagIndex_added(json.loads(res), 1)])
# jsonHTML(json.loads(res), "samplejsonHTMLfly", index=[
#     lowestFly_duration(json.loads(res))])
# ################################################################################################################
# ################################################################################################################
# sample for from_multiple_to_multiple -- function
# from_multiple_to_multiple("sampleMFMTCC", src=['CLJ', 'SBZ'], dst=['OTP', 'BUD'],
#                           dates=['20/10/2019', '25/10/2019'],
#                           index=[['lowest_price_bag_index_added', 1],
#                                  ['lowest_price_bag_index_added', 1],
#                                  ['lowest_fly_duration', 0]])
# ################################################################################################################
# ################################################################################################################
# place search into excel
# placeSearchIntoExcel(s.search_flights(**flightData).text, "sampleSearch")
# ################################################################################################################
# ################################################################################################################
# ################################################################################################################
# sample for multFromMultTo -- function
# fly_from_to(src=['CLJ'], dst=['LHR'], dates=['11/11/2020', '21/11/2020'],
#             filters=[['price_bag_index_added', 2],
#                      ['fly_duration', 0]])
fly_from_to(src=['CLJ'], dst=['LHR'], dates=['6/11/2020', '13/11/2020'],
            filters=[['fly_duration', 0]])
