from fastapi import FastAPI

from recipe_api.modules.areas.router import router as areas_router
from recipe_api.modules.categories.router import router as categories_router
from recipe_api.modules.ingredients.router import router as ingredients_router
from recipe_api.modules.recipe_ingredients.router import (
    router as recipe_ingredients_router,
)
from recipe_api.modules.recipes.router import router as recipes_router
from recipe_api.modules.steps.router import router as steps_router
from recipe_api.modules.units.router import router as units_router


app = FastAPI(
    title="Recipe API",
    description="API REST para la gestión de recetas",
    version="1.0.0",
)


for router in (
    areas_router,
    categories_router,
    units_router,
    ingredients_router,
    recipes_router,
    steps_router,
    recipe_ingredients_router,
):
    app.include_router(router, prefix="/api/v1")
