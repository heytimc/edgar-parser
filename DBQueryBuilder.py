import psycopg2

class QueryBuilder:
    def __init__(self):
        conn = psycopg2.connect("dbname=minervacustomer user=postgres")
        cur = con.cursor()

    def insertCompany(self, companyID, companyName, cik):
        cur.execute("INSERT INTO company (companyid, companyname, cik) VALUES (%s, %s, %s)", (companyID, companyName, cik))

    def insertEventType(self, eventTypeID, eventDescription):
        cur.execute("INSERT INTO eventtype (eventtypeid, description) VALUES (%s, %s)", (eventTypeID, eventDescription))

    def insertEvent(self, eventID, eventDate, address):
        cur.execute("INSERT INTO event (eventid, companyid, eventtypeid, eventdate, address) VALUES (%s, %s, %s, %s, %s)",
                    (eventID, companyID, eventTypeID, eventDate, address))

    def insertResolutions(self, resolutionNum, title, narrative):
        cur.execute("INSERT INTO event (resolutionid, eventid, title, narrative) VALUES (%s, %s, %s, %s)",
                    (resolutionNum, eventID, title, narrative))
        