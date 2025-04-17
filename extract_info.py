#!/usr/bin/env python

from ollama import chat
from pydantic import BaseModel
from typing import List

class AboutMe(BaseModel):
	name: str
	job: str
	likes: List[str]

notes = """
Hello my name is Adam, I am a data scientist and like dogs.
"""

response = chat(model='granite3.2', messages= [
{
	'role': 'user',
	'content': f"Extract key values from the following text: {notes}",
},
], format=AboutMe.model_json_schema())
print(response['message']['content'])
