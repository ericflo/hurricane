How to install:

1. Create a virtual environment

    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/hubbub
    source ~/.virtualenvs/hubbub/bin/activate
    easy_install pip

2. Install the requirements

    pip install -r requirements.txt

3. Run syncdb

    python manage.py syncdb

4. Run the comet server

    python manage.py runcomet

5. In another window, get in the new virtualenv

    source ~/.virtualenvs/hubbub/bin/activate

6. Now run the webserver

    python manage.py runcpserver

7. Open your web browser to http://localhost:8088/