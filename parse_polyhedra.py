import requests
import json
import time


query = """query SpaceLeaderboard($id: Int!, $first: Int, $after: String, $order: LoyaltyPointsRankOrder, $seasonId: Int) 
            {space(id: $id) {id name loyaltyPointsRanks(first: $first, after: $after, order: $order, sprintId: $seasonId) 
            {pageInfo {startCursor endCursor hasNextPage hasPreviousPage __typename} totalCount list 
            {id rank points space { name __typename} address {username id avatar address twitterUserName discordUserName __typename} __typename} __typename} __typename}}"""
variables = {
  "id": "10172",
  "first": 300000,
  "after": "19",
  "order": "Points",
  "seasonId": null
}
headers = {
    'authority': 'graphigo.prd.galaxy.eco',
    'accept': '*/*',
    'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBZGRyZXNzIjoiMHg4NTE3MEEwQmE3NUU4MTRhOEFjQjJFOTgyYkY0RWMyQjM1RjA5ZjkyIiwiTm9uY2UiOiJKV2RxRjQ1RkFQeENqMTIxbCIsImV4cCI6MTY4ODc2MTY0MywiSnd0RXJyb3IiOm51bGx9.c_Pq19PgOgAJwifx3_qFfjNXYkejKT-xL358y1OWMSU',
    'content-type': 'application/json',
    'origin': 'https://galxe.com',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

json_data = {
    'operationName': 'SpaceLeaderboard',
    'variables': {
        'id': '10172',
        'first': 1000,
        'after': '-1',
        'order': 'Points',
        'seasonId': None,
    },
    'query': 'query SpaceLeaderboard($id: Int!, $first: Int, $after: String, $order: LoyaltyPointsRankOrder, $seasonId: Int) {\n  space(id: $id) {\n    id\n    name\n    loyaltyPointsRanks(first: $first, after: $after, order: $order, sprintId: $seasonId) {\n      pageInfo {\n        startCursor\n        endCursor\n        hasNextPage\n        hasPreviousPage\n        __typename\n      }\n      totalCount\n      list {\n        id\n        rank\n        points\n        space {\n          name\n          __typename\n        }\n        address {\n          username\n          id\n          avatar\n          address\n          twitterUserName\n          discordUserName\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
}

def save_json(data_json, name):
    with open(f"{name}.json", "w") as f:
        json.dump(data_json, f)


def main():
    leaderboard_json = {"leaderBoard": []}
    counter = 0
    while True:
        response = requests.post('https://graphigo.prd.galaxy.eco/query', headers=headers, json=json_data)
        print(response.status_code)
        response_json = response.json()
        try:
            users = response_json["data"]["space"]["loyaltyPointsRanks"]["list"]
            for user in users:
                user_data = dict()
                user_data["rank"] = user["rank"]
                user_data["points"] = user["points"]
                user_data["address"] = user["address"]["address"]
                user_data["twitter"] = user["address"]["twitterUserName"]
                user_data["discord"] = user["address"]["discordUserName"]
                leaderboard_json['leaderBoard'].append(user_data)
            if response_json["data"]["space"]["loyaltyPointsRanks"]["pageInfo"]["hasNextPage"] == True:
                json_data['variables']['after'] = str(int(json_data['variables']['after']) + 1000)
            else:
                break
        except:
            print(response_json)
    save_json(leaderboard_json, "data")


if __name__ == "__main__":
    main()
