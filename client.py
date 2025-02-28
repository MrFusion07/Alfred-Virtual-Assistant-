import google.generativeai as genai

genai.configure(api_key="IzaSyBLPngFF2yxOyEGDjHerEN")

model = genai.GenerativeModel("gemini-1.5-flash")  

response = model.generate_content("Explain how AI works")

print(response.text)
