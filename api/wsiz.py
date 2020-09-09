from bs4 import BeautifulSoup
import requests


class Scraper():
    '''
    Scrape student information from the WSIZ Virtual University website
    '''
    def __init__(self, login: str, password: str, semester: str = None, lang: str = None):
        self.login = login
        self.password = password
        self.semester = semester
        self.lang = lang
        self.url = 'https://wu-beta.wsiz.pl/'
        self.login_route = 'Account/Login/'
        self.data_route = 'PersonalData/'
        self.grade_route = 'Grades/'
        self.fees_route = 'Charges/'
        self.study_route = 'CurrentStudy/'
        if self.lang is not None and self.lang.lower() == 'pl':
            self.lang = 'pl-PL'
            self.word_semester = 'Semestr'
            self.word_grades = 'Oceny'
            self.word_charges = 'Opłaty'
        else:
            self.lang = 'en-US'
            self.word_semester = 'Semester'
            self.word_grades = 'Grades'
            self.word_charges = 'Charges'
        if self.semester is not None:
            try:
                if not int(self.semester).bit_length() < 32:  # If Integer Overflow on website, set to latest semester
                    self.semester = '0'
            except ValueError:  # If not a digit, set to latest semester
                self.semester = '0'
            self.grade_route = f"Grades/GetData?semester={self.semester}"

    def start_session(self) -> object:
        s = requests.Session()

        headers = {'Accept-Language': f'{self.lang},en;q=0.8'}
        get_token = s.get(self.url + self.login_route, headers=headers)
        token = BeautifulSoup(get_token.text, 'lxml').find('input', {'name': '__RequestVerificationToken'})['value']

        payload = {
            'UserLogin': self.login,
            'Password': self.password,
            '__RequestVerificationToken': token
        }

        attempt_login = s.post(self.url + self.login_route, data=payload)
        login_error = BeautifulSoup(attempt_login.text, 'lxml').find('span', class_="field-validation-error")
        if login_error:
            return 401
        return s

    def get_grades(self, s: object) -> dict:
        get_grade_page = s.get(self.url + self.grade_route)
        grade_page = BeautifulSoup(get_grade_page.text, 'lxml')
        try:
            semester_num = grade_page.find('span', class_="dxeBase_Office365wsiz").text[-1]
            int(semester_num)
        except ValueError:
            semester_num = ''

        header_items = []
        for table_header in grade_page.find_all('table', class_="dxgvHCEC"):
            column_name = table_header.find_all('td')
            for item in column_name:
                header_items.append(item.text)

        grades = {
            self.word_semester: semester_num,
            self.word_grades: []
        }
        for table_row in grade_page.find_all('tr', class_="dxgvDataRow_Office365wsiz"):
            subject = table_row.find_all('td', class_="dx-ellipsis")
            grade = {}
            for idx, item in enumerate(subject):
                if item.text != '-':  # Skip empty cells
                    grade[header_items[idx]] = item.text.strip()
            grades[self.word_grades].append(grade)
        return grades

    def get_data(self, s: object) -> dict:
        get_data_page = s.get(self.url + self.data_route)
        data_page = BeautifulSoup(get_data_page.text, 'lxml')

        header_items = []
        for table_header in data_page.find_all('td', class_="dxvgHeader_Office365wsiz"):
            column_name = table_header.find_all('tr')
            for item in column_name:
                header_items.append(item.text.strip())

        data = {}
        for table_row in data_page.find_all('table', class_="dxvgTable_Office365wsiz"):
            subject = table_row.find_all('td', class_="dxvgRecord_Office365wsiz")
            for idx, item in enumerate(subject):
                if idx != 0:  # Skip row with photo
                    data[header_items[idx]] = item.text.strip()
        return data

    def get_fees(self, s: object) -> dict:
        get_fees_page = s.get(self.url + self.fees_route)
        fees_page = BeautifulSoup(get_fees_page.text, 'lxml')

        header_items = []
        for table_header in fees_page.find_all('td', class_="dxgvHeader_Office365wsiz"):
            column_name = table_header.find_all('td', class_="dx-ellipsis")
            for item in column_name:
                header_items.append(item.text.strip())

        fees = {
            self.word_charges: []
        }
        for table_row in fees_page.find_all('tr', class_="dxgvDataRow_Office365wsiz"):
            charge = table_row.find_all('td', class_="dx-ellipsis")
            fee = {}
            for idx, item in enumerate(charge):
                if idx != 4:  # Skip row with comments
                    fee[header_items[idx]] = item.text.strip()
            fees[self.word_charges].append(fee)
        return fees

    def get_study(self, s: object) -> dict:
        get_study_page = s.get(self.url + self.study_route)
        study_page = BeautifulSoup(get_study_page.text, 'lxml')

        header_items = []
        for table_header in study_page.find_all('td', class_="dxvgHeader_Office365wsiz"):
            column_name = table_header.find_all('tr')
            for item in column_name:
                header_items.append(item.text.strip())

        study = {}
        for table_row in study_page.find_all('table', class_="dxvgTable_Office365wsiz"):
            subject = table_row.find_all('td', class_="dxvgRecord_Office365wsiz")
            for idx, item in enumerate(subject):
                study[header_items[idx]] = item.text.strip()
        return study
