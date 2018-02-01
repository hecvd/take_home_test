How To Use:

## Install requirements:

Install the requirements for the app with this command:

(Preferably using a virtualenv)

```bash
$ pip install -r requirements.txt
```

## Console version:

To run the console version of the app, use this command:
```bash
$ python main.py
```

## Web Version:

To run the web version of the app, use this command:
```bash
$ python flask_server.py
```

This should start a flask server at [http://127.0.0.1:5000/](http://127.0.0.1:5000) by default.

Visit the page and the result of the test should be there.


## Testing

To run the tests, use this command:

```bash
$ python -m unittest discover tests  "*_test.py"
```


## Coverage

To generate coverage, run 

```bash
$ coverage run --source=.,celebration_app,blueprints,distance_calculator -m unittest discover tests  "*_test.py" 
$ coverage html
```

It will generate a directory named `htmlcov`

Then, open in your browser the file `htmlcov/index.html` to see the report. 
