import psycopg2


class QueryBuilder:
    
    def __init__(self):
        self.conn = psycopg2.connect("dbname=minervacustomer password=123 user=postgres")
        self.cur = self.conn.cursor()

    def insertCompany(self, companyID=None, companyName=None, cik=None):
        # self.cur.execute("INSERT INTO company (companyid, companyname, cik) VALUES (%s, %s, %s)", (companyID, companyName, cik))
        pass

    def insertEventType(self, eventTypeID=None, eventDescription=None):
        # self.cur.execute("INSERT INTO eventtype (eventtypeid, description) VALUES (%s, %s)", (eventTypeID, eventDescription))
        pass
    
    def insertEvent(self, eventID=None, eventDate=None, address=None, companyID=None, eventTypeID=None):
        # self.cur.execute("INSERT INTO event (eventid, companyid, eventtypeid, eventdate, address) VALUES (%s, %s, %s, %s, %s)",
                    # (eventID, companyID, eventTypeID, eventDate, address))
        pass
    
    def insertResolutions(self, resolutionNum=None, title=None, narrative=None, eventID=None):
        # self.cur.execute("INSERT INTO event (resolutionid, eventid, title, narrative) VALUES (%s, %s, %s, %s)",
                    # (resolutionNum, eventID, title, narrative))
        pass