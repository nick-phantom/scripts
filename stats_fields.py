import requests
import json
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#####
url = "https://phantom.us"
username = "admin"
password = "password"
verify_certificate = False
#####

if len(sys.argv) != 3:
    print("Error running script")
    print("Example: phenv python stats.py 2020-03-01 2020-06-24 ")
    sys.exit(0)

start_date = sys.argv[1]
end_date = sys.argv[2]

print("Using the following link in your browser copy the contents into the section below")
print("{}/custom_container_fields/".format(url))
fields_data = raw_input("Output from browser: ")

field_names = []
print("\n\n")
fields_data = json.loads(fields_data)
fields_data = fields_data["global"]["fields"]

for key, value in fields_data.iteritems():
    print("Event count for: {}".format(key))
    for i in value["values"]:
        request_url = "{}/rest/container/?page=0&page_size=10&sort=id&order=desc&_filter_container_type=%22default%22&_filter_custom_fields__{}=%22{}%22".format(url, key, i)
        r = requests.get(request_url, auth=(username,password), verify=verify_certificate).json()
        print("{}: {}".format(i, r["count"]))
