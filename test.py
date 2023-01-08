import openai

api_key = ''

def chatAI(request):
    response = openai.Completion.create(model="text-davinci-003", prompt=request, max_tokens=1024, api_key=api_key)
    print(response)
    answer = response.choices[0].text
    return answer

result = chatAI('Berechne mir die quadratwurzel von 3')
print(result)
