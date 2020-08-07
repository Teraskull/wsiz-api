<h1 align="center">
  WSIZ API
</h1>

<p align="center">
  API for the WSIZ Virtual University <a href="wu-beta.wsiz.pl/">website</a>.
</p>

<p align="center">
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
* [Uvicorn](http://www.uvicorn.org/) ASGI server
    ```console
    $ pip install uvicorn
    ```

## Installation:

```console
$ git clone https://github.com/Teraskull/wsiz-api
```
```console
$ cd wsiz-api
```
```console
$ pip install -r requirements.txt
```
```console
$ uvicorn main:app --reload
```

## Example:

Open your browser at http://127.0.0.1:8000/docs.


## License:

This software is available under the following licenses:

  * **MIT**
  
