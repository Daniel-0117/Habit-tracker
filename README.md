# Habit Tracker


Live deployed link or Walkthrough: https://app.screencastify.com/watch/D2yc9U9m2683LPSK6XfX

![Static Badge](https://img.shields.io/badge/MIT-license?label=license&labelColor=%2332CD30&color=%23A020F0&link=https%3A%2F%2Fopensource.org%2Flicense%2Fmit%2F)

## Description
This project was created so that users will have the backend for a habit tracker app. It performs many of the functions needed for a habit tracker app such as creating, deleting, and getting a user along with their habits. 

## Usage
To use this application the user must clone the repo. Then once properly cloned the user has to perform pip i into the integrated terminal, once all the modules have been properly installed the application is ready to be used. To test this without a front end use a program such as Insomnia to test the various endpoints. 


  ## Table of Contents

- [Description](#description)

- [Usage](#usage)

- [Technologies used](#technologies-used)

- [Credits](#credits)

- [Team's Githubs](#team-githubs)

- [License](#license)

- [Project requirements](#project-requirements)

## Technologies used!
We ended up using quite a few different things!
- Python
- FastAPI
- PostgreSQL
- SQLALchemy
- Pydantic
- Passlib
- Uvicorn
- Virtualenv 
- dotenv
- Insomnia (Api Testing)

## Credits
https://github.com/Daniel-0117

## License
![Static Badge](https://img.shields.io/badge/MIT-license?label=license&labelColor=%2332CD30&color=%23A020F0&link=https%3A%2F%2Fopensource.org%2Flicense%2Fmit%2F)


## Acceptance Criteria:
GIVEN a RESTful API
WHEN I register and log in,
THEN I receive a secure token to authenticate my requests.

WHEN I send a POST request to create a habit,
THEN the new habit is saved in my personal list.

WHEN I send a GET request to view my habits,
THEN I receive a list of all habits I have created, sorted alphabetically.

WHEN I send a PATCH request to update a habit,
THEN the habit’s name is updated in my personal list.

WHEN I send a DELETE request for a habit,
THEN the habit is removed from my personal list.

WHEN I send a GET request for my user info,
THEN I receive my account details (email, ID, and habits).

WHEN I send a DELETE request for my user account,
THEN my account and all related habits are deleted from the system.

WHEN I try to access another user's data,
THEN I am denied access.

### User Story!

As a productive user. I want to securely track my habits through a web API. So that I can manage my personal goals and daily routines efficiently. 