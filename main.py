from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#create the window for create-account window
class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    #if the email and password in correct format (with @ and have content in it), create an account, otherwise pop up window says incorrect
    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset() #reset the password and email input after logged in

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text): #validate with user's password and email in user.txt. Function is stored in database.py
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main" #if validates correctly, window changes to main (dashboard)
        else:
            invalidLogin() #pop up winodw says "invalid password or email"

    def createBtn(self): #if click on "don't have an account..." change the screen to create-account screen and reset the password and email
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class MainWindow(Screen):
    def spinnervalue(self, value): #change to different screens based on the chosen spinner value
        if value == 'Trend and stats':
            sm.current = "tands"
        elif value == 'Growth minitor':
            sm.current= 'gm'

    #connects with the refresh button.
    def humiditylevel(self):
        
        with open("/home/pi/Desktop/robotics/Robotics/Humidity_level.csv") as f:
            last_line1=f.readlines()[-1]
        
        txt1=last_line1.split(",")

        humiditylevel=txt1[1]

        self.ids.humidity_button.text=f'Humidity Level :\n{humiditylevel} % '

    def temperature(self):
        
        with open("/home/pi/Desktop/robotics/Robotics/Temperature_change.csv") as f:
            last_line2=f.readlines()[-1]
        
        txt2=last_line2.split(",")

        temperature=txt2[1]

        self.ids.temperature_button.text=f'Temperature:\n {temperature}°C '

    def soillevel(self):
        
        with open("/home/pi/Desktop/robotics/Robotics/Soil_moisture_level.csv") as f:
            last_line3=f.readlines()[-1]
        
        txt3=last_line3.split(",")

        soilmoisture=txt3[1]

        self.ids.soil_button.text=f'Soil Moisture\nLevel: {soilmoisture} '

class trendandstats(Screen):
    def spinnervalue1(self, value):
        if value == "Dashboard":
            sm.current = "main"
        elif value == 'Growth minitor':
            sm.current= 'gm'

    def graphvalue(self, value):
        if value=="Temperature graph":
            sm.current="temp"
        elif value=="Soil moisture graph":
            sm.current="smgraph"

class temperaturegraph(Screen):
    def spinnervalue2(self, value):
        if value == "Dashboard":
            sm.current = "main"
        elif value == 'Growth minitor':
            sm.current= 'gm'

    def graphvalue1(self, value):
        if value=="Humidity graph":
            sm.current="tands"
        elif value=="Soil moisture graph":
            sm.current="smgraph"

class soilmoisturegraph(Screen):
    def spinnervalue3(self, value):
        if value == "Dashboard":
            sm.current = "main"
        elif value == 'Growth minitor':
            sm.current= 'gm'

    def graphvalue2(self, value):
        if value=="Temperature graph":
            sm.current="temp"
        elif value=="Humidity graph":
            sm.current="tands"

class growthminitor(Screen):
    def spinnervalue4(self, value):
        if value == "Dashboard":
            sm.current = "main"
        elif value == 'Trend and stats':
            sm.current= 'tands'

class WindowManager(ScreenManager):
    pass

def invalidLogin(): #pop up window for invalid login
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(500, 500))
    pop.open()


def invalidForm(): #pop up window for invalid format of input
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs\n with valid information.'),
                  size_hint=(None, None), size=(600, 600))

    pop.open()

#read the csv files using pandas module
humidities = pd.read_csv("/home/pi/Desktop/robotics/Robotics/Humidity_level.csv", index_col=0, parse_dates=True)
temperatures = pd.read_csv("/home/pi/Desktop/robotics/Robotics/Temperature_change.csv", index_col=0, parse_dates=True)
soilmoistures = pd.read_csv("/home/pi/Desktop/robotics/Robotics/Soil_moisture_level.csv", index_col=0, parse_dates=True)

humidities['Humidity:']=pd.to_numeric(humidities['Humidity:'],errors='coerce')
temperatures['Temperature:']=pd.to_numeric(temperatures['Temperature:'],errors='coerce')
soilmoistures['Soil_moisture:']=pd.to_numeric(soilmoistures['Soil_moisture:'],errors='coerce')

#create line graphs from the previous step
graph1 = humidities.plot()
graph2 = temperatures.plot()
graph3 = soilmoistures.plot()

#save the line graphs as JPGs
fig1=graph1.get_figure()
fig2=graph2.get_figure()
fig3=graph3.get_figure()
fig1.savefig("/home/pi/Desktop/humidity.jpg")
fig2.savefig("/home/pi/Desktop/temperature.jpg")
fig3.savefig("/home/pi/Desktop/soilmoisture.jpg")

kv = Builder.load_file("plantminitor.kv") #runs the kv file

sm = WindowManager()
db = DataBase("users.txt") #define a variable for further calling

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"),trendandstats(name="tands"),temperaturegraph(name="temp"),soilmoisturegraph(name="smgraph"),growthminitor(name="gm")]
for screen in screens: #create a screen for each screen
    sm.add_widget(screen)

sm.current = "login"

class PlantMonitorApp(App): #define the app
    def build(self):
        return sm

if __name__ == "__main__": #run the app
    PlantMonitorApp().run()
    

