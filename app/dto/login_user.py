from pydantic import BaseModel, Field, validator


class LoginUser(BaseModel):
    username: str = Field(..., min_length=4, max_length=15)
    password: str = Field(..., min_length=8, max_length=20)

    @validator('password')
    def password_strength(cls, value):
        if len(value) < 8 or len(value) > 20:
            raise ValueError('Password must be at least 8 characters long and less then 20 characters long')

        if not any(c.isupper() for c in value):
            raise ValueError('Password must contain at least one uppercase letter')

        if not any(c.islower() for c in value):
            raise ValueError('Password must contain at least one lowercase letter')

        if not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one digit')

        if not any(c in "!@#$%^&*()_+-=[]{};:'\"\\|,.<>/?`~" for c in value):
            raise ValueError('Password must contain at least one special character')

        return value