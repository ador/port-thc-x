# port-thc-x

Finding outliers in ports' terminal handling charges (demo project).


## How to start a dev server (Flask)


```
$ cd python 
$ pip3 install -r requirements.txt
$ ./run_server.sh
```

Then check the JSON response in a browser (or with Postman) at "http://localhost:5000/histogram/US".
It should be something like:

```
{
  "data": [
    {
      "label": "5.00 - 18.04",
      "normal": 0,
      "outlier": 2
    },
    {
      "label": "18.04 - 31.08",
      "normal": 18,
      "outlier": 0
    },
    {
      "label": "31.08 - 44.12",
      "normal": 0,
      "outlier": 3
    }
  ]
}
```


## How to start a dev client server (React)

```
$ cd client/port-ol-app
$ npm install
$ npm start
```

This will start up a new browser tab for "http://localhost:3000/" where you can 
interact with the server.

Click a country in the list on the left to see its histogram chart.


#### Notes
In the current setup the React dev server is proxying requests to 'localhost:5000'.


