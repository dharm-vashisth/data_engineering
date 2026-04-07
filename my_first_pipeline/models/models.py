from pydantic import BaseModel, Field,field_validator
from typing import Optional

# Data Contract
class UserData(BaseModel):
    user_id:int
    username:str
    email:str
    age:Optional[int] = None

    # validation
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls,value):
        if value<=0:
            raise ValueError(f"User id must be a valid positive number. Got {value}")
        return value
    

if __name__ == "__main__":
    good_data = {
        'user_id': 1,
        'username': 'Dharm Vashisth',
        'email': 'data.dharm.2021@gmail.com',
        'age': 27
    }
    bad_data = {
        'user_id': -32,
        'username': 'Alice',
        'email': 'alice@gmail.com',
    }

    # validate data
    try:
        user1 = UserData(**good_data)
        print(f"Validation successful for the data {user1.username}")
        user2 = UserData(**bad_data)
        print(f"Validation successful for the data {user2.username}")
    
    except Exception as e:
        print(f"Data validation failed: {e}")



    