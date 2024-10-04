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
import os
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
            file_path = os.path.join(os.path.dirname(__file__), 'RMIT_CourseData.json')
            with open(file_path) as f:
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

                response += f"\nDo you have any specific program in mind from the {area_of_interest} field?"
            else:
                response = f"Sorry, no courses available in {area_of_interest}."

        else:
            # Default: List all courses if no specific intent matched
            response = "Here are all the courses we offer:\n"
            for course in data:
                response += f"* **{course['Program Name']}**: Location: {course['Location']} (University: {course['University']})\n"
        dispatcher.utter_message(text=response)
        return []

# New action to get university names based on program name
class ActionGetUniversities(Action):

    def name(self) -> Text:
        return "action_get_universities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load the data from the JSON file
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'RMIT_CourseData.json')
            with open(file_path) as f:
                data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="Course data file not found.")
            return []
        except json.JSONDecodeError:
            dispatcher.utter_message(text="Error reading course data.")
            return []

        # Get the program name from the user's input
        program_name = tracker.latest_message['text']

        # Filter courses based on the specified program name
        matching_courses = [course for course in data if course['Program Name'].lower() == program_name.lower()]

        if matching_courses:
            universities = {course['University'] for course in matching_courses}  # Get unique universities
            university_list = "\n".join([f"- {uni}" for uni in universities])
            response = f"The following universities offer the {program_name} program:\n{university_list}"
            response += f"\nWould you like to check the course details at the selected university? Please select one university from above list"
        else:
            response = f"Sorry, no universities found for the program '{program_name}'."

        dispatcher.utter_message(text=response)
        return []

class ActionGetCourseDetails(Action):
    def name(self) -> Text:
        return "action_get_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the program name from the slot
        program_name = tracker.get_slot('program_name')
        university_name = tracker.get_slot('university_name')
        
        if not program_name:
            dispatcher.utter_message(text="I couldn't find a valid program name.")
            return []

        # Load course data from the JSON file
        file_path = os.path.join(os.path.dirname(__file__), 'Courses.json')  # Update to correct path
        with open(file_path, 'r') as file:
            courses = json.load(file)

        # Search for the course details based on the program name
        course_details = next((course for course in courses 
                       if course["Program Name"] == program_name and 
                          course["University"].lower() == university_name.lower()), 
                       None)

        if course_details:
            # Format the response
            response = (
                f"**Program Name:** {course_details['Program Name']}\n"
                f"**University:** {course_details['University']}\n"
                f"**Location:** {course_details['Location']}\n"
                f"**Program Duration:** {course_details['Program Duration Years']} years\n"
                f"**International Tuition Fee:** ${course_details['International Tuition Fee']}\n"
                f"**Average Credit Points Per Year:** {course_details['Average Credit Points Per Year']}\n"
            )
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any details for that program.")

        return []

# import json
# import os
# from typing import Any, Text, Dict, List
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
#         try:
#             file_path = os.path.join(os.path.dirname(__file__), 'RMIT_CourseData.json')
#             with open(file_path) as f:
#                 data = json.load(f)
#         except FileNotFoundError:
#             dispatcher.utter_message(text="Course data file not found.")
#             return []
#         except json.JSONDecodeError:
#             dispatcher.utter_message(text="Error reading course data.")
#             return []

#         # Get the area of interest from the slot
#         area_of_interest = tracker.get_slot("area_of_interest")

#         if area_of_interest:
#             # Filter the courses based on the area of interest
#             courses = [course for course in data if course['Interest Area'].lower() == area_of_interest.lower()]
#             if courses:
#                 response = f"Here are the programs we offer in {area_of_interest}:\n"
#                 for course in courses:
#                     response += f"- {course['Program Name']}\n"
#             else:
#                 response = f"Sorry, no programs available in {area_of_interest}."
#         else:
#             response = "Please specify an area of interest."

#         dispatcher.utter_message(text=response)

#         # After listing courses, ask if the user has a specific program in mind
#         dispatcher.utter_message(text=f"Do you have any specific program in mind from the {area_of_interest} field?")
        
#         return [SlotSet("awaiting_area_of_interest", False)]  # Reset the awaiting slot

# class ActionGetUniversities(Action):
#     def name(self) -> Text:
#         return "action_get_universities"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         program_name = tracker.get_slot('program_name')
#         print(program_name)
#         # Check if the program_name is present and normalize it
#         if program_name:
#             program_name = program_name.strip().lower()  # Convert to lowercase and remove any extra spaces

#             # Load course data from JSON file
#             try:
#                 file_path = os.path.join(os.path.dirname(__file__), 'RMIT_CourseData.json')
#                 with open(file_path) as f:
#                     data = json.load(f)
#             except FileNotFoundError:
#                 dispatcher.utter_message(text="Course data file not found.")
#                 return []
#             except json.JSONDecodeError:
#                 dispatcher.utter_message(text="Error reading course data.")
#                 return []

#             # Search for the program in the data
#             matched_courses = [course for course in data if course['Program Name'].strip().lower() == program_name]

#             if matched_courses:
#                 # List the universities offering the program
#                 universities = set(course['University'] for course in matched_courses)
#                 response = f"The following universities offer the {program_name.title()} program:\n"
#                 response += "\n".join(f"- {university}" for university in universities)
#             else:
#                 response = f"Sorry, no universities found for the program '{program_name.title()}'."
#         else:
#             response = "Please specify a valid program."

#         dispatcher.utter_message(text=response)
#         return []
