utils/error_handling.py

from flask import jsonify

def handle_error(error):
    response = jsonify({'message': str(error)})
    response.status_code = error.status_code
    return response

def handle_not_found_error(error):
    response = jsonify({'message': 'Not found'})
    response.status_code = 404
    return response

def handle_bad_request_error(error):
    response = jsonify({'message': 'Bad request'})
    response.status_code = 400
    return response

def handle_unauthorized_error(error):
    response = jsonify({'message': 'Unauthorized'})
    response.status_code = 401
    return response

def handle_forbidden_error(error):
    response = jsonify({'message': 'Forbidden'})
    response.status_code = 403
    return response

def handle_conflict_error(error):
    response = jsonify({'message': 'Conflict'})
    response.status_code = 409
    return response

def handle_internal_server_error(error):
    response = jsonify({'message': 'Internal server error'})
    response.status_code = 500
    return response
