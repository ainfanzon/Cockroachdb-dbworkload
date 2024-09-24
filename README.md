# Corckroachdb-dbworkload

## Install dbworkload

If you have installed different versions of Python from various sources, including Homebrew, the Official Installer, and Conda then the package manager (pip) will try to resolve the dependency conflict for you and install the most suitable version instead. The example below shows I am using a the anaconda3 Python binary.

```% which python```<br>
```/opt/anaconda3/bin/python```

If you try to install **dbworkload** ([see github readme.md](https://github.com/fabiog1901/dbworkload/blob/main/README.md#1-psycopg-postgresql-cockroachdb)) you will get an error. In Python, different versions of the same library don’t coexist and you might run into a challenge when installing **dbworkload**.

Pyenv makes it easier to install different versions of python and quickly switch between them. It can also be integrated with virtual environment tools like virtualenv using plugin that allow you to create and manage virtual environment specific to each installed Python version.


```pyenv virtualenv 3.12.2 dbworkload```

```pyenv exec pip install "dbworkload[postgres]"```


```pyenv exec pip install psycopg```
