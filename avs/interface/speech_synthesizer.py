
import uuid
import os

class SpeechSynthesizer(object):
    STATES = {'PLAYING', 'FINISHED'}

    def __init__(self, alexa):
        self.alexa = alexa
        self.state = 'FINISHED'
        self.token = ''

    # {
    #     "directive": {
    #         "header": {
    #             "namespace": "SpeechSynthesizer",
    #             "name": "Speak",
    #             "messageId": "{{STRING}}",
    #             "dialogRequestId": "{{STRING}}"
    #         },
    #         "payload": {
    #             "url": "{{STRING}}",
    #             "format": "AUDIO_MPEG",
    #             "token": "{{STRING}}"
    #         }
    #     }
    # }

    # Content-Type: application/octet-stream
    # Content-ID: {{Audio Item CID}}

    # {{BINARY AUDIO ATTACHMENT}}
    def Speak(self, directive, attachment=None):
        self.token = directive['payload']['token']
        url = directive['payload']['url']
        if url.startswith('cid:'):
            os.system('mpv {}.mp3'.format(url[4:]))

    def SpeechStarted(self):
        event = {
            "event": {
                "header": {
                    "namespace": "SpeechSynthesizer",
                    "name": "SpeechStarted",
                    "messageId": uuid.uuid4().hex
                },
                "payload": {
                    "token": self.token
                }
            }
        }
        self.alexa.event_queue.put(event)


    def SpeechFinished(self):
        event = {
            "event": {
                "header": {
                    "namespace": "SpeechSynthesizer",
                    "name": "SpeechFinished",
                    "messageId": uuid.uuid4().hex
                },
                "payload": {
                    "token": self.token
                }
            }
        }
        self.alexa.event_queue.put(event)

    @property
    def context(self):
        return {
                    "header": {
                        "namespace": "SpeechSynthesizer",
                        "name": "SpeechState"
                    },
                    "payload": {
                        "token": self.token,
                        "offsetInMilliseconds": 0,
                        "playerActivity": self.state
                    }
                }