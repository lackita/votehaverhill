import os, sys, requests, re
from google.cloud import datastore

client = datastore.Client(os.environ["VOTE_HAVERHILL_PROJECT"])

def parse_file(filename, func):
    headers = None
    i = 0
    for line in open(filename, "r"):
        fields = line.strip().split("|")
        if headers:
            print "Row " + str(i)
            func(dict(zip(headers, [unicode(f) for f in fields])))
        else:
            headers = [re.sub(r'[^\x00-\x7F]+',' ', f.strip()) for f in fields]
        i += 1

def save(row):
    key = client.key("Voter", row["Voter ID Number"])

    if not client.get(key):
        voter = datastore.Entity(key)
        row["place_id"] = None
        voter.update(row)
        client.put(voter)

if __name__ == "__main__":
    parse_file(sys.argv[1], save)
