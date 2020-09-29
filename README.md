Python and Data Centric Project Development
Milestone Project 3

# Worldwide Community Cookbook

## Overview
<b>[World Community Cookbook](https://mp-ms3-cookbook.herokuapp.com/)</b> is a site designed to help users find recipes from around the world, either by browsing or searching for a recipe name, ingredient or their favourite cook within the site community.
<br>The site is designed to offer this information to the user in a helpful, user friendly manner.

## User stories
As a.... | I want to... | So that...
---------|--------------|-----------
User|Browse recipes added by others|because I want to increase my recipe portfolio
User|Search for recipes added by others|because I want to increase my recipe portfolio
User|Sign up to become a validated user|I can do things that non validated users can not
Validated User|Add my own recipes|I can share them with others
Validated User|Edit my own recipes|I can make changes if required
Validated User|Delete my own recipe|it is no longer available to others if I choose to remove it
Validated User|Be warned before I delete a recipe|So that I don't delete one by mistake
Validated User|Be able to add a cuisine if the cuisine type for my dish is not present|so that I can add a recipe with my chosen cuisine and therefore people can find my dish by cuisine preference
Validated User|Be able to edit a cuisine I have created|I can ensure the cuisines I have added are accurate, for example if I made a typo
Validated User|Be able to delete a cuisine I have entered|
Site Administrator|Have full control over edit/delete functions|items can be removed or amended if necessary, regardless of whom added the recipe
<br>

## UX
I have used a simple colour scheme and typography for this site - the multitude of bright colours within the recipe images adds the brightness a user would like to see.
<br>

## UI
The user interface  is intuitive with positive or negative feedback provided to the user where appropriate.

## Wireframe


## Features
### Existing Features
1. User registration
2. User login
3. User logout
4. Add recipe
5. Edit recipe (by creator or administrator only)
6. Delete recipe (by creator or administrator only)
7. Add a cuisine type
8. Edit a cuisine type (by creator or administrator only)
9. Delete a cuisine type (by creator or administrator only)
10. Browse for a recipe
11. Search for a recipe 

### Features for the future
1. I would like to implement a file upload feature so that users can use their own photo's of their recipes
2. Potentially allow users to create new meal-courses for example "breakfast" (not currently available)
3. User ability to add a rating to a recipe
4. User ability to mark as a "favourite"
5. Password reset and forgotten password feature

## Technologies used
1. [HTML](https://en.wikipedia.org/wiki/HTML5)
2. [CSS](https://en.wikipedia.org/wiki/CSS)
3. [JavaScript]
4. [Bootstrap v4.3.1](https://en.wikipedia.org/wiki/Bootstrap_(front-end_framework))
5. [Python 3.8.0](https://en.wikipedia.org/wiki/Python_(programming_language))
6. [Flask 1.1.2](https://en.wikipedia.org/wiki/Flask_(web_framework))
7. [Werkzeug 1.0.1](https://en.wikipedia.org/wiki/Flask_(web_framework))
8. [Pymongo]
9. [Mongo DB Atlas](https://en.wikipedia.org/wiki/MongoDB)

## Database & Schemas
I have used Mongo DB Atlas for my database.<br>
From The Mongo DB site:<br>
>MongoDB Atlas is a fully-managed cloud database developed <br>by the same people that build MongoDB. Atlas handles all the complexity of deploying, managing, and healing your deployments on the cloud service provider of your choice ( AWS , Azure, and GCP ).
<br>

The database (Database name: cooking) is made up of collections of documents <br>
<br>
## Collections:<br>

### cuisines
| Field Name | Data Type
---------|--------------|
|_id|ObjectID
|cuisine_name|string
|created_by|string
<br>

### meal_course
| Field Name | Data Type
---------|--------------|
|_id|ObjectID
|course_name|string
<br>

### users
| Field Name | Data Type
---------|--------------|
|_id|ObjectID
|username|string
|password|Binary hashed
|email|string
|role|string
<br>

### recipes
| Field Name | Data Type
---------|--------------|
|_id|ObjectID
|recipe_name|string
|cook_name|string
|prep_time|string
|total_cooking_time|string
|servings|string
|ingredients|Array of strings
|instructions|Array of strings
|image_src|string
|meal_course|string
|protein|string
|fat_per_serve|string
|carbohydrate|string
|dietary_fibre|string
|cholesterol|string
|energy|string
<br>
The recipe collection consists of data from all collections combined to give the "final" recipe.<br>
This can then be edited by the user whom created it or a user with the role "admin"
<br><br>

## Testing

My site has been tested using Google Chrome Developer tools to ensure that the screen changes behaviour on different screen resolutions.

Tested on the following browsers:

Google Chrome
Mozilla Firefox
Internet Explorer
Safari

Manual testing has been carried out by my wife and I using the user stories above.<br><br>
HTML and CSS has been validated using [W3 HTML validator](https://validator.w3.org)
JavaScript has been validated using [JSHint](https://validator.w3.org)
Python has been validated using the flake8 linter within VS Code

## Deployment
This code was developed using Visual Studio Code<br>
It was committed to git and pushed to Github for version control
From there automatic deploys were made via Heroku, where the application is hosted.
<br>To capture the code for continuing development
1. [Use this link](https://github.com/matthewpoyner/mp-ms3-cookbook)
2. Click on Clone or download button
3. Select Open in Desktop
4. Use it in GitHub Desktop
<br>Using VS Code
<br>
<br>To install the requirements for this app
 use this command:<br>`pip install -r requirements.txt`
<br>
Ensure that environment varaiables are kept in a file called env.py
<br>
And that this file is added to your gitignore file
## To see the deployed website click the link below
[https://mp-ms3-cookbook.herokuapp.com/](https://mp-ms3-cookbook.herokuapp.com/) 

## Credits
@tim_ci on slack for his thread on searching for a document in Mongo DB Atlas<br>https://code-institute-room.slack.com/archives/C7JQY2RHC/p1595504612220600?thread_ts=1595502710.214500&cid=C7JQY2RHC<br>
<br>
Anthony Herbert -> Pretty Printed<br>
For his You Tube Video<br><br>
On Flask login sessions<br>
 https://www.youtube.com/watch?v=vVx1737auSE
<br>
[Ranker: Your Favourite Types of Cuisine](https://www.ranker.com/crowdranked-list/favorite-types-of-cuisine) 
<br>This was used to find out the top 20 cuisines, to help start off the cuisine dropdown list

## Acknowledments
Thank you to my mentor for pushing me to be better and for offering me valuable feedback.<br>

A massive thankyou to my wife for supporting me throughout this project and for being my chief tester for UAT<br>

Thanks also to my fellow students on Slack for helpful advice.

## Development Notes
My local development was carried out in a branch "develop", I got a bit confused with how to deploy this to the master and after some struggling I was able to get it working. I used git reset to tidy up my repository

### This site is for educational use