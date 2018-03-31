import os, requests
from google.cloud import datastore

client = datastore.Client(os.environ["VOTE_HAVERHILL_PROJECT"])


def place_id(key, number, name, apt, zip):
    address_parts = [number, name]

    if len(apt) > 0:
        address_parts += ["Apt", apt]

    address_parts += ["Haverhill", "MA", zip[0:5]]

    places = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={
            "query": " ".join(address_parts),
            "key": os.environ["VOTE_HAVERHILL_API_KEY"],
        },
    ).json()

    if len(places["results"]) > 1:
        reduced_places = [p for p in places["results"] if p["name"].split(" ")[0] == number]
        if len(reduced_places) > 1:
            print " ".join([str(x) for x in ["Multiple places", key, number, name, apt, zip, str(places)]])
        places = {"results": reduced_places}
    elif len(places["results"]) == 0:
        print " ".join([str(x) for x in ["No places", key, str(address_parts), str(places)]])

    if len(places["results"]) == 1:
        return places["results"][0]["place_id"]
    else:
        None


if __name__ == "__main__":
    q = client.query(kind="Voter")
    q.add_filter("place_id", "=", None)
    i = 0
    for voter in q.fetch():
        print i
        voter["place_id"] = place_id(
            voter.key,
            voter["Residential Address Street Number"],
            voter["Residential Address Street Name"],
            voter["Residential Address Apartment Number"],
            voter["Residential Address Zip Code"],
        )
        client.put(voter)
        i += 1
