from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException
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
def read_grades(login: str, password: str, semester: Optional[str] = '0', lang: Optional[str] = default_lang):
    """
    Get student grades:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **semester**: University semester (optional)
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
