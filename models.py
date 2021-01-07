import datetime

"""
reading: {
    "name": [entry]
}
"""


class Entry(dict):
    def __init__(self, entry):
        super().__init__()
        # noinspection PyProtectedMember
        self['label'] = entry.label
        self['current'] = entry.current
        if entry.high is not None:
            self['high'] = entry.high
        if entry.critical is not None:
            self['critical'] = entry.critical


class Reading(dict):
    def __init__(self, reading):
        super().__init__()
        self.update({name: list(map(Entry, entries)) for name, entries in reading.items()})


class Log(dict):
    def __init__(self, temps, _id=None, created=datetime.datetime.now(), warning=None):
        super().__init__()
        if _id is not None:
            self['_id'] = _id
        self['created'] = created
        self['temps'] = temps
        if warning is None:
            self['warning'] = any(
                'high' in entry and entry['current'] >= entry['high'] or 'critical' in entry and entry['current'] >=
                entry['critical']
                for entries in self['temps'].values() for entry in entries)
        else:
            self['warning'] = warning
