# Family Game Night

#### Video Demo: https://youtu.be/VbK14MqoFeE

#### App deployed on Heroku:
https://fgn-cs50.herokuapp.com/

#### Description:

I wanted to make something that I would use, and that would take a lot of what we learned in the course, and a little extra. Here's what I came up with!

Family Game Night is a web app developed by myself (Chad Campbell) as a final project for Harvard CS50x: Intro to Computer Science. The project uses micro framework Flask with Python and Jinja syntax for some logic to show database information on the apps routes. HTML, CSS with bootstrap, and Javascript were used on the front end. SQLite3 was used for the database. *Note: SQLite3 does not store information persistantly on Herokus free service.* I have the app hosted on Heroku with their free account tier. So now anyone can use it! The code is also up on my personal github. Learning how to set up github and the heroku service was fun!

#### Pages:

###### Index:
This is the landing page that just greets the user and explains the purpose of the app, if they are logged in. If not they are redirected to login.

###### Login/Register:
These forms are validated with SQL queries and a hash for the password made using werkzeug.security. Then the user id will be the primary key for all other databases.

###### Family/Games:
These forms and data tables INSERT and show SELECTED data for the apps other services, the leaderboard/history and the "wheel".

###### History/Leaderboard:
The forms on this page only allow inputs from the data tables controlled on the Family or Games page, but they INSERT into their own table. This way games and family members can be added and removed while the historical data here will remain.

###### Spin the Wheel:
The Wheel was a bit tricky. I wanted something that would change dynamically based on the users games table. Most iterations of this I could find prior were done with mainly CSS and were static. The answer was winwheel.js. A Javascript library that does the heavy lifting by utilizing a canvas element in HTML. Adding some loops and some of the built in functions of the library the segments of the wheel are created with the data from the SQL table associated with the users games. If there are less than two segments the page will tell you to add more. It has functions to add/remove segments, add sound to the canvas, and I also set up the fillColor function to match my web apps color scheme. I first tried to do this with Jinja inside the functions, but found it easier to get the data types right by first loading the SQL info into Javascript data types and using the JS itself for the functions. 

#### Thank you to everyone at CS:50 for the knowledge and the fun! On to the next learning adventure!