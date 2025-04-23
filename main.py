import time
from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()


@app.get("/status")
async def get_status():
    """
    Returns the status of the application.
    """
    return {"status": "ok", "ts": int(time.time())}


class EmailRequest(BaseModel):
    email: str

EMAIL_REGEX = re.compile(
    r"^(?![.-])([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

@app.post("/email-validate")
async def email_validate(req: EmailRequest):
    email = req.email
    valid = bool(EMAIL_REGEX.fullmatch(email))
    return {"valid": valid}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
