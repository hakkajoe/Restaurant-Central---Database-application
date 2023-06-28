# Restaurant-Central---Database-application

## How to run the application

(0) If not yet installed, install PostgreSQL on your device

instructions: https://github.com/hy-tsoha/local-pg

1. Clone the application repository to your device


```bash
git clone https://github.com/hakkajoe/Restaurant-Central---Database-application
```

2. Open psql and create a new database, and then copy the contents of the schema.sql -file to that database

```bash
CREATE DATABASE <name of the database that you can choose>
```
```bash
psql -d <database name that you chose> < schema.sql
```

3. Create .env file to the cloned folder with the following content:


DATABASE_URL=postgresql+psycopg2:///(name of the database that you chose in phase 2)

SECRET_KEY= (secret key of your choosing)


4. Create virtual environment in the cloned folder and activate it

```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

5. Install dependent libraries

```bash
pip install -r requirements.txt
```

6. Initiate application with command

```bash
flask run
```

## How the application works

The application is  website that acts as a database for listing restaurants and restaurant reviews

The purpose of this application is to act as a website that lists restaurants and their characteristic information. The application can be accessed both by a website administrator as well as regular users. An administrator account is already created and it's credentials can be found in a separate [notes](https://github.com/hakkajoe/Restaurant-Central---Database-application/blob/main/notes) document. Regular user accounts can be created when the application is launched or when the user chooses to sign out of the application through the main page. 

The administrator can add restaurants to the website, a description for the restaurant as well as tags that can be utilized to find the restaurants with a search function. The administrator can also later edit or remove restaurant descrptions and tags, as well as remove restaurants from the website. When a restaurant has been listed to the website, users can find them listed on the main page of the application, and sort the listing order either in alphabetical order or in the order of the average rating of the restaurants. Users can also search for specific restaurants with a search function, that looks for text from both restaurant descriptions as well as assigned tags, that matches the user's search input. 

From the main page, all users can write reviews for restaurants, which include both a text review and a star rating from 1 to 5. Users can also read other peoples reviews. Administrator can delete individual reviews from the review listing pages if they wish to do so. 
