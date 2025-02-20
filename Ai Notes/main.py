from openai import OpenAI
import sqlite3
from dotenv import load_dotenv
import os

class AINotes:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv('api_key'),
        )
        self.con = sqlite3.connect("note.db")
        self.cursor = self.con.cursor()
        try:
            self.cursor.execute('Select * From notes')
        except:
            self.cursor.execute('create table notes (id int NOT NULL PRIMARY KEY, note char(1000))')

        self.main()

    def check_id(self):
        if self.cursor.execute('Select COUNT(*) From notes').fetchone()[0] > 0:
            res = self.cursor.execute("Select MAX(id) From notes ")
            max_id = res.fetchone()[0]
        else:
            max_id = 0
        return max_id

    def add_note(self):
        new_note = input("Napisz notatkę: ")
        max_id = self.check_id()
        params = (max_id+1, new_note)
        self.cursor.execute(f'insert into notes(id, note) Values(?, ?)', params)
        self.con.commit()

    def print_note(self):
        query = self.cursor.execute("Select * From Notes")
        result = query.fetchall()
        for i in range(len(result)):
            print(f'{result[i][0]}. {result[i][1]}')

    def summaries_note(self):
        id = input("Choose note number: ")
        query = self.cursor.execute(f"Select note From notes Where id = {id}")
        result = query.fetchone()[0]
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Summaries this text {result}",
                }
            ],
            model="gpt-4o")
        print(response.choices[0].message.content)

    def translate_note(self):
        id = input("Choose note number: ")
        lang = input("Language to translate: ")
        query = self.cursor.execute(f"Select note From notes Where id = {id}")
        result = query.fetchone()[0]
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Translate {result} to {lang}",
                }
            ],
            model="gpt-4o")
        print(response.choices[0].message.content)


    def main(self):
        print("1. Add note")
        print("2. Display notes ")
        print("3. Summaries note")
        print('4. Translate note')
        option = input('Choose option: ')
        if option == '1':
            self.add_note()
        elif option == '2':
            self.print_note()
        elif option == '3':
            self.summaries_note()
        elif option == '4':
            self.translate_note()

app = AINotes()