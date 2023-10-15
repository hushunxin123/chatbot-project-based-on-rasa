from typing import Text, List, Any, Dict

# from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk import Tracker, Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ConversationPaused, UserUtteranceReverted,Restarted,FollowupAction
import re


def clean_name(name):
    return "".join([c for c in name if c.isalpha()])

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"
    def validate_help_choice(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `help_choice` value."""
        # If the name is super short, it might be wrong.
        # name = slot_value
        # if len(name) == 0:
        #     dispatcher.utter_message(text="That must've been a typo.")
        #     return {"first_name": None}
        return {"help_choice": slot_value}



class ValidateCallnumberForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_callnumber_form"
    
    def validate_callnumber(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `call_number` value."""
        return {"call_number": slot_value}



class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""
    def name(self):
        return 'action_default_fallback'
    
    def run(self, dispatcher, tracker, domain):
        
        text = tracker.latest_message.get('text')
        # dispatcher.utter_template('utter_default', tracker, silent_fail=True)
        print(f"text = {text}")
        message = "Sorry, there is no matching information for this issue. Adjust the question and re-enter the keyword."
        
        dispatcher.utter_message(text=message)
        # message = ChatApis.get_response(text)
        # if message is not None:
        #     dispatcher.utter_message(message)
        # else:
        #     dispatcher.utter_template('utter_default', tracker, silent_fail=True)
        return [UserUtteranceReverted()]



class ActionHelpQuestion(Action):
    def name(self) -> Text:
        return "action_help_question"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play rock paper scissors
        # user_choice = tracker.get_slot("choice")
        help_choice = tracker.get_slot("help_choice")
        # print(f"action_help_question")

        print(f"help_choice = {help_choice}")

        if help_choice.isnumeric() == False:
            dispatcher.utter_message(text=f"please type the choise")

        if help_choice == "1":
            # dispatcher.utter_message(text=f"Ok, manual customer service: Suzy, we are on the line with you.")
            dispatcher.utter_message(response = "utter_human_support")

        if help_choice == "2":
            # dispatcher.utter_message(text=f"type the email to ")
            dispatcher.utter_message(response = "utter_end_email")

        if help_choice == "3":
            # dispatcher.utter_message(text=f"phone is: 177000203210")
            dispatcher.utter_message(text=f"type the 'senior executive' to question")
            
        return [Restarted()]



class ActionDefaultAskAffirmation(Action):
    def name(self) -> Text:
        return "action_default_ask_affirmation"
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict[Text, Any]
    ):
        #Chatbot asks the user to confirm by selecting one of the optinos
        message = "Sorry, there is no matching information for this issue. Adjust the question and re-enter the keyword."
        
        dispatcher.utter_message(text=message)
        return []



class ActionQuestion(Action):
    def name(self) -> Text:
        return "action_default_question"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play rock paper scissors
        # user_choice = tracker.get_slot("choice")
        user_choice = tracker.get_slot("choise")
        # if user_choice.isnumeric():
        if user_choice.isnumeric() == False:
            dispatcher.utter_message(text=f"please type the 1~4 choise")
            return []
        # dispatcher.utter_message(text=f"You chose {user_choice}")
        # comp_choice = self.computer_choice()
        # dispatcher.utter_message(text=f"The computer chose {comp_choice}")
        print(f"user_choice = {user_choice}")
        if user_choice == "1":
            # dispatcher.utter_message(text=f"Offline business hall information inquiry")
            dispatcher.utter_message(response = "utter_ask_question_1")

        if user_choice == "2":
            dispatcher.utter_message(response = "utter_ask_choice_2")

        if user_choice == "3":
            dispatcher.utter_message(response = "utter_ask_choice_3")
        
        if user_choice == "4":
            dispatcher.utter_message(text=f"please type the help to choice help")

        return [Restarted()]



class ValidatePhoneForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_phone_form"
    
    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phone_number` value."""
        phone = re.compile('^(13(7|8|9|6|5|4)|17(0|8|3|7)|18(2|3|6|7|9)|15(3|5|6|7|8|9))\d{8}$')
        if re.match(phone, slot_value):
            return {"phone_number": slot_value}
        else:
            dispatcher.utter_message(text="wrong input phone_number.")
            return {"phone_number": None}
    def validate_sim_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `sim_number` value."""
        phone = re.compile('^\d{5,10}$')
        if re.match(phone, slot_value):
            return {"sim_number": slot_value}
        else:
            dispatcher.utter_message(text="wrong input number.")
            return {"sim_number": None}

        

class ValidateQuestionForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_question_form"

    def validate_choise(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `choise` value."""
        # If the name is super short, it might be wrong.
        # name = clean_name(slot_value)
        print(f"slot_value choise = {slot_value}")

        if slot_value.isnumeric() == False:
            dispatcher.utter_message(text=f"That must've been a number please type the 1~4 choise")
            return {"choise": None}
    
        choise = int(slot_value)

        if choise <0 or choise>4:
            dispatcher.utter_message(text=f"That must've been a number please type the 1~4 choise")
            return {"choise": None}

        # name = slot_value
        # print("name====")
        print(f"slot_value choise = {choise}")

        if len(slot_value) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"choise": None}
        return {"choise": slot_value}
    
    
    
class ValidateHelpQuestionForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_help_form"

    def validate_choise(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `choise` value."""

        # If the name is super short, it might be wrong.
        # name = clean_name(slot_value)
        name = slot_value
        # print("name====")
        print(f"name = {name}")

        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"help": None}
        return {"help": name}