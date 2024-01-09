![LCO logo](/img/LCO_logo.png)
<br>
<br>
<br>
![MeteoBlue logo](/img/meteoblue_logo.png)

# LCO Meteorology

This project displays the meteorology data obtained from 2 sources: **Vaisala** and 
**Meteoblue**, this data is obtained using **lcodataclient module** which returns the 
information in a pandas dataframe. The data is displayed in dashboards using: 
Django, Dash and Ploty. To integrate all of these 3 technologies the project uses **django_plotly_dash**. All of this is done following the OOP paradigm, PEP 8 and the folder structures that Django gives.

<p align="center">
  <a href="#how-it-works">How it works</a>
  <a href="#getting-started">Getting Started</a> •
  <a href="#installing">Installing</a> •
  <a href="#built-with">Built with</a>
</p>

## How it works
1. Creates django project: The whole application lives in a Django project
2. Create django app: There is only one app which is the **dashboards** folder
3. Creates dash apps inside django app: Inside the app there is 2 dash apps
one for the Vaisala and the other for the Meteoblue dashboard.
4. Dash apps are called within the django views: The apps are rendered usign 
the django views. For more info in django views check [this](https://docs.djangoproject.com/en/5.0/intro/tutorial01/#write-your-first-view).

- In a nutshell the project structure is like this: 

<p align="center">
  <img src="img/lco_meteorology_structure.png" alt="Project structure"/>
</p>

5. Each dashboard is a class and each plot is a function: The classes are the
followings

<p align="center">
  <img src="img/lco_meteorology_classes.png" alt="Classes"/>
</p>

## Getting Started

First you will need to create a python virtual enviroment and then install 
the requirements.txt to finally start the project in your local machine

### Prerequisites

The main libraries of this project are:
- django_plotly_dash
- dash
- plotly

 ``` bash
# First create virtual enviroment
$ python -m venv venv

# Second activate the virtual enviroment (Windows 10)
$ .\venv\Scripts\activate

# Install the requirements in the virtual enviroment
$ python install -r requirements.txt
```

### Installing

After you have all the libraries installed you can start the project in your 
local machine.

``` bash
# First go to the django project folder
cd .\meteorologyProject

# Second start the local server
python manage.py runserver
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used.
* [django_plotly_dash](https://django-plotly-dash.readthedocs.io/en/latest/) - 
Plotly Dash applications served up in Django templates using tags.
* [Dash](https://dash.plotly.com/) - Framework for build data apps.
* [Plotly](https://plotly.com/) - Used to generate the graphs.
* [lcodataclient]() - Module for obtaining the data in dataframes.
* [Pandas](https://pandas.pydata.org/) - Used to manipulate the dataframes.


## Author

* **Gabriel Carvajal Figueroa** - *Initial work* - [Github](https://github.com/gabrielcarvajalfigueroa)


## Acknowledgments

* Thank to Nicolas Gonzalez for developing the lcodataclient module.
