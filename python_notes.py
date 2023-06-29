import datetime
import json


def start():

    fnc = Operator(FileNote("Notes.json"), Print())
    while (True):
        print('Starting Notes')
        menuInterface()
        option = ''
        try:
            option = int(input('Insert number from 1 to 7: '))
        except:
            print('Insert Error')

        if option == 1:
            print('\nCreating Note.')
            fnc.newNote(fillNote())
        elif option == 2:
            print('\nShow Note.')
            if fnc.isNotes():
                fnc.viewNote(int(noteIdentification()))
        elif option == 3:
            if fnc.isNotes():
                print('\nShow all Notes.')
                fnc.viewNotes()
        elif option == 4:
            if fnc.isNotes():
                print('\nEdit Note.')
                updated_id = int(noteIdentification())
                if fnc.isNoteId(updated_id):
                    fnc.updateNote(updated_id, fillNote())
        elif option == 5:
            if fnc.isNotes():
                print('\nDelete Note/')
                delete_id = int(noteIdentification())
                if fnc.isNoteId(delete_id):
                    fnc.discardNote(delete_id)
        elif option == 6:
            if fnc.isNotes():
                print('Delete All Notes.')
                if fnc.isNotes():
                    fnc.discardNotes()
        elif option == 7:
            print('Exit.')
            exit()
        else:
            print('Insert Error. Insert number from 1 to 7.')


def fillNote():
    note_id = 0
    date = datetime.datetime.now()
    title = input('\t\tName Note: ')
    text = input('\t\tTape Note: ')
    return Note(note_id, date, title, text)


def noteIdentification():
    while True:
        get_choice = input('\t\tTape Note ID: ')
        if get_choice.isdigit() and int(get_choice) > 0:
            return get_choice
        else:
            print('\t\t\tWrong ID!')


class Operator(object):

    def __init__(self, model, view):

        self.model = model
        self.view = view

    def viewNotes(self):

        notes = self.model.readFile()
        self.view.printNoteList(notes)

    def viewNote(self, note_id):

        try:
            note = self.model.readNoteId(note_id)
            self.view.viewNote(note)
        except ValueError:
            self.view.noId(note_id)

    def newNote(self, note):

        self.model.newNote(note)
        self.view.noteAdded()

    def updateNote(self, note_id, note):

        self.model.updateNote(note_id, note)
        self.view.noteUpdated(note_id)

    def discardNote(self, note_id):

        try:
            self.model.discardNote(note_id)
            self.view.noteDelete(note_id)
        except ValueError:
            self.view.noId(note_id)

    def discardNotes(self):

        self.model.discardNotes()
        self.view.notesDeleteAll()

    def isNotes(self):

        notes = self.model.readFile()
        if len(notes) == 0:
            self.view.emptyList()
            return False
        else:
            return True

    def isNoteId(self, search_id):

        notes = self.model.readFile()
        for note in notes:
            if note.note_id == search_id:
                return True
        else:
            self.view.noId(search_id)
            return False


class FileNote(object):

    def __init__(self, filename):
        self.filename = filename
        self.notes = list()

    def newNote(self, note):

        self.notes = self.readFile()
        max_id = 0
        for item in self.notes:
            if item.note_id > max_id:
                max_id = item.note_id
        note_id = max_id + 1
        note.note_id = note_id

        self.notes.append(note)
        self.fileWrite(self.notes)

    def readNoteId(self, search_id):

        self.notes = self.readFile()
        for note in self.notes:
            if note.note_id == search_id:
                return note
        else:
            Print.noId(search_id)

    def readFile(self):

        return self.fileRead()

    def noteRefactor(self, search_id, note):

        self.notes = self.readFile()
        for item in self.notes:
            if item.note_id == search_id:
                item.date = note.date
                item.title = note.title
                item.text = note.text

        self.fileWrite(self.notes)

    def discardNote(self, search_id):

        self.notes = self.readFile()

        for index, note in enumerate(self.notes):
            if note.note_id == search_id:
                del self.notes[index]

        self.fileWrite(self.notes)

    def discardNotes(self):

        self.notes = self.readFile()
        self.notes.clear()
        self.fileWrite(self.notes)

    def fileWrite(self, notes):

        json_strings_list = list()
        for note in notes:
            json_strings_list.append({'id': note.note_id, 'date': note.date, 'title': note.title, 'text': note.text})

        notes_json = json.dumps(json_strings_list, indent=4, ensure_ascii=False, sort_keys=False, default=str)

        with open(self.filename, "w", encoding='utf-8') as my_file:
            my_file.write(notes_json)

    def fileRead(self):

        notes_list = list()
        try:
            with open(self.filename, "r", encoding='utf-8') as my_file:
                notes_json = my_file.read()
            data = json.loads(notes_json)
            data.sort(key=lambda x: x['date'])
            for item in data:
                notes_list.append(Note(item['id'], item['date'], item['title'], item['text']))

            return notes_list
        except ValueError:
            return self.notes


class Print(object):

    @staticmethod
    def printNoteList(notes):
        for note in notes:
            print('------')
            print(f'ID: {note.note_id}\n' \
                  f'Last Date: {note.date}\n' \
                  f'Header: {note.title}\n' \
                  f'Note: {note.text}\n')

    @staticmethod
    def viewNote(note):
        print('------')
        print(f'ID: {note.note_id}\n' \
              f'Last Date: {note.date}\n' \
              f'Header: {note.title}\n' \
              f'Note: {note.text}\n')

    @staticmethod
    def emptyList():
        print('>>There Is No Notes Yet')

    @staticmethod
    def idEpsent(note_id):
        print(f'--- Note {note_id} Is Epsent')

    @staticmethod
    def idPresent(note_id):
        print(f'--- Note {note_id} Is Already Exists')

    @staticmethod
    def noteAdded():
        print('--- Note Added')

    @staticmethod
    def noteUpdated(note_id):
        print(f'--- Note {note_id} Updated')

    @staticmethod
    def noteDelete(note_id):
        print(f'--- Note {note_id} Deleted')

    @staticmethod
    def notesDeleteAll():
        print('All Notes Deleted')

    def noId(search_id):
        return search_id


def menuInterface():

    for key in interfaceVariables.keys():
        print(key, '--', interfaceVariables[key])


class FileChanger(object):

    def __init__(self, model, view):

        self.model = model
        self.view = view

    def viewNotes(self):

        notes = self.model.readFile()
        self.view.printNoteList(notes)

    def viewNote(self, note_id):

        try:
            note = self.model.readNoteId(note_id)
            self.view.viewNote(note)
        except ValueError:
            self.view.noId(note_id)

    def newNote(self, note):

        self.model.newNote(note)
        self.view.noteAdded()

    def updateNote(self, note_id, note):

        self.model.noteRefactor(note_id, note)
        self.view.noteUpdated(note_id)

    def discardNote(self, note_id):

        try:
            self.model.discardNote(note_id)
            self.view.noteDelete(note_id)
        except ValueError:
            self.view.noId(note_id)

    def discardNotes(self):

        self.model.discardNotes()
        self.view.notesDeleteAll()

    def isNotes(self):

        notes = self.model.readFile()
        if len(notes) == 0:
            self.view.emptyList()
            return False
        else:
            return True

    def isNoteId(self, search_id):

        notes = self.model.readFile()
        for note in notes:
            if note.note_id == search_id:
                return True
        else:
            self.view.noId(search_id)
            return False


class Note(object):

    def __init__(self, note_id, date, title, text):
        self.note_id = note_id
        self.date = date
        self.title = title
        self.text = text

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def note_id(self):
        return self._note_id

    @note_id.setter
    def note_id(self, note_id):
        self._note_id = note_id

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    def __str__(self):
        return f'ID:{self._note_id}' \
               f'Last Date:{self._date}' \
               f'Header:{self._title}' \
               f'Note:{self._text}'


interfaceVariables = {
    1: 'Add Note',
    2: 'Show Note',
    3: 'Show All Notes',
    4: 'Edit Note',
    5: 'Delete Note',
    6: 'Delete All Notes',
    7: 'Exit',
}
