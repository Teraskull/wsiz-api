from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from typing import Optional, Union
from wsiz import Scraper


app = FastAPI()
default_lang = 'en'


def validate_user(s: Union[int, object]) -> None:
    if s == 401:
        raise HTTPException(status_code=401, detail="401 Unauthorized")


@app.get("/")
def read_root():
    """
    Root path, redirects to this documentation
    """
    return RedirectResponse("/docs/")


@app.get("/grades")
def read_grades(login: str, password: str, semester: Optional[str] = Query('0', deprecated=True), lang: Optional[str] = default_lang):
    """
    Get student grades:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **semester**: University semester (optional) [DEPRECATED: Grades from previous semesters are currently not available on the Virtual University.]
     - **lang**: Language [en, pl] (optional)
    """
    scraper = Scraper(login, password, semester, lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_grades(s)


@app.get("/data")
def read_data(login: str, password: str, lang: Optional[str] = default_lang):
    """
    Get student personal data:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [en, pl] (optional)
    """
    scraper = Scraper(login, password, lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_data(s)


@app.get("/fees")
def read_fees(login: str, password: str, lang: Optional[str] = default_lang):
    """
    Get student fees:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [en, pl] (optional)
    """
    scraper = Scraper(login, password, lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_fees(s)
