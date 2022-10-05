import os.path
import requests
import json
import pickle

def distance_diction(req_list,stn_list):
    if not os.path.exists('dist.p'):
        distance_dic = {}

        for req in req_list:
            for st in stn_list:
                distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id:
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)

        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    else:
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        for req in req_list:
            for st in stn_list:
                if dic_key(req.loc, st.loc) not in distance_dic:
                    distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                    distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id and (dic_key(req1.loc, req2.loc) not in distance_dic):
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)

        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    return distance_dic

def get_distance_lat(coord1, coord2):
    if coord2[0] == coord1[0] and coord2[1] == coord1[1]:
        dist = 0

    else:
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        r = requests.get(
            f"http://router.project-osrm.org/route/v1/car/{lon1},{lat1};{lon2},{lat2}?overview=full""")
        routes = json.loads(r.content)
        route_1 = routes.get("routes")[0]
        dist = route_1["distance"]

    return dist / 1000  # Returns in kilometers


def dic_key(coord1, coord2):
    return str(coord1[0]) + str(coord1[1]) + 'to' + str(coord2[0]) + str(coord2[1])
