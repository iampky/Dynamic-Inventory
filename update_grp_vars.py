import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()

auth = HTTPBasicAuth('nexadmin', '#189@Nex3k2')

ansible_headers = {'Content-Type':'application/json'}

netbox_headers = {'Content-Type':'application/json',
                  'Authorization':'Token b8753bb0a6f52c36893314285ce761f369c81810'
}

group_payload = {
    "name": "",
    "description": "imported",
    "variables": ""
}

inventory_payload = {
      "name": "",
      "organization": 3,
      "variables": ""
     }

#------------FETCHING global_vars AND group_vars FROM NETBOX---------------

netbox_vars_url = "http://netbox.nexariacloud.com:8000/api/extras/config-contexts/"
var_response = requests.get(netbox_vars_url, headers=netbox_headers, verify=False)
response_data = var_response.json()
vars_list = response_data["results"]

#------------FETCHING all the inventories to get latest created inventory ID--------------

inv_id = []
inv_name = []
inventory_url = "https://3.82.135.197/api/v2/inventories/"
inventory_response = requests.get(inventory_url, headers=ansible_headers, auth = auth, verify=False)
inventory_data = json.loads(inventory_response.text)
inventory_results = inventory_data["results"]

for inventory in inventory_results:
     inv_id.append(inventory["id"])
     inv_name.append(inventory["name"])
     if ('Dynamic Inventory' in inv_name):
      inventory_name = "Dynamic Inventory"
     
#------------UPDATING group_vars TO SPECIFIC GROUPS--------------

group_url = "https://3.82.135.197/api/v2/inventories/" + str(max(inv_id)) + "/groups/"
groupvar_response = requests.get(group_url, headers=ansible_headers, auth = auth, verify=False)
group_data = json.loads(groupvar_response.text)
groups = group_data["results"]

for result in vars_list:
    name = result["name"]
    var_data = json.dumps(result["data"])

    for group in groups:
     grp_id = group["id"]
     grp_name = group["name"]
     group_vars_url = "https://3.82.135.197/api/v2/groups/"+str(grp_id)+"/"
     group_payload["name"] = grp_name
     if name == "cisco" and grp_name == "cisco":
      group_payload["variables"] = var_data
      grp_response = requests.put(group_vars_url, data=json.dumps(group_payload), headers=ansible_headers, auth=auth, verify=False)
      print(grp_response)
      
     elif name == "juniper" and grp_name == "juniper":
      group_payload["variables"] = var_data
      grp_response = requests.put(group_vars_url, data=json.dumps(group_payload), headers=ansible_headers, auth=auth, verify=False)
      print(grp_response)
    
    #--------------UPDATING global_vars TO THE INVENTORY---------------

    if name == "global_vars":     
     inventory_url = "https://3.82.135.197/api/v2/inventories/" + str(max(inv_id)) + "/"
     inventory_payload["name"] = inventory_name
     inventory_payload["variables"] = var_data
     inventory_vars_response = requests.put(inventory_url, data=json.dumps(inventory_payload), headers=ansible_headers, auth=auth, verify=False)
     print(inventory_vars_response)
    













    #============================================================================================================================
    #grp_response = requests.put(group_vars_url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
    #print(grp_response)
    
    # if name == "cisco":
    #       grp_name = name
    #       payload["name"] = grp_name
    #       payload["variables"] = data
    #       #put group vars to ansible group
    #       #grp_response = requests.put(ansiblegroupurl, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
    #       #print(grp_response)
    # elif name == "juniper":
    #       grp_name = name
    #       payload["name"] = grp_name
    #       payload["variables"] = data
    #       #put group vars to ansible group
    #       #grp_response = requests.put(ansiblegroupurl, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
    #       #print(grp_response)



#--------------------------------------------------------------------
    # elif name == "global_vars":
    #       print(name)
    #       print(result["data"])
    #       #put global vars to ansible inventory
    

#-------------------------------------------------


# inventoryurl = "https://3.82.135.197/api/v2/inventories/27/"
# inventorypayload = {
#     "name": "NetInv",
#     "organization": 3,
#     "variables": ""
# }
# ansible_connection_timeout =  str(ansible_connection_timeout)
# ansible_python_interpreter = str(ansible_python_interpreter)
# ansible_user = str(ansible_user)
# ansible_password = str(ansible_password)


# inventorypayload["variables"] = "---\nansible_connection_timeout: " + ansible_connection_timeout + "\nansible_python_interpreter: " + ansible_python_interpreter + "\nansible_user: " + ansible_user + "\nansible_password: " +ansible_password

# inventory_response = requests.put(inventoryurl, data=json.dumps(inventorypayload), headers=headers, auth=auth, verify=False)
# print(json.dumps(inventorypayload))
# print(inventory_response)
