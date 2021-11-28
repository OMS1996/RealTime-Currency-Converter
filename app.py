import requests
import json
import questionary
import pandas as pd
import sys
import fire
import emoji # library el gdeeda.

url_data = "https://api.exchangerate-api.com/v4/latest/USD"

class JoeCurrencyConverter:
    def __init__(self, url = url_data):
        "These has all the attributes of the class"
        self.url = url_data
        self.data = self.getData()
        self.rate = self.data['rates']

    def welcomeFunction(self):
        heart = emoji.emojize(":red_heart: :red_heart: :red_heart:",variant="emoji_type")
        questionary.print("Hello, welcome to Joe's Currency Converter", style="bold italic fg:darkred")
        questionary.print(heart)

    def chooseAction(self):
        action = questionary.rawselect(
            "What do you want to do? , \n Please click on the number you would like to choose from your keyboard.",
            ["Convert currencies.",
             "Show top 10 highest currencies.",
             "Show top 10 lowest currencies.",
             "Quit the program."
            ]).ask()
        return action

    def getData(self):
        """
        To get the data using the exchangerate api
        """
        return requests.get(self.url).json()

    def showData(self, data):
        """
        To show the data
        """
        # Display the response data
        print(json.dumps(data, indent=4, sort_keys=True))

    def getDomesticCurrency(self):
        """ Gets input from user about the domestic currency country"""
        choice = questionary.select(
            "Which Domestic would you like to change from ? ",
             list(self.rate.keys())
        ).ask()
        questionary.print("You chose " + str(choice) + " as your Domestic Currency")
        return choice

    def getValueOfDomesticCurrency(self):
        """ To get the amount that needs to be changed """
        i = 1
        while (type(i) != float):
            i = questionary.text("Enter the Value needed to be changed .... ").ask()
            try:
                i = float(i)
                if type(i) == float:
                    break
            except:
                print("Please enter a valid amount (numbers).... Thank you.")
        print("value entered is ")
        print(i)
        return i

    def getForeignCurrency(self):
        """ Gets input from user about the foreign currency country"""
        choice = questionary.select(
            "Which Foreign currency would you like to ? ",
             list(self.rate.keys())
        ).ask()
        questionary.print("You chose " + str(choice) + " as your Foreign Currency")
        return choice

    def convert_currency(self, amount, domestic, foreign):
        """How to convert from domestic to foreign"""
        final_val = amount * foreign / domestic
        questionary.print(str(final_val))
        return final_val

    def get_df(self):
        "Creates a dataframe from the acquired"
        df = pd.DataFrame.from_dict(self.data)
        df['country_ticker'] = df.index
        df_rates = df[['country_ticker', 'rates']]
        return df_rates

    def show_top_highest_10(self, df_rates):
        highest = df_rates.sort_values(by= "rates").iloc[0:10,:]
        print(highest)
        return highest

    def show_top_lowest_10(self, df_rates):
        lowest = df_rates.sort_values(by="rates", ascending=False).iloc[0:10,:]
        print(lowest)
        return lowest


    def quit(self):
        sys.exit("Goodbye, hope to see you again!")

def run():

    program = JoeCurrencyConverter()
    program.welcomeFunction()
    action = program.chooseAction()
    df_rates = program.get_df()

    if action == "Convert currencies.":

        # current domestic currency
        domestic_currency = program.getDomesticCurrency()

        # value flooos, money.
        val_domestic_currency = program.getValueOfDomesticCurrency()

        # foreign currency country.
        foreign_currency = program.getForeignCurrency()

        # rates for dom, for.
        dom = program.rate[domestic_currency]
        foreign = program.rate[foreign_currency]

        # calculating and printing to the screen.

        program.convert_currency(val_domestic_currency, dom, foreign)
        print(" Thank you very much for using Joe's Currency converter!!!! ")
    elif action == "Show top 10 highest currencies.":
        # show the highest rates
        program.show_top_highest_10(df_rates)
        print(" Thank you very much for using !!!! ")
    elif action == "Show top 10 lowest currencies.":
        # show the lowest rates.
        program.show_top_lowest_10(df_rates)
        print(" Thank you very much for using Joe's Currency Converter !!!! ")
    else:
        # quit the whole program
        program.quit()

if __name__ == "__main__":
    fire.Fire(run)
