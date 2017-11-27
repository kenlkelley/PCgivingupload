import urllib3, certifi
import csv, json

TOKEN = 'efc6e2e34663885dcd891bb7cd157b8ae8c5ddeed5dbe754c90b07a4c42e574d'
SECRET = '7e04cb5c66c9309a470f945bb3109919dca71e485de3d7095cd8548d89b1f890'

if __name__ == '__main__':
    
    # open a file for writing
    households_out = open('Households.csv', 'w')
    # create the csv writer object
    csvwriter = csv.writer(households_out, lineterminator='\n')

    #Set up for HTTPS using basic authentication
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    req_header = urllib3.util.make_headers(basic_auth=TOKEN + ":" + SECRET)

    #Write heading row for the CSV file
    header = ['HouseholdID','Name','Members','Primary Contact','ContactID','Created','Updated','Link']
    csvwriter.writerow(header)

    offset=0
    while offset is not None:

        request = 'https://api.planningcenteronline.com/people/v2/households?offset=' + str(offset)
        resp = http.request('GET', request, headers=req_header)
        if resp.status != 200:
            raise ValueError('Status ' + str(resp.status) + ' returned on GET request ' + request)

        resp_dict=json.loads(resp.data)
        for h in resp_dict["data"]:
            h_attrs=h["attributes"]
            csvrow=[h['id'], h_attrs['name'], h_attrs['member_count'],
                h_attrs['primary_contact_name'], h_attrs['primary_contact_id'],
                h_attrs['created_at'], h_attrs['updated_at'],
                h['links']['self']]
            #print(csvrow)
            csvwriter.writerow(csvrow)
        if resp_dict["meta"].get("next") is not None:
            offset = resp_dict["meta"].pop("next",None).pop("offset",None)
        else:
            offset = None

    households_out.close()
exit
