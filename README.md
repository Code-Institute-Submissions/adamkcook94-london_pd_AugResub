# London Police Department

A website for a police department that wishes to gain intelligence on and expose alleged criminals
in the local area by inviting the public to submit investigations into them and advertising their
details online. The website offers log in and log out functionality for users, user submission forms,
allowance for users to edit submissions and the ability to view other user submissions. The main goal
of the website is to advertise dangerous criminals in order to keep London safe. Access to the website
can be found [here](https://london-pd.herokuapp.com/)

This website can be categorised as a B2C website as the London Police Department aims to work in
conjunction with the public to keep London safer. Its purpose is to appeal to those in the community
to come forward with information about crimes that have occured across London in order to help the police
catch criminals. The website is designed in a fluid manner, informing the visitor of the importance of
this need which hopefully will lead to them creating an account to help the London Police Department.

The goals of the website are as follows:

- Informing the public of the need to help the London Police Department.
- Informing the public of dangerous criminals in the London area.
- Providing a visually appealing website.
- Providing information on staying safe in the London area.
- Functional design to create a simple process for visitors to create an account and submit information.

The goals of the consumer are:

- Information on dangerous people in their local area.
- Information on staying safe.
- Access to an up-to-date website.
- A website which allows them to report crimes they have seen committed.
- A simplistic design that creates a hassle-free process to create an account to submit information.

## UX

### Ideal Visitor

This website is aimed at those who:

- Live in and around the London area.
- Have information regarding a crime that has been committed.
- Would like to report a dangerous individual.

Visitors to the website will be looking for:

- A safe and secure way to report crimes.
- Information on staying safe.
- Dangerous individuals in their local area to be wary of.

This project helps the consumer achieve this by:

- Offering users a safe and secure path to creating an account to submit reports.
- Providing a page on tips to staying safe.
- Being able to search for their local areas in the 'Wanted Persons' page in order to track dangerous
  indivduals in their area.

## Deployment

### How to run this project locally

To access this project on your own IDE, carry out the following, ensure you have an IDE such as [Visual
Studio Code](https://code.visualstudio.com/)

You will also need to have access to the following:

- [PIP](https://pip.pypa.io/en/stable/installing/)
- [Python 3](https://www.python.org/downloads/)
- [Git](https://gist.github.com/derhuerst/1b15ff4652a867391f03)
- An account with [MongoDB](https://www.mongodb.com/)

### Instructions

1. Go to https://github.com/adamkcook94/london_pd.

2. Save a copy of the GitHub repository by clicking on "Code" at the top of the page and from the dropdown
   menu select "Download Zip". If you have downloaded the aforementioned "Git", you can clone the repository
   with the command:

git clone https://github.com/adamkcook94/london_pd

3. If needed, you can upgrade pip with the command:

pip install --upgrade pip.

4. Install the required modules with the command:

pip - requirements.txt.

5. In your IDE, create a file called "env.py".

6. In "env.py" create a "SECRET_KEY" variable and "MONGO_URI" to connect to your database.

7. You can now run the app with the command:

python3 app.py.

## Heroku Deployment

To deploy this project to Heroku, carry out the following:

1. Create a "requirements.txt" file using the following command:

pip freeze > requirements.txt.

2. Create a Procfile with the command:

echo web: python3 app.py > Procfile.

3. Using "git add" and "git commit" prepare the requirements and Procfile, then "git push"
   the project to GitHub.

4. Create a new app with [Heroku](https://www.heroku.com/) firstly by signing up or logging in,
   and selecting "New" on your dashboard.

5. Give it a name and select Europe as your region.

6. From the dashboard, click on "Deploy", then "Deployment method" and select GitHub.

7. Confirm your wish to link the Heroku app to the correct GitHub repository.

8. From the Heroku dashboard, click on "Settings" and then "Reveal Config Vars".

9. Set the following config vars:

DEBUG = FALSE
IP = 0.0.0.0
MONGO_URI = mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority
PORT = 5000
SECRET_KEY = <your_secret_key>

10. In the Heroku dashboard click "Deploy"

11. In "Manual Deployment" ensure the master branch has been selected and click "Deploy Branch".

12. The site has now been deployed.
