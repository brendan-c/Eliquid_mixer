from models import Recipe, Flavour, User
from app_setup import db
from pprint import pprint
# from server import db

def insert_sample_recipe(recipe_name):

    testflav = Flavour(name="Strawberry", percentage=5)
    testflav2 = Flavour(name="Orange", percentage=2)

    test_recipe = Recipe(
        name = recipe_name,
        version = 3,
        batchvolume = 30,
        batchnic = 6,
        batchratio = 70,
        basenic = 60,
        baseratio = 50,
        flavours = [testflav, testflav2]
        )
    try:
        db.session.add(test_recipe)
        db.session.commit()
    except:
        print("Duplicate entry! Recipe already exists")


def insert_recipe(recipe):
    existing_recipe = recipe_by_name(recipe['name'])
    version = 0 
    if (existing_recipe):
        print("Recipe version:", existing_recipe.version)
        version = existing_recipe.version + 1
    
    recipe_model = Recipe(
        name = recipe['name'],
        version = version,
        batchvolume = int(recipe['batchvolume']),
        batchnic = recipe['batchnic'],
        batchratio = recipe['batchratio'],
        basenic = recipe['basenic'],
        baseratio = recipe['baseratio'],
        flavours = [Flavour(name=x['label'], percentage=x['percentage']) for x in recipe["flavours"]]
    )

    if existing_recipe is not None:
        print("Existing recipe")
        pprint(existing_recipe.as_dict())

        print("New recipe")
        pprint(recipe_model.as_dict())

        print("models are the same:", recipe_model == existing_recipe)

        if recipe_model == existing_recipe:
            print("No difference between recipes - skipping insertion")
            return
    try:
        db.session.add(recipe_model)
        db.session.commit()
    except Exception as ex:
        print(ex)

def list_recipes():
    query = db.session.query(Recipe.name).distinct()
    names = [x for x in query]
    return names

def recipe_by_name(name):
    subquery = db.session.query(db.func.max(Recipe.version)).filter(Recipe.name == name)
    query = db.session.query(Recipe).filter(Recipe.name == name, Recipe.version == subquery)
    try:
        return query.one()
    except Exception as ex:
        print(ex)
        return None

def recipe_by_id(recipe_id):
    subquery = db.session.query(func.max(Recipe.version)).filter(Recipe.id == recipe_id)
    query = db.session.query(Recipe).filter(Recipe.id == recipe_id, Recipe.version == subquery)
    try:
        return query.one()
    except Exception as ex:
        print(ex)
        return None

def dictify_recipe(recipe):
    result = recipe.as_dict()
    result["flavours"] = [x.as_dict() for x in recipe.flavours]
    result["numflavours"] = len(recipe.flavours)
    return result

def recipe_is_same(json_recipe, recent_recipe):
    flavours = [Flavour(name=x['label'], percentage=x['percentage']) for x in json_recipe["flavours"]]
    print(flavours)
    print(recent_recipe.flavours)
    return (recent_recipe.name == json_recipe['name'] and
        recent_recipe.batchvolume == json_recipe['batchvolume'] and
        recent_recipe.batchnic == json_recipe['batchnic'] and
        recent_recipe.batchratio == json_recipe['batchratio'] and
        recent_recipe.basenic == json_recipe['basenic'] and
        recent_recipe.baseratio == json_recipe['baseratio'])
        # recent_recipe.baseratio == json_recipe['baseratio'] and
        # recent_recipe.flavours == flavours)

if __name__=="__main__":
    Base.metadata.create_all(engine)

    recipe_name = "Recipe 1"

    insert_sample_recipe(recipe_name)
    list_recipes()
    recipe = recipe_by_name(recipe_name)
    # print(recipe.as_dict())
    # print([x.as_dict() for x in recipe.flavours])
    print(dictify_recipe(recipe))