import urllib3, certifi
import csv, json

TOKEN = 'efc6e2e34663885dcd891bb7cd157b8ae8c5ddeed5dbe754c90b07a4c42e574d'
SECRET = '7e04cb5c66c9309a470f945bb3109919dca71e485de3d7095cd8548d89b1f890'


def People_Out(json_data, writer, linenbr):
    
    people_elems = json_data['data']
    for person in people_elems:
        attribs = person['attributes']

        if linenbr == 0:
            header = ['PersonID','First','Last','FullName']
            writer.writerow(header)
            linenbr += 1
        
        writer.writerow([person['id'],attribs['first_name'],attribs['last_name'],attribs['name']])

if __name__ == '__main__':

    # open a file for writing
    people_out = open('People.csv', 'w')
    # create the csv writer object
    csvwriter = csv.writer(people_out, lineterminator='\n')

    #Set up for HTTPS using basic authentication
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    req_header = urllib3.util.make_headers(basic_auth=TOKEN + ":" + SECRET)

    #Write heading row for the CSV file
    header = ['LastFirstName','PeopleID','Last','First','Full Name','Nick Name','Gender','Membership','Child',
              'BirthDate','Status','HouseholdID','Created','Updated','Link']
    csvwriter.writerow(header)

    offset = 0
    
    while offset is not None:

        #Get people in last name order and include household ID if present
        request = 'https://api.planningcenteronline.com/people/v2/people?include=households&order=last_name&offset=' + str(offset)
        resp = http.request('GET', request, headers=req_header)
        if resp.status != 200:
            raise ValueError('Status ' + str(resp.status) + ' returned on GET request ' + request)

        resp_dict=json.loads(resp.data)
        for p in resp_dict["data"]:
            p_attrs=p["attributes"]
            p_household=p["relationships"]["households"]["data"]
            if len(p_household) == 0:
                houseID = ""
            else:
                houseID = p_household[0]['id']
                
            csvrow=[p_attrs['last_name'] + ", " + p_attrs['first_name'], p['id'], p_attrs['last_name'], p_attrs['first_name'], 
                p_attrs['name'], p_attrs['nickname'], p_attrs['gender'], p_attrs['membership'], p_attrs['child'], 
                p_attrs['birthdate'], p_attrs['status'], houseID,
                p_attrs['created_at'], p_attrs['updated_at'],
                p['links']['self']]
            #print(csvrow)
            csvwriter.writerow(csvrow)
        if resp_dict["meta"].get("next") is not None:
            offset = resp_dict["meta"].pop("next",None).pop("offset",None)
        else:
            offset = None

    people_out.close()
exit
        



