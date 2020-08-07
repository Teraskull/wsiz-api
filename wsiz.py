from bs4 import BeautifulSoup
import requests


url = 'https://wu-beta.wsiz.pl/'
login_route = 'Account/Login/'
data_route = 'PersonalData/'
grade_route = 'Grades/'
fees_route = 'Charges/'


def start_session(login: str, password: str, lang: str = 'en') -> object:
    s = requests.Session()
    if lang.lower() == 'pl':
        lang = 'pl-PL'
    else:
        lang = 'en-US'
    headers = {'Accept-Language': f'{lang},en;q=0.8'}

    get_token = s.get(url + login_route, headers=headers)
    token = BeautifulSoup(get_token.text, 'html.parser').find('input', {'name': '__RequestVerificationToken'})['value']

    payload = {
        'UserLogin': login,
        'Password': password,
        '__RequestVerificationToken': token
    }

    attempt_login = s.post(url + login_route, data=payload)
    login_error = BeautifulSoup(attempt_login.text, 'html.parser').find('span', class_="field-validation-error")
    if login_error:
        return 401
    return s


def get_grades(s: object, semester: str = '0') -> dict:
    if semester != 0:
        grade_route = f"Grades/GetData?semester={semester}"
    get_grade_page = s.get(url + grade_route)
    grade_page = BeautifulSoup(get_grade_page.text, 'html.parser')
    semester_num = grade_page.find('span', class_="dxeBase_Office365wsiz").text[-1]

    header_items = []
    for table_header in grade_page.find_all('table', class_="dxgvHCEC"):
        column_name = table_header.find_all('td')
        for item in column_name:
            header_items.append(item.text)

    grades = {
        "Semester": semester_num,
        "Grades": []
    }
    for table_row in grade_page.find_all('tr', class_="dxgvDataRow_Office365wsiz"):
        subject = table_row.find_all('td', class_="dx-ellipsis")
        grade = {}
        for idx, item in enumerate(subject):
            if item.text != '-':
                grade[header_items[idx]] = item.text.strip()
        grades["Grades"].append(grade)
    return grades


def get_data(s: object) -> dict:
    get_data_page = s.get(url + data_route)
    data_page = BeautifulSoup(get_data_page.text, 'html.parser')

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


def get_fees(s: object) -> dict:
    get_fees_page = s.get(url + fees_route)
    fees_page = BeautifulSoup(get_fees_page.text, 'html.parser')

    header_items = []
    for table_header in fees_page.find_all('td', class_="dxgvHeader_Office365wsiz"):
        column_name = table_header.find_all('td', class_="dx-ellipsis")
        for item in column_name:
            header_items.append(item.text.strip())

    fees = {
        "Charges": []
    }
    for table_row in fees_page.find_all('tr', class_="dxgvDataRow_Office365wsiz"):
        charge = table_row.find_all('td', class_="dx-ellipsis")
        fee = {}
        for idx, item in enumerate(charge):
            if idx != 4:  # Skip row with comments
                fee[header_items[idx]] = item.text.strip()
        fees["Charges"].append(fee)
    return fees
