import json


def main(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    with open('users_ids.json') as json_file:
        sessionStorage = json.load(json_file)
    if event['session']['user_id'] not in sessionStorage:
        sessionStorage[event['session']['user_id']] = 0
    else:
        sessionStorage[event['session']['user_id']] += 1
    with open('users_ids.json', 'w+', encoding="UTF-8") as file:
        json.dump(sessionStorage, file, indent=2, ensure_ascii=False)
    response = {  # то что отправляем
        'session': event['session'],
        'version': event['version'],
        'response': {
            'end_session': False
        }
    }

    text = 'Hello! I\'ll repeat anything you say to me.'
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        text = event['request']['original_utterance'] + str(
            sessionStorage[event['session']['user_id']])
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
            'text': text,
            # Don't finish the session after this response.
            'end_session': 'false'
        },
    }
