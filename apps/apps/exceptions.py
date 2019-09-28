from rest_framework.views import exception_handler

def core_exception_handler(exc, context):
    handlers = {
        'ValidationError': _handle_generic_error
    }

    response = exception_handler(exc, context)

    # Identify the type of the current exception and check 
    # if it should be handled here or by the default handler
    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response

def _handle_generic_error(exc, context, response):
    # Just wrap in errors key the response generated by DRF
    response.data = {
        'errors': response.data
    }
    
    return response