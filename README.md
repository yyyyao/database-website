# NBA-DATA
clone the repository and run 
```
python main.py
```
Go to http://0.0.0.0:8111/ for the local server.

User needs to signup/login first, and then search the players or teams data.


* The PostgreSQL account where your database on our server resides: 
    
    yw3225

* The URL of your web application：
    
    http://34.73.3.228:8111

* A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway:

    We implemented the functions of signup, login, inseart, search. To be more precise, users can search the information of each basketball player, team, and game result, etc, as well as interact with the website by input the name of a player or a team. There will be links to the Amazon NBA fan shop for the team or the player. Also, users can login by their username. After login, users can do all the interact things including modifying the data by filling a request form, and the data will be posted on the website after administrator approve it. 
    The part we didn’t implement is subscribing and voting. As these two functions are not mainly based on execute SQL queries. Also, subscribing and voting have no interaction with our other entities in the database. Thus, we decide not implement the part. Instead, we spent our time on more interesting things like how to make our database more functional and attack protectable. 

* Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

    The signup page require some interesting database operations. As we use select to check if the username or email had already exist in the database. If duplicate, we have an informing message indicating that the username/email was used by other people; if not, we insert that information to our user table and jump to the login page. Moreover, both signup and login page have some validator. Your username must  be between 3 and 15 characters long, or our page would give an error message.
    The search page is also interesting. Once you type the existing player in our database, you can go to the webpage that shows all the information of that player. In that player page, you can see a link that can lead you to the player’s team.

