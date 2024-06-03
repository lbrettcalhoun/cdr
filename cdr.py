from voipms import VoipMs
from datetime import datetime, timedelta
import json
import requests
import keys

StartDay = str((datetime.now() - timedelta(days=7)).date())
EndDay = str((datetime.now() - timedelta(days=0)).date())
i = 0
cdrList = []
countries = {'US', 'CA'};
additional_params = {'country' : countries}

class IPQS:
    key =  keys.IPQS_KEY
    def phone_number_api(self, phonenumber: str, vars: dict = {}) -> dict:
        url = 'https://www.ipqualityscore.com/api/json/phone/%s/%s' %(self.key, phonenumber)
        x = requests.get(url, params = vars)
        return (json.loads(x.text))

# Create a Client object
client = VoipMs(keys.VOIP_EMAIL,keys.VOIP_KEY)

# Create IPQS object
ipqs = IPQS()

# Get the CDR
try:
    res = client.calls.get.cdr(date_from=StartDay, date_to=EndDay,timezone=-4,answered=True,noanswer=True,busy=True,failed=True)
except TypeError as terr:
    print (f"No calls")
    wait = input("Press any key to quit:")
    exit (0)
except Exception as err: 
    print (f"Unexpected {err=}, {type(err)=}")
    wait = input("Press any key to quit:")
    exit (2)
else:  
    print ("CDR Request Status: " + res["status"])

print()
print(f'{"ID":4}{"Date":20}{"Caller":48}{"Destination":16}{"Disposition":12}{"Duration":8}')

for rec in res["cdr"]:
    caller = rec["callerid"]
    if caller[0] == '"':
        caller = caller.rsplit("<",1)[1].strip(">")
    cdrList.insert(i, caller)
    print (f'{str(i):4}{rec["date"]:20}{rec["callerid"]:48}{rec["destination"]:16}{rec["disposition"]:12}{rec["duration"]:8}')
    i = i + 1

print()
num = input("Enter ID to investigate or 'q' to quit: ")

while num != "q":
    num = int(num)
    phonenumber = cdrList[num]
    result  = ipqs.phone_number_api(phonenumber, additional_params)
    if 'success' in result and result['success']:
        print(f'{"Number: ":10}{result["formatted"]:20}')
        print(f'{"Format: ":10}{result["local_format"]:20}')
        print(f'{"Name: ":10}{result["name"]:20}')
        print(f'{"Carrier: ":10}{result["carrier"]:20}')
        print(f'{"Type: ":10}{result["line_type"]:20}')
        print(f'{"State: ":10}{result["region"]:20}')
        print(f'{"City: ":10}{result["city"]:20}')
        print(f'{"Fraud: ":10}{result["fraud_score"]:3}')
        print(f'{"Risky: ":10}{result["risky"]:1}')
        print(f'{"Abuse: ":10}{result["recent_abuse"]:1}')
        print(f'{"Spammer: ":10}{result["spammer"]:1}')
        print(f'{"Status: ":10}{result["active_status"]:20}')
        print(f'{"Request: ":10}{result["request_id"]:20}')
    num = input("Enter ID to investigate or 'q' to quit: ")
exit (0)