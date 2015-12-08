First you must obtain an application id and secret from fb,
you can do this by registering as a developer on their website
https://developers.facebook.com/
The website should get you started

Then you must edit fbg.py and replace the relevant fields with
 the strings just obtained, also replace rootId, it is the page id
from which the data will be extarcted

In order to run the programs the folowing dependencies are required:
numpy, matplotlib, facebook-sdk, arrow, requests

Now you must obtain the data(The timestamps of the posts and
comments on its own page of the page user) run fbg.py

Finaly run histogram.py and histogramw.py to generate the relevant
charts.
