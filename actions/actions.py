# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions


# # This is a simple example for a custom action which utters "Hello World!"

# # from typing import Any, Text, Dict, List
# #
# # from rasa_sdk import Action, Tracker
# # from rasa_sdk.executor import CollectingDispatcher
# #
# #
# # class ActionHelloWorld(Action):
# #
# #     def name(self) -> Text:
# #         return "action_hello_world"
# #
# #     def run(self, dispatcher: CollectingDispatcher,
# #             tracker: Tracker,
# #             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
# #
# #         dispatcher.utter_message(text="Hello World!")
# #
# #         return []
# # actions/actions.py
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# class ActionProvideUniversityDetails(Action):

#     def name(self) -> Text:
#         return "action_provide_university_details"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         university = tracker.get_slot('university')  # Get the selected university

#         if university == "University of Melbourne":
#             details = (
#                 "### University of Melbourne\n"
#                 "**Course Fee:** AUD 50,000\n"
#                 "**Duration:** 2 years\n"
#                 "**Overview:** The Master of Data Science at the University of Melbourne prepares graduates to apply data science techniques to solve complex problems."
#             )
#         elif university == "Monash University":
#             details = (
#                 "### Monash University\n"
#                 "**Course Fee:** AUD 45,000\n"
#                 "**Duration:** 2 years\n"
#                 "**Overview:** The Master of Data Science program at Monash provides a robust foundation in data science principles."
#             )
#         elif university == "RMIT University":
#             details = (
#                 "### RMIT University\n"
#                 "**Course Fee:** AUD 48,000\n"
#                 "**Duration:** 2 years\n"
#                 "**Overview:** RMIT's Master of Data Science offers industry-focused learning and research opportunities."
#             )
#         else:
#             details = "I'm sorry, I don't have information for that university."

#         dispatcher.utter_message(text=details)

#         return []
