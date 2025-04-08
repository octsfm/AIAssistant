from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from functools import wraps

def admin_auth_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if not request.session.get("authenticated"):
            return RedirectResponse(url="/login")
        return await func(request, *args, **kwargs)
    return wrapper
