import sys, requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from gui import *

#########################################################
#              --- BIG ASS DISCLAIMER ---               #
#   THIS PROGRAM IS ONLY CAPABLE OF SHOWING 9 PARTIES   #
#             AT THE SAME TIME CUZ IM LAZY              #
#########################################################

class Application(Ui_MainWindow):
    def __init__(self, Form) -> None:
        self.setupUi(Form)
        self.DAWUM_API_URL = 'https://api.dawum.de/'
        super().__init__()
        self.get_current_json()

        self.actionSend_in_Discord.triggered.connect(self.discord_webhook_send)
    
    def get_current_json(self):
        global data
        rsp = requests.get(self.DAWUM_API_URL) # Sends a request to the API_URL
        self.data = rsp.json() # Converts it into a JSON
        self.most_recent_survey()
    
    def most_recent_survey(self):
        global MRS
        keys = list(self.data["Surveys"].keys())
        MRS = self.data["Surveys"][f"{keys[0]}"] # MRS (Most Recent Survey) is now the first key in the Surveys Section
        self.get_values(MRS)
    
    def get_values(self, MRS):

        self.date = MRS["Date"] # Gets date of first Survey
        self.surveyed_people = MRS["Surveyed_Persons"] # How many people contributed
        self.results = MRS["Results"] # Results of all Parties who were there
        self.parliament_ID = MRS["Parliament_ID"] # Parliament ID
        self.institude_ID = MRS["Institute_ID"] # usw...
        self.parliament_name = self.data["Parliaments"][f"{self.parliament_ID}"]["Name"]
        self.institute_name = self.data["Institutes"][f"{self.institude_ID}"]["Name"]

        self.parties = []
        self.percentages = []
        self.abbreviations = []
        for key in self.results.keys(): # Gets the KEYS of the 'results' dict (1, 7...)
            self.parties.append(self.data["Parties"][f"{key}"]["Name"]) # Alternative für Deutschland... usw
            self.abbreviations.append(self.data["Parties"][f"{key}"]["Shortcut"]) # AfD, CDU/CSU...
            self.percentages.append(self.results[f"{key}"]) # 30%, 17%...

        self.change_texts()

    def change_texts(self):
        party_labels = [self.Party1, self.Party2, self.Party3, self.Party4, self.Party5, self.Party6, self.Party7, self.Party8, self.Party9]
        for abb in range(len(party_labels)):
            try:
                party_labels[abb].setText(f"{self.abbreviations[abb]}")
            except:
                party_labels[abb].clear()

        self.Date.setText(f"Datum: {self.date}")
        self.Date_2.setText(f"Befragte Personen: {self.surveyed_people}")

        self.Parlament.setText(f"Parlament: {self.parliament_name}")
        self.Institut.setText(f"Institut: {self.institute_name}")
        self.change_stats()
    
    def change_stats(self):
        party_stats = [self.Party_stat1, self.Party_stat2, self.Party_stat3, self.Party_stat4, self.Party_stat5, self.Party_stat6, self.Party_stat7, self.Party_stat8, self.Party_stat9]
        for iteration in range(len(party_stats)):
            try:
                party_stats[iteration].setGeometry(QtCore.QRect(440, int(100+(60*iteration)), int(self.percentages[iteration]*15), 31)) # for each party it creates a nice blue 'bar'
            except:
                party_stats[iteration].setGeometry(QtCore.QRect(0,0,0,0)) # if it doesnt exist, just have a bar without any size or position
        self.change_percentages()
    
    def change_percentages(self):
        percentages_label = [self.Percentage, self.Percentage_2, self.Percentage_3, self.Percentage_4, self.Percentage_5, self.Percentage_6, self.Percentage_7, self.Percentage_8, self.Percentage_9]
        for iteration in range(len(percentages_label)):
            try:
                percentages_label[iteration].setText(f"{self.percentages[iteration]}%") # for each label that exists in the program, it tries to get the percentage to the corresponding party
            except:
                percentages_label[iteration].clear() # if there arent enough parties, just clear the label
    
    def discord_webhook_send(self):
        results = ""
        content = f"Datum: **{self.date}**\nAnzahl befragte Personen: **{self.surveyed_people}**\nParlament: **{self.parliament_name}**\nInstitut: **{self.institute_name}**\n# __Ergebnisse__\n"

        for i in range(len(self.abbreviations)):
            if i < 2:
                heading = "#"*(i+2) # a hashtag '#' in a discord message makes the font size bigger, so the top 2 parties have a bigger font than the rest.
            else:
                heading = "" # if the party is not in the top 2, the texts size will be normal
            
            results += f"\n{heading} **{i+1}.** *{self.abbreviations[i]}:* {self.percentages[i]}%"
        
        content = content + results # combines date, surveyed people, parliament, institute and the results into one big string
        
        webhook = DiscordWebhook(url="YOUR WEBHOOK URL") # sets up a Discord Webhook
        embed = DiscordEmbed(title="NEUESTE WAHLERGEBNISSE", description=content, color="ff0313") # creates a Discord Embed
        webhook.add_embed(embed)
        response = webhook.execute() # sends the message

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QMainWindow()
ui = Application(Form)
Form.show()
app.exec()