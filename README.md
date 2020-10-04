<p align="center">
  <a href="https://wsiz.rzeszow.pl/"><img src="wsiz_logo.png" width="10%"></a>
</p>
<h1 align="center">
  WSIZ API
</h1>

<p align="center">
  API for the WSIZ Virtual University <a href="https://wu.wsiz.edu.pl/">website</a>.
</p>

<p align="center">
  <a style="text-decoration:none" href="https://pydebloatx.com:1327">
    <img src="https://img.shields.io/website?label=API&style=flat-square&up_color=00B16A&url=https%3A%2F%2Fpydebloatx.com%3A1327" alt="WSIZ API" />
  </a>
  <a style="text-decoration:none" href="https://www.codefactor.io/repository/github/teraskull/wsiz-api">
    <img src="https://www.codefactor.io/repository/github/teraskull/wsiz-api/badge?style=flat-square" alt="CodeFactor" />
  </a>
</p>

## Requirements:

* Python 3.6+

* [FastAPI](https://github.com/tiangolo/fastapi) framework
    ```console
    $ pip install fastapi
    ```
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) library
    ```console
    $ pip install beautifulsoup4
    ```
* [Uvicorn](http://www.uvicorn.org/) ASGI server
    ```console
    $ pip install uvicorn
    ```

## Installation:

```console
$ git clone https://github.com/Teraskull/wsiz-api

$ cd wsiz-api

$ pip install -r requirements.txt

$ cd api

$ uvicorn main:app --reload
```

## Documentation:

Open your browser at http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)).


## License:

This software is available under the following licenses:

  * **MIT**
  
