from fastapi import FastAPI, HTTPException
from typing import Optional, Union
from wsiz import Scraper


app = FastAPI(title='WSIZ API',
              description='API for the WSIZ Virtual University website.',
              version="1.2.0",
              docs_url="/",
              openapi_url="/api/v1/openapi.json"
              )


def validate_user(s: Union[int, object]) -> None:
    if s == 401:
        raise HTTPException(status_code=401, detail="401 Unauthorized")


@app.get("/", tags=["Documentation"])
def read_docs():
    """
    Interactive API documentation provided by Swagger UI
    """


@app.get("/redoc", tags=["Documentation"])
def read_redoc():
    """
    ReDoc API Reference Documentation
    """


@app.get("/grades", tags=["Endpoints"])
def read_grades(login: str, password: str, semester: Optional[str] = '0', lang: Optional[str] = None):
    """
    Get student grades:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **semester**: University semester (optional)
     - **lang**: Language [pl] (optional)
    """
    scraper = Scraper(login, password, semester, lang)
    s = scraper.start_session()
    validate_user(s)
    return scraper.get_grades(s)


@app.get("/data", tags=["Endpoints"])
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


@app.get("/fees", tags=["Endpoints"])
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


@app.get("/study", tags=["Endpoints"])
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
