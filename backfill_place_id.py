import os
from google.cloud import datastore

client = datastore.Client(os.environ["VOTE_HAVERHILL_PROJECT"])

i = 0
for voter in client.query(kind="Voter").fetch():
    print i
    voter["place_id"] = None
    client.put(voter)
    i += 1
