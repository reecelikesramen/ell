import instructor
from pydantic import BaseModel
from openai import OpenAI


# Define your desired output structure
class UserInfo(BaseModel):
    name: str
    profession: str
    age: int


# Patch the OpenAI client
client = instructor.from_openai(OpenAI())

# Extract structured data from natural language
user_info = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserInfo,
    messages=[{"role": "user", "content": [{"type": "text", "text": "John Doe is 30 years old."}, {"type": "text", "text": "John Doe's profession is software engineer."}]}],
)

print(user_info.name)
#> John Doe
print(user_info.age)
#> 30
print(user_info.profession)
#> software engineer