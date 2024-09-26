# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from datetime import datetime, timedelta

menu_data = {
    2: {"day": "LABOR DAY", "food": []},
    3: {"day": "ITALIAN DAY", "food": ["Fish Tenders", "Rice Salad", "Brownies", "Fresh Fruit"]},
    4: {"day": "ITALIAN DAY", "food": ["Pasta Rustica", "Garden Salad", "Fresh Fruit"]},
    5: {"day": "", "food": ["Quinoa Salad", "Tomato Cuc Salad", "Fresh Fruit"]},
    6: {"day": "", "food": ["Margherita Pizza", "Caesar Salad", "Fresh Fruit", "Carrot Cake"]},
    9: {"day": "ALL AMERICAN", "food": ["Pasta Carbonara", "Garden Salad", "Fresh Fruit", "Baguette"]},
    10: {"day": "ASIAN DAY", "food": ["Teriyaki Chicken", "Rice", "Rugelachs", "Fresh Fruit"]},
    11: {"day": "", "food": ["Turkey Sandwich", "Vegetable Soup", "Fruit Salad"]},
    12: {"day": "", "food": ["Shepherd's Pie", "Spinach Salad", "Fresh Fruit", "Baguette"]},
    13: {"day": "FRENCH DAY", "food": ["Ratatouille", "Couscous", "Fresh Fruit", "Ch. Chip Cookies"]},
    16: {"day": "ALL AMERICAN", "food": ["BBQ Chicken", "Potato Salad", "Fresh Fruit"]},
    17: {"day": "", "food": ["Beef Chili", "Brown Rice", "Carrots & Celery", "Fruit Pies"]},
    18: {"day": "", "food": ["Pepperoni Pizza", "Garden Salad", "Fresh Fruit"]},
    19: {"day": "", "food": ["Roast Chicken & Vegetables", "Fresh Fruit"]},
    20: {"day": "", "food": ["Tortellini Marinara", "Garden Salad", "Fresh Fruit", "Cowboy Cookies"]},
    23: {"day": "", "food": ["Chicken Tenders", "Rice with Corn", "Banana Cake", "Fresh Fruit"]},
    24: {"day": "ALL AMERICAN", "food": ["Meatloaf", "Mac & Cheese", "Fresh Fruit", "Banana Cake"]},
    25: {"day": "", "food": ["Chicken Noodle", "Cheese Toast", "Fruit Salad"]},
    26: {"day": "ITALIAN DAY", "food": ["Salmon Penne Pasta", "Garden Salad", "Fresh Fruit"]},
    27: {"day": "", "food": ["Vegetable Fried Rice", "Fresh Fruit", "Cheesecake"]},
    30: {"day": "MEXICAN DAY", "food": ["Chicken Fajitas", "Mexican Rice", "Fresh Fruit"]}
}

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "DO YOU WANT THE MENU! TELL ME TO YAY!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class LFSDMenuIntentHandler(AbstractRequestHandler):
    """Handler for LFSD Menu Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LFSDMenuIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Get today's date (day of the month)
        today = datetime.now() - timedelta(days=1)  # Adjust by subtracting one day
        today_day = today.day  # Get the day of the month

        menu_info = menu_data.get(today_day, None)  # Retrieve the menu for today

        if menu_info:
            day_info = menu_info["day"]
            food_menu = menu_info["food"]
            
            if day_info:
                speak_output = f"Today is {day_info}. "
            else:
                speak_output = "The menu is available today."

            if food_menu:
                speak_output += " The menu includes: " + ", ".join(food_menu) + "."
            else:
                speak_output += " Sorry, no food is available today."
        else:
            speak_output = "Sorry, no menu is available for today."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(LFSDMenuIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()