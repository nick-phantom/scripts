import requests
import json
import sys

#####
url = "https://phantom.us"
username = "admin"
password = "password"
verify_certificate = True
#####

if len(sys.argv) != 3:
    print("Error running script")
    print("Example: phenv python stats.py 2020-03-01 2020-06-24 ")
    sys.exit(0)

start_date = sys.argv[1]
end_date = sys.argv[2]

# get the number of tenants
tenants_list = []
tenants = requests.get("{}/rest/tenant?include_disabled=true&sort=id&order=asc&page_size=5&page=0".format(url), auth=(username, password), verify=verify_certificate).json()

for i in tenants["data"]:
    tenants_list.append(i["id"])

# now that we have tenant id's get a count of events and cases
for i in tenants_list:
    print("Event Count for Tenant {}:".format(str(i)))
    r = requests.get("{}/rest/container?_filter_create_time__range=%22{}%22,%20%22{}%22&_filter_tenant__in=[{}]&_filter_container_type=%22default%22".format(url,start_date, end_date, str(i)), auth=(username, password), verify=verify_certificate).json()
    
    event_count = r["count"]
    print("Events: " + str(event_count))
    
    r = requests.get("{}/rest/container?_filter_create_time__range=%22{}%22,%20%22{}%22&_filter_tenant__in=[{}]&_filter_container_type=%22case%22".format(url,start_date, end_date, str(i)), auth=(username, password), verify=verify_certificate).json()

    case_count = r["count"]
    print("Cases: " + str(case_count))
    total = event_count + case_count
    print("Total: " + str(total) + "\n" )
