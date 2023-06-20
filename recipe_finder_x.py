import requests

def recipe():
    ingredient = input('Enter an ingredient you would like to search for?')
    print('\nSearching for {}'.format(ingredient))

    r = requests.get(
        f'https://api.edamam.com/search?q={ingredient}&app_id=de009ce8&app_key=28adfc61863241290820dd088579959e')

    response = r.json()

    # first_recipe = response['hits'][0]['recipe']

    # print(first_recipe['label'])
    # print(first_recipe['url'])

    if len(response['hits']) == 0:
        return -1

    API_response = response['hits']
    results = []
    length = len(API_response)
    for number in range(length):
        # print(response['hits'][number]['recipe'])
        recipe_data = response['hits'][number]['recipe']
        results.append((recipe_data["label"], recipe_data["calories"], recipe_data["healthLabels"]))
    return results

# rr = recipe()

while True:
    rr = recipe()
    if rr == -1:
        print('Nothing found. Do again.')
        continue

    else:
        break

for rec in rr:
    print(rec)

# with open('recipe.txt', 'w+') as text_file:
#     results = str(rr)
#     text_file.write(results)
