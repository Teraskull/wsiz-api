from wsiz import start_session, get_grades, get_data, get_fees
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException
from typing import Optional


app = FastAPI()
default_lang = 'en'


def validate_user(s: int) -> None:
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
    s = start_session(login, password, lang)
    validate_user(s)
    try:
        if int(semester).bit_length() < 32:  # Check if no Integer Overflow on website
            return get_grades(s, semester)  # Accept anything as a semester value
        return get_grades(s)
    except ValueError:
        return get_grades(s)  # If semester does not exist, return latest one


@app.get("/data")
def read_data(login: str, password: str, lang: Optional[str] = default_lang):
    """
    Get student personal data:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [en, pl] (optional)
    """
    s = start_session(login, password, lang)
    validate_user(s)
    return get_data(s)


@app.get("/fees")
def read_fees(login: str, password: str, lang: Optional[str] = default_lang):
    """
    Get student fees:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [en, pl] (optional)
    """
    s = start_session(login, password, lang)
    validate_user(s)
    return get_fees(s)
