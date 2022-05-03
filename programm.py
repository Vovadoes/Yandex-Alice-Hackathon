sessionStorage = {}


def main(event, context):
    global sessionStorage

    text = 'Hello! I\'ll repeat anything you say to me.'
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        if event['session']['user_id'] not in sessionStorage:
            sessionStorage[event['session']['user_id']] = 0
        else:
            sessionStorage[event['session']['user_id']] += 1
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
