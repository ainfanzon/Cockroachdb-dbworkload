# Corckroachdb-dbworkload Enablement Exercise.

## Install dbworkload.

If you have installed different versions of Python from various sources, including Homebrew, the Official Installer, and Conda then the package manager (pip) will try to resolve the dependency conflict for you and install the most suitable version instead. The example below shows I am using a the anaconda3 Python binary.

<code>% which python
/opt/anaconda3/bin/python
</code>

If you try to install **dbworkload** ([see github readme.md](https://github.com/fabiog1901/dbworkload/blob/main/README.md#1-psycopg-postgresql-cockroachdb)) you will get an error. In Python, different versions of the same library don’t coexist and you might run into a challenge during the installation.

**[Pyenv](https://realpython.com/intro-to-pyenv/)** makes it easier to install different versions of python and quickly switch between them. It can also be integrated with virtual environment tools like virtualenv using a plugin that allows you to create and manage a virtual environment specific to each installed Python version.

Once you have **pyenv** you can install multiple versions of Python. The **pyenv versions** command shows which versions of Python are available.

<code>% pyenv versions
system
3.12.2
pypy3.10-7.3.15
pypy3.10-7.3.15/envs/mt_app
</code>

To install a new virtual environment using one of those versions and give it a name you can run pyenv like this: 

<code>pyenv virtualenv 3.12.2 dbworkload</code>

The newly created virtual evironment should be listed in the output of the **pyenv versions** command:

<code>% pyenv versions
system
3.12.2
3.12.2/envs/dbworkload
\* dbworkload --> /Users/ainfanzon/.pyenv/versions/3.12.2/envs/dbworkload (set by /Users/ainfanzon/dbworkload/.python-version)
  mt_app --> /Users/ainfanzon/.pyenv/versions/pypy3.10-7.3.15/envs/mt_app
pypy3.10-7.3.15
pypy3.10-7.3.15/envs/mt_app
</code>

Once the virtual environment has been created, the Python version selected will be active

<code>% which python
/opt/anaconda3/bin/python</code>

Now you should be able to install dbworkload using pyenv:

```% pyenv exec pip install "dbworkload[postgres]"```<br>
```% pyenv exec pip install psycopg```

and execute the **dbworklod** command:

<code>% dbworkload<br>
 Usage: dbworkload [OPTIONS] COMMAND [ARGS]...<br>
 dbworkload v0.4.1: DBMS workload utility.<br>
 <br>
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮<br>
│ --version             -v        Print the version and exit                                       │<br>
│ --install-completion            Install completion for the current shell.                        │<br>
│ --show-completion               Show completion for the current shell, to copy it or customize   │<br>
│                                 the installation.                                                │<br>
│ --help                          Show this message and exit.                                      │<br>
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯<br>
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮<br>
│ run                   Run the workload.                                                          │<br>
│ util                  Various utils.                                                             │<br>
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯<br>
<br>
 GitHub: <https://github.com/fabiog1901/dbworkload></code>

## Using 3 node CRDB cluster on localhost.

### Step 0: Launch a CRDB insstance and clone the repository

<code>% git clone https://github.com/ainfanzon/Cockroachdb-dbworkload</clode>

### Step 1: Create the northwind database

Use the following command to create the **northwind** database and the tables:

<code>% cockroach sql --url "postgres://root@localhost:26257/defaultdb?sslmode=disable" --user root --database defaultdb --insecure --file northwind.sql</code>

 Once the database has been created, use **sbworkload** to generate an intermediate representation of what needs to be generated - a definition file - in YAML syntax.

 <code>% dbworkload util yaml --input northwind.sql -o northwind.yaml</>
