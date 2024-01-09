# Livre Mon Colis - Python Backend

## About

This is the Backend for the `Livre Mon Colis` application in python.

> **Note:**  
> This is not the final version of this page and is just sent as a test once again and again but sometimes it just needs some tinkering and it works, maybe?


## How to run

First of all, you need to install the dependencies:

```sh
pip3 install -r ./requirements.txt
```

> **Note:**  
> It's recommended to install dependencies in a virtualenv such as a `venv` or a
> `pyenv virtualenv`.

When it's done, you can run the command below to launch the server asynchronously:

```sh
uvicorn server:app
```

> **Note:**  
> If you want to launch the server in development mode, you can do:
>
> ```sh
> uvicorn server:app --reload
> ```