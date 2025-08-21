from fastapi import APIRouter, Request

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/create_session")
async def session_set(request: Request):
    request.session["my_session"] = "1234"
    return {"status": "session created"}



@router.get("/read_session")
async def session_info(request: Request):
    my_var = request.session.get("my_session")
    return {"session_value": my_var}



@router.get("/delete_session")
async def session_delete(request: Request):
    my_var = request.session.pop("my_session", None)
    return {"deleted": my_var}
