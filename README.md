# Finance Tracker
### Video Demo:  https://youtu.be/zGPy_67vVig
### Description:
Finance Tracker is a web app made using the python library Flask that allows users to add in logs and keep track of their savings.

Logbook: The logbook stores all your transactions (logs) that you have recorded. Logs come in 2 forms, spent (shown in the dashboard as red) and received (shown in the dashboard as green/blue) and include information you have entered such as what the purchase was made for / where you received the money from as well as the amount you gained/lost. These logs are sorted in the dashboard the most recent being on the top.

Savings: Savings allow users to keep track of a certain amount of money meant to be spent on a certain, ideally big, purchase.

Finance Tracker stores all these in your account which you can create using a username and password.

#### Pages:
- landing page: The landing page advertises the website's key features in short, digestible, sentences. Content such as the text about the website and the images displaying the websites functionality appear dynamically as the user scrolls down the page.
- register: allows the user to register for the website by adding a username and password, if the username already exists an error message displaying Username taken underneath the text field as well as an erorr icon will appear upon submission. Password must be entered twice to be confirmed.
- login: Allows the user to login with their username and password
- dashboard: contains a welcome message, the user's current balance (defaults to 0 for a new account) and the logbook with entries arranged from the most recent
- new_log: allows user to create a new entry with 3 pieces of information, transaction_type (received / spent), notes and amount, all of which are compulsory and a failure to enter any one of them will result in an error message underneath the text field as well as an error icon on the right hand side of the text field.
- savings: displays 3 items on the page: amount in savings, savings up for, required savings
    - of amount in savings is equal to or greater the required savings the color of the text changes to green to signal to the use that they are able to make the purchase, if not it defaults to red unless the user has not specified an amount in savings, in which case in default to black.
- edit_savings: allows users to change their amount in savings, what they are savings up for, and their required savings
    - users are allowed to leave all fields blank in the case where they are not saving up for anything
        - amount and required amount both default to 0 and saving up for defaults to not savings up for anything
- settings: contains 3 actions, out, change password, delete account
    - logout: logs the user out by clearing the session then redirecting them to the landing page
    - change_password: allows a user to change their password after confirming their old password, new password must be entered twice to confirm
    - delete_account: deletes all information in all 3 databases concerning the user (using the users id), the user is asked to type in their username and password to confirm the action. The account is unretrievable after deletion.

#### Databases:
- Database: tracker. db
- users: stores all users, their IDs, hashed passwords and balance
    - id: numeric
    - user: text
    - hash: text
    - balance: numeric
- logbook: stored logbook data
    - user_id: numeric (corresponds with users.id)
    - transaction_type: text (should only be 2, either spent of recieved)
    - notes: text (cant be left empty)
    - amount: numeric
- savings: stores savings data
    - amount_in_savings: numeric (when left empty defaults to 0)
    - saving_up_for: text (when left emptry defaults to Not saving up for anything)
    - required_savings: numeric (when left empty defaults to 0)

#### Design
The website is built using the CSS provided by Bootstrap, specifically the Bootswatch Lux theme (learn more in Bootstrap.css). This theme was chosen as it allows for a luxury feel, perfect for a web app centring around finance and finance management. The Landing page uses animations for each card to further intensify the luxury of the web app. The black and white accent colours of the website present a minimalistic, simple feel showcasing this web app and one built for the less "tech savvy" people with fewer things to configure.

#### File structure
All html templates are stored within the templates folder, a total of 11 html files are used in this project. Images for the landing page, the websites favicon (provided by Icons8), the bootstrap CSS styling used in the website as well as the script written in JavaScript used to make the cards in the landing page move are stored within the static folder. the app.py file and well as the tracker.db sqlite databse are kept in the parent folder project.

#### Error messages
Majority of the html files containes a few lines of code in case a user were to input an unexpected value in order to render a message underneath the text field as well as an error icon on the right hand sign. These styling are provided by boostrap. Below is a list of every error message in every html file, only unique erorr messages are defined.

- change_password
    - wrong_password: when the old password inputted by the user does not match the password in the database
    - empty_password: when the new password field is empty
    - unmatch_password: when the new password and the confirmed password do not match
- delete_account
    - missing_username: the user does not provide a username in the text field
    - error_username: the username is incorrect (does not match the database username)
    - missing_password: the user does not provide a password in the text field
    - error_password: the password is incorrect (does not match the databases hash)
- index: None
- landing: None
- layout: None
- log
    - invalid_option: if the user (somehow) chooses an option thats not offered in the select menu (spent/recieved)
    - empty_option: if the user does not choose an option
    - missing_notes: if the user does not write any notes (notes field left empty)
    - invalid_amount: if the amount the user inputs is invalid (not a number)
    - missing_amount: if the user fails to enter an amount (field left empty)
    - not_enough: if the transaction type chosen is spent and the amount spent is greater than the users balance
    - exceed_limit: if the user exceeds the max amount input of 1,000,000
        - this limit is created to ensure that the user does not input an insanely long number
- login
    - missing_username
    - error_username
    - missing_password
    - error_password
- register
    - used_username: the username already exists in the database
    - empty_username: the user does not provide a username in the text field
    - empty_password
    - unmatch_password: when the new password and the confirmed password do not match
- savings_edit
    - invalid_amount
    - not_enough
    - invalid_req_amount: same as invalid_amount
- savings: None
- settings: None

