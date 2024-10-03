# # # This files contains your custom actions which can be used to run
# # # custom Python code.
# # #
# # # See this guide on how to implement these action:
# # # https://rasa.com/docs/rasa/custom-actions

# import json
# from typing import Any, Dict, List, Text
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet

# class ActionListCourses(Action):

#     def name(self) -> Text:
#         return "action_list_courses"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Load the data from the JSON file
#         with open('RMIT_CourseData.json') as f:
#             data = json.load(f)

#         # Get the user intent
#         user_intent = tracker.latest_message['intent'].get('name')

#         # Initialize a response message
#         response = ""

#         # Handle the request for Master's programs
#         if user_intent == "request_master_programs":
#             response = "Please specify an area of interest (e.g., Engineering / Information Technology)."
#             return [SlotSet("awaiting_area_of_interest", True)]  # Set a slot to track this state

#         # Check if the user specified an area of interest
#         area_of_interest = tracker.get_slot("area_of_interest")

#         if area_of_interest:
#             # Filter courses based on the specified area of interest
#             courses = [course for course in data if course['Interest Area'].lower() == area_of_interest.lower()]
#             if courses:
#                 response = f"Here are the courses we offer in {area_of_interest}:\n"
#                 for course in courses:
#                     response += f"* **{course['Program Name']}**: Location: {course['Location']} (University: {course['University']})\n"
#             else:
#                 response = f"Sorry, no courses available in {area_of_interest}."

#         else:
#             # Default: List all courses if no specific intent matched
#             response = "Here are all the courses we offer:\n"
#             for course in data:
#                 response += f"* **{course['Program Name']}**: Location: {course['Location']} (University: {course['University']})\n"

#         dispatcher.utter_message(text=response)
#         return []

import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionListCourses(Action):

    def name(self) -> Text:
        return "action_list_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load the data from the JSON file
        try:
            with open('RMIT_CourseData.json') as f:
                data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="Course data file not found.")
            return []
        except json.JSONDecodeError:
            dispatcher.utter_message(text="Error reading course data.")
            return []

        # Get the user intent
        user_intent = tracker.latest_message['intent'].get('name')

        # Initialize a response message
        response = ""

        # Handle the request for Master's programs
        if user_intent == "request_master_programs":
            response = "Please specify an area of interest (e.g., Engineering / Information Technology)."
            return [SlotSet("awaiting_area_of_interest", True)]  # Set a slot to track this state

        # Check if the user specified an area of interest
        area_of_interest = tracker.get_slot("area_of_interest")

        if area_of_interest:
            # Filter courses based on the specified area of interest
            courses = [course for course in data if course['Interest Area'].lower() == area_of_interest.lower()]
            if courses:
                response = f"Here are the courses we offer in {area_of_interest}:\n"
                for course in courses:
                    response += f"* **{course['Program Name']}**: Location: {course['Location']} (University: {course['University']})\n"
            else:
                response = f"Sorry, no courses available in {area_of_interest}."

        else:
            # Default: List all courses if no specific intent matched
            response = "Here are all the courses we offer:\n"
            for course in data:
                response += f"* **{course['Program Name']}**: Location: {course['Location']} (University: {course['University']})\n"

        dispatcher.utter_message(text=response)
        return []
