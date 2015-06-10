#Mapster

With so many things to see, do, and eat, Mapster provides a spatial reference for travelers to efficiently plan their trips. Users can search for something to do, compare and research the results, and save the location to their map, where they can view and customize it to their liking.


####Technology Stack
JavaScript, jQuery, HTML, CSS, AJAX, BootStrap, Python, Flask, Jinja, SQLAlchemy, SQLite



####Search and Destination

On the Homepage, users input a search, destination, and sort parameter. Doing so, the Yelp API is being called and queried. The returned results will appear in the next page where users can compare locations with star ratings, review count, category, and a link to the yelp page for additional research one may want to do. 

![image]("/static/images/homepage.png")



#### Saving Markers
Once the user chooses a location to add to their map, a modal window will appear, prompting the user to choose a map category and any additional notes they have for that specific location. On the map, the map category becomes a checkmark box, turning on and off the markers on the map that are associated with that category.

<p align="center">
  <img align="center" src="/static/images/results.png" alt="Home-Page">
</p>

#### Marker Information
For each marker displayed on the map, a info window is assigned to it. When a marker is clicked, the info window appears, displaying all the specific information about that maker location and your personal notes you may have included.

<p align="center">
  <img align="center" src="/static/images/modal.png" alt="Home-Page">
</p>

<p align="center">
  <img align="center" src="/static/images/map.png" alt="Home-Page">
</p>




##Get Mapster Running on Your Machine

Clone or fork this repo: 

```
https://github.com/judychau/Mapster.git

```

Create and activate a virtual environment inside your project directory: 

```

virtualenv env

source env/bin/activate

```

Install the requirements:

```
pip install -r requirements.txt

```

Get your own secret keys from Yelp (https://www.yelp.com/developers) and save them to a file <kbd>secrets.sh</kbd>. You should also set your own secret key for Flask. Your file should look something like this:

```
export CONSUMER_KEY='YOURCONSUMERKEYHERE'
export CONSUMER_SECRET='YOURCONSUMERSECRETKEYHERE'
export TOKEN='YOURTOKENHERE'
export TOKEN_SECRET='YOURTOKENSECRETHERE'

```
	
Source your secret keys:

```
source secrets.sh

```

Run the app:

```
python server.py

```
Navigate to `localhost:5000/home` to create your own travel maps!

##Future Plans

Check out the [issues log for this project] (https://github.com/judychau/mapster/issues) to see what's up next.


