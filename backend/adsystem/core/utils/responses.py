from starlette.responses import JSONResponse


def make_error(description, status_code=400):
    return JSONResponse({
        'description': description
    }, status_code=status_code)
