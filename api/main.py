from fastapi import FastAPI, HTTPException, Query
from typing import Optional, Union
from wsiz import Scraper


app = FastAPI(title='WSIZ API',
              description='API for the WSIZ Virtual University website.',
              version="1.1.0",
              docs_url="/",
              openapi_url="/api/v1/openapi.json"
              )


def validate_user(s: Union[int, object]) -> None:
    if s == 401:
        raise HTTPException(status_code=401, detail="401 Unauthorized")


scraper = Scraper()


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


@app.get("/user", tags=["Endpoints"])
def read_user(login: str, password: str, lang: Optional[str] = None):
    """
    Log into student account:
     - **login**: WSIZ student ID (required)
     - **password**: WSIZ student account password (required)
     - **lang**: Language [pl] (optional)
    """
    s, login, lang = scraper.start_session(login, password, lang)
    validate_user(s)
    return scraper.get_user(login, lang)


@app.get("/grades", tags=["Endpoints"])
def read_grades(semester: Optional[str] = Query(None, deprecated=True)):
    """
    Get student grades:
     - **semester**: University semester (optional) [DEPRECATED: Grades from previous semesters are currently not available on the Virtual University.]
    """
    return scraper.get_grades(semester)


@app.get("/data", tags=["Endpoints"])
def read_data():
    """
    Get student personal data
    """
    return scraper.get_data()


@app.get("/fees", tags=["Endpoints"])
def read_fees():
    """
    Get student fees
    """
    return scraper.get_fees()


@app.get("/study", tags=["Endpoints"])
def read_study():
    """
    Get student course of study
    """
    return scraper.get_study()
