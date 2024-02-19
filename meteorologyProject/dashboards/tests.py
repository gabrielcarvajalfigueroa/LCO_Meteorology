from django.test import TestCase

from .Dash_Apps.dashboards_components import VaisalaDashBoard, MeteoBlueDashboard
from django.urls import reverse
from datetime import datetime

'''
This file contains testings for the classes VaisalaDashboard, MeteoBlueDashbord
and also tests the different views status codes.

If you want to write a test REMEMBER:
-------------------------------------
- You need to create a class for testing, were each method is a test

- Your class MUST receive the TestCase parameter in order for Django to recognize it
as a test.

- Your methods MUST start with test in order to be recognized as a test.

After your tests are done run:
$ python3 manage.py test dashboards
-------------------------------------
'''

# ---------------------------------------------------------
# TESTS FOR CLASSES VAISALADASHBOARD AND METEOBLUEDASHBOARD
# ---------------------------------------------------------

# python3 manage.py test dashboards.tests.VaisalaTestCase
class VaisalaTestCase(TestCase):
    """
    This class is for testing VaisalaDashboard class
    """

    def test_vaisala_generation_time(self):    

        print("-" * 40)
        print(" TESTING:    VAISALA GENERATION TIME ")
        print("-" * 40)

        start = datetime.now()

        dashboard = VaisalaDashBoard("Magellan")

        dashboard.generate_stations_plot()

        dashboard.generate_scattergl_plot()

        dashboard.generate_seeing_plot()

        # record loop end timestamp
        end = datetime.now()
        
        # find difference loop start and end time and display
        td = (end - start).total_seconds() * 10**3

        self.assertLessEqual(td, 1500, "\n Vaisala class takes more than 1.5 seconds to generate the plot")


# python3 manage.py test dashboards.tests.MeteoBlueTestCase
class MeteoBlueTestCase(TestCase):
    """
    This class is for testing MeteoBlueDashboard class
    """
    def test_meteoblue_generation_time(self):

        print("-" * 40)
        print(" TESTING:    METEOBLUE GENERATION TIME ")
        print("-" * 40)
        start = datetime.now()

        dashboard = MeteoBlueDashboard("4")

        dashboard.generate_dash()

        # record loop end timestamp
        end = datetime.now()
        
        # find difference loop start and end time and display
        td = (end - start).total_seconds() * 10**3

        self.assertLessEqual(td, 3000, "\n Meteoblue class takes more than 3 seconds to generate the plot")


# ---------------------------------------------------------
# ----------------- TESTS FOR VIEWS -----------------------
# ---------------------------------------------------------

class ViewsRenderingTestCase(TestCase):
    """
    This class uses reverse to check that all views return 200 status code.
    """

    def test_stations_view(self):
        print("-" * 40)
        print(" TESTING:    STATIONS VIEW STATUS CODE ")
        print("-" * 40)

        response = self.client.get(reverse("vaisala"))
        self.assertEqual(response.status_code, 200)

    def test_meteoblue_view(self):
        print("-" * 40)
        print(" TESTING:    METEOBLUE VIEW STATUS CODE ")
        print("-" * 40)

        response = self.client.get(reverse("meteoblue"))
        self.assertEqual(response.status_code, 200)

    def test_otherResources_view(self):
        print("-" * 40)
        print(" TESTING:    OTHER RESOURCES VIEW STATUS CODE ")
        print("-" * 40)

        response = self.client.get(reverse("otherResources"))
        self.assertEqual(response.status_code, 200)

    def test_webcams_view(self):
        print("-" * 40)
        print(" TESTING:    WEBCAMS VIEW STATUS CODE ")
        print("-" * 40)

        response = self.client.get(reverse("webcams"))
        self.assertEqual(response.status_code, 200)
    
    def test_history_view(self):
        print("-" * 40)
        print(" TESTING:    HISTORY VIEW STATUS CODE ")
        print("-" * 40)

        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 200)

    def test_allskycamera_view(self):
        print("-" * 40)
        print(" TESTING:    ALLSKYCAMERA VIEW STATUS CODE ")
        print("-" * 40)

        response = self.client.get(reverse("allskycamera"))
        self.assertEqual(response.status_code, 200)

    def test_nightlyskymovie_view(self):
        print("-" * 40)
        print(" TESTING:    NIGHTLYSKYMOVIE VIEW STATUS CODE ")
        print("-" * 40)

        response = self.client.get(reverse("nightlyskymovie"))
        self.assertEqual(response.status_code, 200)

