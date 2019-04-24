"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
from comprehend import Comp
import json,random

map = 'soundmap.json'
selfsentiment = 0
prev = None

with open(map) as json_file:
    soundboards = json.load(json_file)

intentmap = {
             "NEGATIVE"      :["fat","afteryou","finished","respect","outface"],
             "POSITIVE"      :["smartmf","hadsay","bigbrain"],
             "MIXED"         :["dontwantthat","fresh"],
             "NEUTRAL"       :["nottime","resources"],
             "fedup"         :["fat","afteryou","asking","stfu","rulesofengagement"],
             "greetingIntent":["whatsthematter","knockoff"],
             "foodIntent"    :["tastyburger","goodburger","hamburgers","kahunaburger","gourmet","ass"],
             "foodIntentN"   :["ass","trueromance"],
             "selfIntent"    :["superflytnt","mushroom","righteousman","evilman"],
             "endIntent"     :["partysover","endthis"],
             "songIntent"    :["song","song2","song3"],
             "storyIntent"   :["story"],
             "mfkersIntent"  :["fks"],
             "loveIntent"    :["love2","love3"],
             "jackIntent"    :["nasty"],
             "doyouIntent"   :["yesido","yesimake","yesidid"],
             "whoIntent"     :["vincent"],
             "fall"          :["english","englishinwhat"],
             "lostIntent"    :["youlost"],
             "AMAZON.YesIntent":["nodoubt","possible","correct"],
             "AMAZON.NoIntent" :["nodoubt","possible","correct"],
             }

def randomPick(intent):
    global prev
    global selfsentiment
    if selfsentiment < -20 and intent + 'N' in intentmap:
        intent = intent + 'N'
    sounds = intentmap[intent]
    rand = random.choice(sounds)
    if prev and len(sounds) != 1:
        while rand == prev:
            rand = random.choice(sounds)
    prev = rand
    return soundboards[rand]


# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_audio_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            "ssml": "<speak><audio src='" + output +"' /></speak>",
            "type": "SSML"
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - "
        },
        'reprompt': {
            'outputSpeech': {
                "ssml": "<speak><audio src='" + reprompt_text +"' /></speak>",
                "type": "SSML"
            }
        },
        'shouldEndSession': should_end_session
    }



def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_fall_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "fall"
    speech_output = randomPick("fall")
    reprompt_text = soundboards["howwedoinbaby"]
    should_end_session = False
    return build_response(session_attributes, build_audio_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_intent_response(intent_name):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "intent"
    speech_output = randomPick(intent_name)
    reprompt_text = soundboards["howwedoinbaby"]
    should_end_session = False
    return build_response(session_attributes, build_audio_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_you_response(intent_slot):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    session_attributes = {}
    card_title = "you"
    ut = intent_slot[0] + ' you ' + intent_slot[1]
    sen = Comp(ut).main()
    if sen != None:
        sentiment = sen['Sentiment']
        speech_output = randomPick(sentiment)
    else:
        speech_output = randomPick("fall")
    reprompt_text = soundboards["howwedoinbaby"]
    should_end_session = False
    return build_response(session_attributes, build_audio_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = soundboards["samuelljackson"]
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = soundboards["howwedoinbaby"]
    should_end_session = False
    return build_response(session_attributes, build_audio_response(
        card_title, speech_output, reprompt_text, should_end_session))



def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = randomPick("endIntent")
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_audio_response(
        card_title, speech_output, speech_output, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass



def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    intent_slot = ['','']
    try:
        slot = intent_request['intent']['slots']
        if "value" in slot['person']:
            intent_slot[0]=slot['person']['value']
        elif "value" in slot['target']:
            intent_slot[1] = slot['target']['value']
    except:
        pass
    # Dispatch to your skill's intent handlers

    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "youIntent":
        return get_you_response(intent_slot)
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fall_response()
    elif intent_name:
        return get_intent_response(intent_name)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

