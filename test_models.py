import google.generativeai as genai

genai.configure(api_key="AIzaSyAh6YaZCnpVMFz1XFUHaAq4ysUCqakiljI")

for model in genai.list_models():
    print(model.name)
