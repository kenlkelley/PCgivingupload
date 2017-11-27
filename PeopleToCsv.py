import json
import csv


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

    linenbr = 0
    
    for fileref in ['people1.json','people2.json','people3.json','people4.json']:
        people_file = open(fileref)
        people_data = people_file.read()
        People_Out(json.loads(people_data), csvwriter, linenbr)
        
    people_out.close()


