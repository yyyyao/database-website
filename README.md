# NBA-DATA
clone the repository and run 
```
python main.py
```
Go to http://0.0.0.0:8111/ for the local server.

User needs to signup/login first, and then search the players or teams data.


* The website has the functions of signup, login, inseart, search. To be more precise, users can search the information of each basketball player, team, and game result, etc, as well as interact with the website by input the name of a player or a team. There will be links to the Amazon NBA fan shop for the team or the player. Also, users can login by their username. After login, users can do all the interact things including modifying the data by filling a request form, and the data will be posted on the website after administrator approve it. 


* The signup page require some interesting database operations. As I used select to check if the username or email had already exist in the database. If duplicate, the page would have an informing message indicating that the username/email was used by other people; if not, the signup page would insert that information to the user table and jump to the login page. Moreover, both signup and login page have some validator. Your username must be between 3 and 15 characters long, or the page would give an error message.
    The search page is also interesting. Once you type the existing player in our database, you can go to the webpage that shows all the information of that player. In that player page, you can see a link that can lead you to the player’s team.

