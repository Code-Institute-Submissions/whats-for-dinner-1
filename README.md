# What's For Dinner?

[View the live project here](#)

**What's for Dinner?** is an online resource aimed at sharing recipes with friends to help people as a way of staying in touch during lockdown.

The primary goal of this project is to create  an online resource where users can share recipe ideas, ingredient lists, and browse for ideas on what to cook for their next lockdown meal.

---

## Contents

1. [Contents](#Contents)
2. [Project Background](#Project-Background)
3. [UX Design](#UX-Design)
   - [User Stories](#User-Stories)
   - [Wireframes](#Wireframes)
   - [Development](#Development)
4. [Features](#Features)
   - [Existing Features](#Existing-Features)
   - [Features Left to Implement](#Features-Left-to-Implement)
   - [Known Issues](#Known-Issues)
5. [Technologies Used](#TechnologiesUsed)
   - [Languages](#Languages)
   - [Libraries](#Libraries)
   - [Other Tools](#Other-Tools)
6. [Testing](#Testing)
   - [Test Process](#Test-Process)
   - [Tests Conducted](#Tests-Conducted)
7. [Deployment](#Deployment)
   - [Deploying on Github Pages](#Deploying-on-Github-Pages)
   - [Differences between deployed version and development version](#Differences-between-deployed-version-and-development-version)
   - [Cloning a local version](#Cloning-a-local-version)
8. [Credits](#Credits)
   - [Content](#Content)
   - [Media](#Media)
   - [Acknowledgements](#Acknowledgements)

## Project Background

This project is being completed as part of a Full Stack Developer Diploma award. This forms the basis for the developer's first milestone project. As such it will be completed within a set of guidelines as to which technologies to use.

While the core focus of the project is to be submitted as the summative assessment for the student developers course, it is also hoped that the resource itself, and the brand created for it can be developed over time into something that can be of value to the wider community.

[BACK TO CONTENTS](#Contents)

---

## UX Design

### User Stories

With the target users in mind, the following user stories are generated.

- As a user I should be able to browse a list of available recipes by cuisine type
- As a user I should be able to view individual recipes, and see an ordered list of steps to create each one
- As a user I should be able to view ingredient lists for individual recipies
- As a user I should be able to see an image of the finished recipe
- As a user I should be able to create a new recipe to add to the shared database
- As a user I should be able to make edits to an existing recipe in the shared database
- As a user I should be able to delete old recipes from the database

### Wireframes

Wireframes were created for all basic views on both mobile devices as well as web devices. They have been included for the convenience of the examiners in the [github repository](https://github.com/bryansmullen/whats-for-dinner).

---

## Features

### Existing Features

- Shared list of cuisine styles
- Shared list of recipes within each cuisine
- List of ingredients for each recipe
- Ability to upload accompanying image for each recipe
- Ability to create ingredients list for recipes
- Ability to view ingredients list for recipes
- Ability to edit ingredients list for recipes
- Ability to delete ingredients for recipes
- Ability to create ordered instructions for each recipe
- Ability to view ordered instructions for each recipe
- Ability to edit instructions for each recipe
- Ability to delete instructions for each recipe
- Ability to create new recipe items
- Ability to view recipe items
- Ability to edit recipe items
- Ability to delete recipe items

### Features Left to Implement

- Ability to update image of recipe
- Automated testing of project
- Ingredients & Instructions could be formatted as lists if there were a more user friendly way to allow for an indefinite number of input fields and the tracking of associated units for ingredients.

### Known Issues

- Flask Form populates an image data uri to the first item in the form when attempting to update
- Unable to pre populate image field in update form
- Users can submit multiple ratings from the same account
- Recipe name cannot currently contain any spaces - this was in an effort to disallow recipe names including only spaces. Requires addressing in the future.

[BACK TO CONTENTS](#Contents)

---

## Technologies Used

In this section, I will mention all of the languages, frameworks, libraries, and any other tools that I have used to construct this project.

### Languages

- [HTML](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) is used to render the content of the website.
- [CSS](https://www.w3.org/Style/CSS/#specs) is used to style the content of the website.
- [Javascript](https://www.w3schools.com/js/DEFAULT.asp) is used for initialising front end functionality
- [Python](https://www.python.org/) is used for backend logic and serving of files

### Frameworks

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) is the prescribed framework for this project
- [Jinja 2](https://pypi.org/project/Jinja2/) is templating language used

### Libraries

- [Materialize CSS](https://materializecss.com/) is used for presentation

### Other Tools

- [Git](https://git-scm.com/) is used for version control in this project. Throughout the project, a Develop branch has been added to the project to allow work to continue on the website without breaking the functioning version on the Master branch.
- [Github](https://github.com/) is used as a remote repository for the site, as well as for deployment of the final version.
- [Pycharm](https://www.jetbrains.com/pycharm/) was used as IDE
- [MongoDB](https://www.mongodb.com/) was used as a database solution
- [AWS S3](https://aws.amazon.com/s3/) was used to host images
- [Heroku](https://www.heroku.com/) was used for deployment

[BACK TO CONTENTS](#Contents)

---

## Testing

- In the absence of a specific, detailed and comprehensive module on automated testing provided by the course, manual testing has been opted for. It is assumed that this will not be penalised.
- The deployed, live version of the site was utilised for the tests.

### Tests Conducted

#### Finished Project Tests

The function of these tests is to ensure that the finished project renders acceptably on all intended devices. Four sets of tests were completed:

- Validation
- Modelled Device Testing
- Automated Cross Browser Testing
- Manual Browser Testing

#### Validation

Validation took place on HTML, CSS, JS, and Python files in the project. With the exception of a number of 'line too long' errors in python which would have caused tradeoffs in legibility, and an erroneous javascript error (stemming from the validator not having access to the function call), no errors returned.

#### Modelled Device Testing

To test the layout on multiple devices, Google Chrome DevTools is used to simulate the size of multiple devices and screen ratios. Screen responsiveness has been noted to ensure the correct screen ratio was delivered, links are tested by clicking through, images are checked to ensure they displayed correctly on all devices, and the website as a whole is checked to ensure everything renders as expected. Any faults or issues were noted in the [Device Testing Chart](testing/testing_charts/testing-spreadsheet.ods)

The following device dimensions are tested:

- Moto G4
- Galaxy S5
- Pixel 2
- Pixel 2 XL
- iPhone 5/SE
- iPhone 6,7,8
- iPhone 6,7,8 Plus
- iPhone X
- iPad
- iPad Pro
- Surface Duo
- Galaxy Fold
- Desktop


#### Automated Cross Browser Testing

To test the layout on multiple browsers, [browserstack](https://www.browserstack.com) is used to emulate different browsers running on virtual machines. Results are documented in [Device Testing Chart](testing/testing_charts/testing-spreadsheet.ods). The following browsers are tested:

- Catalina 13.1
- Firefox 82
- Chrome 64
- Opera 48
- Yandex 14.12

#### Manual Cross Browser Testing

To complement the above results the website is also tested manually on up-to-date browsers available on the developer's machine. The results are once again documented in the [Device Testing Chart](testing/testing_charts/testing-spreadsheet.ods)

The following browsers are tested:

- Edge
- Brave
- Chrome

[BACK TO CONTENTS](#Contents)

---

## Deployment

This project is deployed on Heroku, which can be accessed at [What's For Dinner](https://github.com/bryansmullen/whats-for-dinner) or [What's For Dinner Deployed Version](https://bryansmullen-whats-for-dinner.herokuapp.com/). The deployment is linked to the Master Branch of the repo, and will automatically update the deployment when any changes are committed to this branch of the remote repository. The deployment procedure is documented below.
- Project was initialized as a git repository
- A remote repository was linked to the project using github
- Code was commited to git and pushed to github taking care to ignore sensitive files, for example env.py, as well as venv folders and notes files
- It was ensured that both an up-to-date requirements.txt file was maintained, and a Procfile to configure heroku also existed
- A remote repository was created for the project using heroku
- Environment variables from the local environment were added to heroku's config variables
- Heroku was configured to automatically deploy from the github master branch

[BACK TO CONTENTS](#Contents)

## Cloning a Local Version

The procedure for cloning a local version on a windows machine is detailed below. Instructions for Mac/Linux will be considered at a later date.

- Ensure Git, Python, Pip, and PyCharm are installed on your machine
- Clone the [github repository](https://github.com/bryansmullen/whats-for-dinner/) using `git clone https://github.com/bryansmullen/whats-for-dinner.git`
- Within the created folder, create and activate a virtual environment
- Install the project requirements within the virtual environment the requirements.txt file
- Create and configure a MongoDB database
- Create and configure an instance of AWS S3 with a Bucket
- Create environment variables for each of the following:
    - IP
    - PORT
    - MONGO_DBNAME
    - MONGO_URI
    - SECRET_KEY
    - aws_access_key_id
    - aws_secret_access_key
    - BUCKET_NAME

[BACK TO CONTENTS](#Contents)

---

## Credits

### Content

The inspiration for this project came from Matthew Dudek's lockdown facebook series.

### Media
- Background image by Vaibhav Jadhav from Pexels
- CSS Background Image overlay logic - learnwithparam.com
- Photo by Tranmautritam from Pexels
- Photo by Rajesh TP from Pexels
- Photo by Acharaporn Kamornboonyarush from Pexels
- Photo by Rachel Claire from Pexels
- Photo by Marvin Ozz from Pexels
- Photo by Daria Shevtsova from Pexels
- Photo by Anna Shvets from Pexels
- Favicon from https://www.freefavicon.com/freefavicons/food/downloadicon.php?ico=fast-food-triple-cheeseburger-204444.zip
### Acknowledgements
- Whitespace validation from [nullskull](http://www.nullskull.com/q/10393870/white-space-validation-in-javascript.aspx)

[BACK TO TOP](#What's-For-Dinner?)