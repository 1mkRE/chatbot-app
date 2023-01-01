import openai

api_key = ''

def chatAI(request):
    response = openai.Completion.create(model="text-davinci-003", prompt=request, max_tokens=1024, api_key=api_key)
    answer = response.choices[0].text
    return answer

result = chatAI('Hauptstadt von Bosnien')
print(result)
