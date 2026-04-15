from pydantic import BaseModel, Field,field_validator, EmailStr, ValidationError
from typing import Optional
import os
from utils import get_logging_loader
from constants import (
    root, 
    log_directory_name
)


# custom logger
log_file = os.path.join(root,log_directory_name,"validation_failed.log")
validation_logger = get_logging_loader("validation_logger",log_file)

# Data Contract
class UserData(BaseModel):
    user_id:int
    username:str
    email:EmailStr # auto validation for email type string using pydantic.
    age:Optional[int] = None

    # validation for business logic
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls,value):
        if value<=0:
            validation_logger.error(f"User id must be a valid positive number. Got {value}")
        return value
    
    @field_validator('age')
    @classmethod
    def validate_age(cls,value):
        if value<1 or value > 120:
            validation_logger.error(f"Age must be valid in the range from 1-120. Got {value}")
        return value
    

if __name__ == "__main__":
    def get_bulk_data():
        return [
            # good data
            {'user_id': 1,'username': 'Dharm Vashisth','email': 'data.dharm.2021@gmail.com','age': 27},
            # bad data: user id field validation failure
            {'user_id': -32,'username': 'Alice','email': 'alice@gmail.com'},
            # good data: pydantic will handle the user id itself using type casting.
            {'user_id': '12','username': 'Ronny','email': 'ronny@gmail.com'},
             # bad data: pydantic will handle the user id itself using type casting and field validation failure
            {'user_id': '-12','username': 'Rocky','email': 'rocky@gmail.com'},
            # bad data: age field validation failure
            {'user_id': 22,'username': 'Alice D','email': 'alice.d@gmail.com', 'age':121},
            # bad data: email field validation failure using pydantic emailstr type
            {'user_id': 12,'username': 'Don D','email': 'don.d@gmailcom'},
        ]
    
    for data in get_bulk_data():
        # validate data
        try:
            user = UserData(**data)
            print(f"✅ Validation successful for the data {user.username}\n")
        except ValidationError as e:
            print(f"❌ Data validation failed for {data['username']}: {e.json()}\n")



    