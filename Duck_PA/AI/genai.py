import google.generativeai as genai
import os

auth_token = os.getenv("GEMINI_API_KEY")  # Get the authentication token from an environment variable
genai.configure(api_key=auth_token)
model = genai.GenerativeModel("gemini-1.5-flash")