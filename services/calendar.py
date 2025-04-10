from caldav import DAVClient

class CalendarService():

    def __init__(self, acess_token):
        self.client = DAVClient(
            url= "http://nextcloud/remote.php/dav",
            headers={"Autorization": f"Bearer {acess_token}"}
        )
        self.principal = self.client.principal()
        self.calendar = self.principal.calendars()[0]
    
    def get_events_today(self):
        events = self.calendar.date_search()
        return[
            e.vobject_instance.vevent.summary.value for e in events
        ]