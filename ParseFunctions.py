from bs4 import BeautifulSoup

def parse_to_csv(time_table):
    """
        Convert html to csv.
    """
    
    soup = BeautifulSoup(time_table)


    ##### go through each row in the table #####

    data=[["name","semester","type","group","lecture","start_time","end_time","venue"]]
    
    for tr in soup.tbody.find_all('tr'):
        ##### put data of the form d1/d2/d3/d4 in variable seperated = [d1,d2,d3,d4]
        together = tr.td.string
        index = 0;
        seperated = [];
        while index >= 0:
            index1 = together.find( '/', index )
            if index1 == -1:
                seperated.append(together[index:])
                index = index1
            else:
                seperated.append(together[index:index1])
                index=index1+1
            
        cols = tr.find_all('td')
        
        name = seperated[1]
        type = seperated[4][0]
        group = int(seperated[2][2:])
        day = cols[2].string
        start_time = cols[3].string
        end_time = cols[4].string
        venue = cols[5].string
        
        if cols[1].string[0] == "S":
            semester = int(cols[1].string[1:])
            data.append([name,semester,type,group,day,start_time,end_time,venue])
        elif cols[1].string[0] == "J":
            for sem in range(2):
                data.append([name,sem+1,type,group,day,start_time,end_time,venue])
        
    return data
