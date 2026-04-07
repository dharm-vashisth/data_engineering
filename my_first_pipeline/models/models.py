from pydantic import BaseModel, Field,field_validator
from typing import Optional

# Data Contract
class UserData(BaseModel):
    user_id:int
    username:str
    email:str
    age:Optional[int] = None

    # validation for business logic
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls,value):
        if value<=0:
            raise ValueError(f"User id must be a valid positive number. Got {value}")
        return value
    

if __name__ == "__main__":
    def get_bulk_data():
        return [
            # good data
            {'user_id': 1,'username': 'Dharm Vashisth','email': 'data.dharm.2021@gmail.com','age': 27},
            # field validation failure
            {'user_id': -32,'username': 'Alice','email': 'alice@gmail.com'},
            # pydantic will handle the user id itself using type casting.
            {'user_id': '12','username': 'Ronny','email': 'ronny@gmail.com'},
             # pydantic will handle the user id itself using type casting and field validation failure
            {'user_id': '-12','username': 'Rocky','email': 'rocky@gmail.com'},
        ]
    
    for data in get_bulk_data():
        # validate data
        try:
            user1 = UserData(**data)
            print(f"✅ Validation successful for the data {user1.username}\n")
        except Exception as e:
            print(f"❌ Data validation failed for {data['username']}: {e.json()}\n")



    