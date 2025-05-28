from django.shortcuts import render
from django.http import HttpResponseBadRequest

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def recipe_view(request, dish):
    servings = request.GET.get('servings', 1)
    try:
        servings = int(servings)
        if servings < 1:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Параметр servings должен быть положительным числом")

    # Получаем рецепт или пустой словарь, если такого блюда нет
    base_recipe = DATA.get(dish, {})

    # Масштабируем
    recipe = {
        ingredient: amount * servings
        for ingredient, amount in base_recipe.items()
    }

    context = {
        'recipe': recipe
    }

    return render(request, 'calculator/index.html', context)


    # можете добавить свои рецепты ;)


# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
