import json
from json2html import *
from datetime import datetime, date
from flightData import *
from exceptions.WronInputException import WIException

thismodule = sys.modules[__name__]


# ####################################################################################################################
# ############################################### HELPER FUNCTIONS ###################################################
# ####################################################################################################################
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    raise TypeError("Type %s not serializable" % type(obj))


def place_search_into_excel(res, name):
    """funciton to put the raw search result into an excel: sorting reasons, etc -- NOT TRANSPOSING URL"""
    jsn = json.loads(res)
    for i in range(0, len(jsn['data'])):
        for l in range(0, len(jsn['data'][i]['route'])):
            for delFromR in range(0, len(delFromRoute)):
                del jsn['data'][i]['route'][l][delFromRoute[delFromR]]
        for k in range(0, len(toDeleteLocal)):
            del jsn['data'][i][toDeleteLocal[k]]
    import pandas as pd
    pd.read_json(json.dumps(jsn['data'])).to_excel('excels/' + name + '.xlsx')


# ####################################################################################################################
# ############################################ DOC_CREATOR FUNCTIONS #################################################
# ####################################################################################################################
def fly_from_to(src=None, dst=None, dates=None, filters=None):
    """function to create a html file with a combination of every flight from the src array with the to array
    between dates[0] - flight date and dates[1] - fly back time with a specific COMMON characteristic: using the
    filter functions - USE AS MANY AS WANTED

    !!! using explicitly the function: filters need to have the SPECIFIC form: ['name', 'index_value']"""
    if filters is None:
        filters = []
    if src != [''] and dst != [''] and len(dates) == 2 and dates[0] != '' and dates[1] != '':
        fn = " & ".join(src) + " -- " + " & ".join(dst) + " -- " + dates[0].replace("/", "-") + "~" + dates[1].replace(
            "/", "-")
        import os
        fl = "flights\\" + fn + ".html"
        # print(fl, os.path.exists(fl))
        if os.path.exists(fl):
            os.remove(fl)

        from kiwicom import kiwi
        # configure kiwi
        kiwi.configure_structlog()
        # set up kiwi search
        ss = kiwi.Search()
        flightData.update({"date_from": dates[0]})
        flightData.update({'date_to': flightData.get('date_from')})
        flightData.update({"return_from": dates[1]})
        flightData.update({'return_to': flightData.get('return_from')})
        for s in range(0, len(src)):
            update_element('fly_from', src[s])
            for d in range(0, len(dst)):
                update_element('fly_to', dst[d])
                res = ss.search_flights(**flightData).text
                if len(filters) != 0:
                    for i in range(0, len(filters)):
                        myModule = getattr(thismodule, filters[i][0])
                        json_html(json.loads(res), fn,
                                  index=[myModule(json.loads(res), filters[i][1])],
                                  subtitle=filters[i][0] + " >> from " + src[s] + ", to " + dst[d] +
                                  " between: " + dates[0] + " <-> " + dates[1])
                else:
                    json_html(json.loads(res), fn)
        # successful finishing note
        # print("DONE")
    else:
        raise WIException("WRONG INPUT DATA!")


def json_html(parsed_json, filename, index=None, subtitle=None):
    """create the whole HTML document of the result: index: place all the select functions inside
    html will result in reversed order

    !!! using explicitly the function: filters have default index value of 0"""
    # delete unwanted items to get into the html
    if index is None:
        index = []
    for i in range(0, len(toDeleteGlobal)):
        try:
            del parsed_json[toDeleteGlobal[i]]
        except Exception:
            pass
    for i in range(0, len(parsed_json['data'])):
        for l in range(0, len(parsed_json['data'][i]['route'])):
            pass
            for rl in range(0, len(parsed_json['data'][i]['route'])):
                try:
                    for delFromR in range(0, len(delFromRoute)):
                        del parsed_json['data'][i]['route'][rl][delFromRoute[delFromR]]
                except Exception:
                    pass
        # make links accessible by html
        link = parsed_json['data'][i]['deep_link']
        parsed_json['data'][i]['deep_link'] = "<a href=\"" + link + "\">kiwi.com link</a>"
        for k in range(0, len(toDeleteLocal)):
            try:
                del parsed_json['data'][i][toDeleteLocal[k]]
            except Exception:
                pass

    # apply filters from the index -- FILTERS MIGHT GENERATE MORE ANSWERS
    sub = ""
    if len(index) == 0:
        pass
    else:
        val = 0
        for i in range(0, len(index)):
            lst = index[i]
            for j in range(0, len(lst)):
                parsed_json['data'].insert(0, parsed_json['data'][lst[j] + val])
                val = val + 1
                sub = subtitle

        for i in range(0, len(parsed_json['data']) - len(index) - val):
            del parsed_json['data'][len(index) + val]
        del parsed_json['data'][val]
    # ORDERING BY PRICE ASCENDING !!
    from copy import deepcopy
    sorted_obj = deepcopy(parsed_json)
    sorted_obj['data'] = sorted(parsed_json['data'], key=lambda x: x['price'], reverse=False)
    parsed_json['data'] = sorted_obj['data']
    # swap to make correct order
    cr = parsed_json['currency']
    sp = parsed_json['search_params']
    parsed_json['currency'] = parsed_json['data']
    parsed_json['data'] = cr
    parsed_json['search_params'] = parsed_json['currency']
    parsed_json['currency'] = sp
    # place new in file + format to utf-8
    fl = "flights\\" + filename + ".html"
    f = open(fl, 'a', encoding='utf-8')
    # add subtitle
    f.write('<br><br><b><font size="+2">&#9992; {}</font></b><br><br>'.format(sub))
    f.write(json2html.convert(json=json.dumps(parsed_json)))
    f.close()
    filedata = open(fl, 'r', encoding='utf-8').read()
    filedata = filedata.replace("&lt;", "<")
    filedata = filedata.replace("&quot;", "\"")
    filedata = filedata.replace("&gt;", ">")
    f = open(fl, 'w', encoding='utf-8')
    f.write(filedata)
    f.close()


# ####################################################################################################################
# ############################################### FILTER FUNCTIONS ###################################################
# ####################################################################################################################
def price_bag_index_added(parsed_json, index=0):
    """filter from the results the flight with the lowest price + additional_bag_no_index
    index 0 means no additional baggage: lowest price
    if index is bigger than any possible index in the list: lowest price"""
    winningIndex = []
    minValue = 99999999
    lower = 0
    for length in range(0, len(parsed_json['data'])):
        # add flight with not so many bags as requested
        if len(parsed_json['data'][length]['bags_price']) < int(index):
            lower += 1
        if len(parsed_json['data'][length]['bags_price']) >= int(index) and index != 0:
            if minValue > parsed_json['data'][length]['price'] + parsed_json['data'][length]['bags_price'][str(index)]:
                minValue = parsed_json['data'][length]['price'] + parsed_json['data'][length]['bags_price'][str(index)]
                winningIndex = [length]
            elif minValue == parsed_json['data'][length]['price'] + \
                    parsed_json['data'][length]['bags_price'][str(index)]:
                winningIndex.append(length)
        if lower == len(parsed_json['data']) or index == 0:
            winningIndex = [0]
    return winningIndex


def fly_duration(parsed_json, index):
    """filter from the results the flight based on the fly_duration
    - index == 0: fastest fly_duration
    - index == 1: slowest fly_duration"""
    winning_indexes = []

    if not index:
        min_value = "9959"
        for item in range(0, len(parsed_json['data'])):
            # create the comparable value
            actual_value = create_actual_value(parsed_json['data'][item]['fly_duration'])
            if int(min_value) > int(actual_value):
                min_value = actual_value
                winning_indexes = [item]
        # create the list of every element which is the lowest fly duration
        for item in range(0, len(parsed_json['data'])):
            # create the comparable value
            actual_value = create_actual_value(parsed_json['data'][item]['fly_duration'])
            if int(min_value) == int(actual_value):
                winning_indexes.append(item)
                # make unique elements
                winning_indexes = list(set(winning_indexes))
        return winning_indexes
    # TODO: make a list of lowest/highest number -> depending on index parameter
    # TODO: and check again the baggage function
    # TODO: check for possible other functions


def create_actual_value(flight_duration):
    """function to create a unified value from the format xh ym => two_digit_hours & two_digit_minutes"""
    hours_n_minutes = flight_duration.split(" ")
    # transform the hours in a good format
    hours_n_minutes[0] = hours_n_minutes[0].replace("h", "")
    if len(hours_n_minutes[0]) == 1:
        hours_n_minutes[0] = "0" + hours_n_minutes[0]

    # transform the minutes in a good format
    hours_n_minutes[1] = hours_n_minutes[1].replace("m", "")
    if len(hours_n_minutes[1]) == 1:
        hours_n_minutes[1] = "0" + hours_n_minutes[1]
    # final version of the number
    return hours_n_minutes[0] + hours_n_minutes[1]
