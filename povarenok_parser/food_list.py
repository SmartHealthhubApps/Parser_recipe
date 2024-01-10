from Backend.PovarenokParser.food_list import RecipePage, MainPage
from mongodb.mongo import MongoDB
from img_generator import Text2ImageAPI
import base64
import re


def generate_img(name: str, ingr: list) -> bytes:
    prompt = f"4k, hires, cinematic, Блюдо: '{name}' суперреализм на тарелке крупным планом. " \
             f"Ингредиенты: '{','.join(ingr)}'"
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)
    return base64.b64decode(images[0])


CATEGORIES = {'https://www.povarenok.ru/recipes/category/2/': 6826,
              'https://www.povarenok.ru/recipes/category/6/': 43076,
              'https://www.povarenok.ru/recipes/category/12/': 17644,
              'https://www.povarenok.ru/recipes/category/15/': 16171,
              'https://www.povarenok.ru/recipes/category/19/': 2920,
              'https://www.povarenok.ru/recipes/category/23/': 1663,
              'https://www.povarenok.ru/recipes/category/25/': 33268,
              'https://www.povarenok.ru/recipes/category/30/': 22822,
              'https://www.povarenok.ru/recipes/category/35/': 4141,
              'https://www.povarenok.ru/recipes/category/228/': 828,
              'https://www.povarenok.ru/recipes/category/227/': 220,
              'https://www.povarenok.ru/recipes/category/55/': 893,
              'https://www.povarenok.ru/recipes/category/187/': 634,
              'https://www.povarenok.ru/recipes/category/247/': 362,
              'https://www.povarenok.ru/recipes/category/289/': 331,
              'https://www.povarenok.ru/recipes/category/308/': 2320,
              'https://www.povarenok.ru/recipes/category/356/': 98
              }

if __name__ == '__main__':
    db = MongoDB().connect('recipe', 'recipe_dataset')
    for category in CATEGORIES:
        try:
            count = CATEGORIES[category] // 15
            url_list = MainPage(category).get_recipe_list(count=1)

            api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '821F382F8DACDA85D5CDC743ACDFC160',
                                'F35782A854ABBC9EDBE3CAC74E3B7261')
            path = 'img'
            model_id = api.get_model()

            for url in url_list:
                recipe = RecipePage(url)
                post = recipe.get_mongo_dict()
                name, url, ingr = recipe.name, recipe.url, recipe.ingredients.keys()
                url = re.search(r'\d+', url)[0]
                with open(f"{path}/{url}.png", mode='wb') as img:
                    img.write(generate_img(name, ingr))

                db.insert_one(post)
        except Exception as msg:
            print(msg)
