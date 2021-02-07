import json
import os


class DownloadFilter:

    def __init__(self, data):
        self._data = data
        os.makedirs(self._data, exist_ok=True)


    def _nameDB(self, name):
        return os.path.join(self._data, name) + '.json'


    def _readDB(self, name):
        db = []
        try:
            with open(self._nameDB(name), 'r') as f:
                db = json.load(f)
        except FileNotFoundError:
            pass
        return db


    def _writeDB(self, name, data):
        with open(self._nameDB(name), 'w') as f:
            json.dump(data, f, indent=4)


    def filterNew(self, name, entries):
        db = self._readDB(name)
        newEntries = []
        for entry in entries:
            entry_id = entry['id']
            found = False
            for saved in db:
                if saved['id'] == entry_id:
                    found = True
            if not found:
                newEntries.append(entry)
        return newEntries


    def update(self, name, entry):
        db = self._readDB(name)
        db.append(
            {
                'id': entry['id'],
                'title': entry['title'],
            }
        )
        self._writeDB(name, db)
