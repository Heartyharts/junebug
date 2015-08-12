from klein import Klein
from twisted.web import http

from junebug.validate import body_schema, validate
from junebug.utils import json_body, response


class ApiUsageError(Exception):
    '''Exception that is raised whenever the API is used incorrectly.
    Used for incorrect requests and invalid data.'''


class JunebugApi(object):
    app = Klein()

    @app.handle_errors(ApiUsageError)
    def usage_error(self, request, failure):
        return response(request, 'api usage error', {
            'errors': [{
                'type': str(failure.type),
                'message': str(failure.value),
                }]
            }, code=http.BAD_REQUEST)

    @app.handle_errors(Exception)
    def generic_error(self, request, failure):
        return response(request, 'generic error', {
            'errors': [{
                'type': str(failure.type),
                'message': str(failure.value),
                }]
            }, code=http.SERVER_ERROR)

    @app.route('/channels', methods=['GET'])
    def get_channel_list(self, request):
        '''List all channels'''
        raise NotImplementedError()

    @app.route('/channels', methods=['POST'])
    @json_body
    @validate(
        body_schema({
            'type': 'object',
            'properties': {
                'type': {'type': 'string'},
                'label': {'type': 'string'},
                'config': {'type': 'object'},
                'metadata': {'type': 'object'},
                'status_url': {'type': 'string'},
                'mo_url': {'type': 'string'},
                'rate_limit_count': {
                    'type': 'integer',
                    'minimum': 0,
                },
                'rate_limit_window': {
                    'type': 'integer',
                    'minimum': 0,
                },
                'character_limit': {
                    'type': 'int',
                    'minimum': 0,
                },
            },
            'required': ['type', 'config', 'mo_url'],
        }))
    def create_channel(self, request, body):
        '''Create a channel'''
        raise NotImplementedError()

    @app.route('/channels/<string:channel_id>', methods=['GET'])
    def get_channel(self, request, channel_id):
        '''Return the channel configuration and a nested status object'''
        raise NotImplementedError()

    @app.route('/channels/<string:channel_id>', methods=['POST'])
    @json_body
    @validate(
        body_schema({
            'type': 'object',
            'properties': {
                'type': {'type': 'string'},
                'label': {'type': 'string'},
                'config': {'type': 'object'},
                'metadata': {'type': 'object'},
                'status_url': {'type': 'string'},
                'mo_url': {'type': 'string'},
                'rate_limit_count': {
                    'type': 'integer',
                    'minimum': 0,
                },
                'rate_limit_window': {
                    'type': 'integer',
                    'minimum': 0,
                },
                'character_limit': {
                    'type': 'int',
                    'minimum': 0,
                },
            },
        }))
    def modify_channel(self, request, channel_id):
        '''Mondify the channel configuration'''
        raise NotImplementedError()

    @app.route('/channels/<string:channel_id', methods=['DELETE'])
    def delete_channel(self, request, channel_id):
        '''Delete the channel'''
        raise NotImplementedError()

    @app.route('/channels/<string:channel_id>/messages', methods=['POST'])
    @json_body
    @validate(
        body_schema({
            'type': 'object',
            'properties': {
                'to': {'type': 'string'},
                'from': {'type': 'string'},
                'reply_to': {'type': 'string'},
                'event_url': {'type': 'string'},
                'priority': {'type': 'string'},
                'channel_data': {'type': 'object'},
            }
        }))
    def send_message(self, request, body, channel_id):
        '''Send an outbound (mobile terminated) message'''
        to_addr = body.get('to')
        reply_to = body.get('reply_to')
        if (to_addr and not reply_to) or (not to_addr and reply_to):
            raise ApiUsageError(
                'Only one of "from" and "reply_to" may be specified')

        raise NotImplementedError()

    @app.route(
        '/channels/<string:channel_id>/messages/<string:message_id>',
        methods=['GET'])
    def get_message_status(self, request, channel_id, message_id):
        '''Retrieve the status of a message'''
        raise NotImplementedError()