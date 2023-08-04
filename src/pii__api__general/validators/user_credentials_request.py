from pydantic import BaseModel


class ApiUserInvite(BaseModel):
    credentials_request_token: str
    password: str


class ApiUserResetPasswordRequest(BaseModel):
    login: str


class ApiUserResetPassword(BaseModel):
    credentials_request_token: str
    new_password: str


class ApiUserChangePassword(BaseModel):
    credentials_request_token: str
    old_password: str
    new_password: str
