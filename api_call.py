import json

import requests
from bs4 import BeautifulSoup as bs
import certifi
import pycurl
from io import BytesIO
from urllib.parse import urlparse, parse_qs
from urllib import parse

api_endpoint = 'https://api.na.mabibase.com/graphql?t=1'
example = "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemName%2C%22Homestead+Subject+Theta+Figure%22%3BUnitPrice%2Clte%2C%22150000000%22%3BListedAfter%2C%221741157552581%22&sort=ItemName%3AAscending"


def get_item_results(target_url):
    parsed_url = urlparse(target_url)
    query = parse_qs(parsed_url.query)
    queryList = query['q'][0].split(";")
    # print(queryList)
    query_dict = {}
    for d in queryList:
        options = d.split(',')
        if len(options) == 2:
            name, value = options
            query_dict[name.strip('"')] = value.strip('"')
        elif len(options) == 3:
            attr, op, value = options
            query_dict['op'] = op
            query_dict['price'] = value.strip('"')
    print(query_dict)

    payload = [{"operationName": "auctionHouseSearch", "variables": {"server": "mabius6", "filters": [
                {"type": "ItemName", "value": query_dict['ItemName']}, {"type": "UnitPrice", "comparator": query_dict['op'], "value": query_dict['price']},
                {"type": "ListedAfter", "value": query_dict['ListedAfter']}], "pagination": {"pageSize": 25, "pageIndex": 0},
                                                                      "sort": {"attribute": "ItemPrice",
                                                                               "direction": "Ascending"}},
                 "extensions": {"persistedQuery": {"version": 1,
                                                   "sha256Hash": "e42f50b9ab00b0e7b820afbaae91c07722178ed6b0d3aa3b578c8cc4edfe3a84"}}}]
    headers = {
        "Content-Type": "application/json"
    }
    # print(payload)

    resp = requests.post(api_endpoint, data=json.dumps(payload), headers=headers)
    resp_json = resp.json()
    print(resp_json)
    data = resp_json[0]['data']['auctionHouse']['results']
    result_set = []
    for item in data:
        # print(item)
        i = {
            'name': item['itemName'],
            'price': f"{int(item['price1']):,}",
            'amount': item['itemInfo']['info']['amount'],
            'endDate': item['endDate']
        }
        result_set.append(i)
    print(json.dumps(result_set, indent=4))
    return result_set



if __name__ == '__main__':
    get_item_results(example)
