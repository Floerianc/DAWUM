import sys, requests
from gui import *

class Application(Ui_MainWindow):
    def __init__(self, Form) -> None:
        self.setupUi(Form)
        self.DAWUM_API_URL = 'https://api.dawum.de/'
        super().__init__()
        self.get_current_json()
    
    def get_current_json(self):
        global data
        rsp = requests.get(self.DAWUM_API_URL) # Sends a request to the API_URL
        data = rsp.json() # Converts it into a JSON
        self.most_recent_survey()
    
    def most_recent_survey(self):
        keys = list(data["Surveys"].keys())
        MRS = data["Surveys"][f"{keys[0]}"] # MRS (Most Recent Survey) is now the first key in the Surveys Section
        self.get_values(MRS)
    
    def get_values(self, MRS):
        date = MRS["Date"] # Gets date of first Survey
        surveyed_people = MRS["Surveyed_Persons"] # How many people contributed
        results = MRS["Results"] # Results of all Parties who were there
        parliament_ID = MRS["Parliament_ID"] # Parliament ID
        institude_ID = MRS["Institute_ID"] # usw...
        self.change_texts(results, date, surveyed_people, parliament_ID, institude_ID)

    def change_texts(self, results, date, surveyed_people, parliament, institute):
        parliament_name = data["Parliaments"][f"{parliament}"]["Name"]
        institute_name = data["Institutes"][f"{institute}"]["Name"]

        parties = []
        percentages = []
        abbreviations = []
        for key in results.keys(): # Gets the KEYS of the 'results' dict (1, 7...)
            parties.append(data["Parties"][f"{key}"]["Name"]) # Alternative für Deutschland... usw
            abbreviations.append(data["Parties"][f"{key}"]["Shortcut"]) # AfD, CDU/CSU...
            percentages.append(results[f"{key}"]) # 30%, 17%...
        
        party_labels = [self.Party1, self.Party2, self.Party3, self.Party4, self.Party5, self.Party6, self.Party7, self.Party8, self.Party9]
        for abb in range(len(abbreviations)):
            party_labels[abb].setText(f"{abbreviations[abb]}")

        self.Date.setText(f"Datum: {date}")
        self.Date_2.setText(f"Befragte Personen: {surveyed_people}")

        self.Parlament.setText(f"Parlament: {parliament_name}")
        self.Institut.setText(f"Institut: {institute_name}")
        self.change_stats(percentages)
    
    def change_stats(self, percentages):
        party_stats = [self.Party_stat1, self.Party_stat2, self.Party_stat3, self.Party_stat4, self.Party_stat5, self.Party_stat6, self.Party_stat7, self.Party_stat8, self.Party_stat9]
        for iteration in range(len(percentages)):
            party_stats[iteration].setGeometry(QtCore.QRect(440, int(100+(60*iteration)), int(percentages[iteration]*15), 31))
        self.change_percentages(percentages)
    
    def change_percentages(self, percentages):
        percentages_label = [self.Percentage, self.Percentage_2, self.Percentage_3, self.Percentage_4, self.Percentage_5, self.Percentage_6, self.Percentage_7, self.Percentage_8, self.Percentage_9]
        for iteration in range(len(percentages)):
            percentages_label[iteration].setText(f"{percentages[iteration]}%")

# DIESE GANZE PARTY STATS UND PARTY LABELS IN EINE LIST KLATSCHEN DANKE

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QMainWindow()
ui = Application(Form)
Form.show()
app.exec()