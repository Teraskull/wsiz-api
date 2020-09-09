from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from typing import Optional, Union
from wsiz import Scraper


app = FastAPI()


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
def read_grades(login: str, password: str, semester: Optional[str] = Query(None, deprecated=True), lang: Optional[str] = None):
    """
    Get student grades:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **semester**: University semester (optional) [DEPRECATED: Grades from previous semesters are currently not available on the Virtual University.]
     - **lang**: Language [pl] (optional)
    """
    scraper = Scraper(login, password, semester, lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_grades(s)


@app.get("/data")
def read_data(login: str, password: str, lang: Optional[str] = None):
    """
    Get student personal data:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [pl] (optional)
    """
    scraper = Scraper(login, password, lang=lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_data(s)


@app.get("/fees")
def read_fees(login: str, password: str, lang: Optional[str] = None):
    """
    Get student fees:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [pl] (optional)
    """
    scraper = Scraper(login, password, lang=lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_fees(s)


@app.get("/study")
def read_study(login: str, password: str, lang: Optional[str] = None):
    """
    Get student course of study:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [pl] (optional)
    """
    scraper = Scraper(login, password, lang=lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_study(s)
