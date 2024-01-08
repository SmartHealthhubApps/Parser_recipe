import requests
from bs4 import BeautifulSoup
import json

headers = {"Accept": "*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

all_recipes_dict = dict()
json_data = list()
for page_number in range(1, 21):  # всего 3665 страниц
    print(f"Парсим {page_number} страницу для получения всех url рецептов")
    url = "https://eda.ru/recepty?page=" + str(page_number)
    req = requests.get(url, headers=headers)
    if req is None:
        continue
    else:
        req.encoding = "utf-8"
        src = req.text
        # print(src)

        with open("index.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open("index.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_recipes_current = soup.find_all(class_="emotion-18hxz5k")

        for item in all_recipes_current[1:]:
            item_text = item.text
            item_href = "https://eda.ru" + item.get("href")
            all_recipes_dict.update({item_text: item_href})

with open("all_recipes_dict.json", "w", encoding="utf-8") as file:
    json.dump(all_recipes_dict, file, indent=4, ensure_ascii=False)

with open("all_recipes_dict.json", encoding="utf-8") as file:
    all_recipes_urls = json.load(file)

recipe_number = 0
for recipe_name, recipe_href in all_recipes_urls.items():
    recipe_number += 1
    print(f"Парим рецепт: {recipe_number} из {len(all_recipes_urls)}")
    req = requests.get(recipe_href, headers=headers)
    req.encoding = "utf-8"
    if req is None:
        continue
    else:
        src = req.text

        with open(f"data/{recipe_name}.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f"data/{recipe_name}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        # ингредиенты и их кол-во
        ingredients_names = soup.find_all(itemprop="recipeIngredient")
        quantities = soup.find_all(class_="emotion-bsdd3p")
        if (ingredients_names and quantities) is None:
            continue
        else:
            ingredients_dict = dict()
            for i in range(len(ingredients_names)):
                ingredients_dict[ingredients_names[i].text] = quantities[i].text
            # print(ingredients_dict)

        # инструкция приготовления
        cooking_process = soup.find_all(itemprop="text")
        if cooking_process is None:
            continue
        else:
            cooking_process_text = str()
            count = 1
            for paragraph in cooking_process:
                cooking_process_text += f"{count} {paragraph.text} "
                cooking_process_text = cooking_process_text.replace("\xa0", " ")
                count += 1
            # print(cooking_process_text)

            json_data.append({"Название рецепта": recipe_name, "Ссылка": recipe_href, "Ингредиенты": ingredients_dict,
                              "Инструкция приготовления": cooking_process_text})

with open("eda_ru_data.json", "w", encoding="utf-8") as file:
    json.dump(json_data, file, indent=4, ensure_ascii=False)

# with open("eda_ru_data.json", encoding="utf-8") as file:
#     data = json.load(file)
