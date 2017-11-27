import csv
import json
pco = {"data":{
                "type":"Donation",
                "attributes": {"payment_method":"cash",
                               "received_at":"2017-01-01",
                               "payment_check_number": "123"},
                "relationships": {
                    "person":{"data": {"type": "Person", "id":"123123"}},
                    "payment_source": {"data": {"type": "PaymentSource", "id": "456456"}}
                    
                    }
                },
            "included": {
                "type":"Designation",
                "attributes": {"amount_cents": 0000 },
                "relationships": {
                    "fund": {"data": {"type": "Fund", "id": "123"}}
                    }
                }
            }


if __name__ == '__main__':

    # open files for reading and writing
    donation_file = open('DonationXfer.csv')
    json_file = open('json.txt','w')

    # create the csv reader object
    donation_record = csv.reader(donation_file, dialect='excel')
    
    donation_hdr = next(donation_record)
    for donation_rec in donation_record:
        
        donation_dict=dict(zip(donation_hdr,donation_rec))
        #If an incoming ID is present, post donation information
        if donation_dict["PeopleID"] != "#NA":
            pco["data"]["attributes"]["payment_method"]=donation_dict["payment_method"]
            pco["data"]["attributes"]["received_at"]=donation_dict["Received_at"]
            
            pco["data"]["relationships"]["person"]["data"]["id"]=donation_dict["PeopleID"]
            
            pco["included"]["attributes"]["amount_cents"]=int(round(float(donation_dict["Amount"].strip(' $'))*100))
            pco["included"]["relationships"]["fund"]["data"]["id"]=int(donation_dict["fund_id"])

            #If we have a checkNbr value, include it in the attribute, otherwise remove the attribute for it
            if donation_dict["checkNbr"] > "":
                pco["data"]["attributes"]["payment_check_number"]=donation_dict["checkNbr"]
            else: 
                pco["data"]["attributes"].pop("payment_check_number",None)

            #If we have a payment_source value, include it in the relationship, otherwise remove the relationship for it
            if donation_dict["payment_source"] > "":
                pco["data"]["relationships"]["payment_source"]={"data": {"type": "PaymentSource", "id": donation_dict["payment_source"]}}
            else:
                pco["data"]["relationships"].pop("payment_source",None)
            
            json_file.write(json.dumps(pco))
            json_file.write("\n\n")
        
    # close files
    json_file.close()
    donation_file.close()
    
exit
