from caldav import DAVClient

class CalendarService:
    def __init__(self, access_token):
        self.client = DAVClient(
            url="https://nuvem.codegus.space/remote.php/dav",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        self.principal = self.client.principal()
        self.calendar = self.principal.calendars()[0]

    def get_events_today(self):
        events = self.calendar.date_search()
        return [e.vobject_instance.vevent.summary.value for e in events]
