from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class AggregateRating:
    rating_count: Optional[int] = None
    type: Optional[str] = None
    rating_value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AggregateRating':
        assert isinstance(obj, dict)
        rating_count = from_union([from_none, lambda x: int(from_str(x))], obj.get("ratingCount"))
        type = from_union([from_str, from_none], obj.get("@type"))
        rating_value = from_union([from_str, from_none], obj.get("ratingValue"))
        return AggregateRating(rating_count, type, rating_value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.rating_count is not None:
            result["ratingCount"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.rating_count)
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.rating_value is not None:
            result["ratingValue"] = from_union([from_str, from_none], self.rating_value)
        return result


@dataclass
class Author:
    type: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Author':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("@type"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Author(type, name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class Image:
    type: Optional[str] = None
    url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("@type"))
        url = from_union([from_str, from_none], obj.get("url"))
        height = from_union([from_int, from_none], obj.get("height"))
        width = from_union([from_int, from_none], obj.get("width"))
        return Image(type, url, height, width)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        return result


@dataclass
class Item:
    id: Optional[str] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("@id"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Item(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["@id"] = from_union([from_str, from_none], self.id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        return result


@dataclass
class ItemListElement:
    type: Optional[str] = None
    position: Optional[int] = None
    item: Optional[Item] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ItemListElement':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("@type"))
        position = from_union([from_int, from_none], obj.get("position"))
        item = from_union([Item.from_dict, from_none], obj.get("item"))
        return ItemListElement(type, position, item)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.position is not None:
            result["position"] = from_union([from_int, from_none], self.position)
        if self.item is not None:
            result["item"] = from_union([lambda x: to_class(Item, x), from_none], self.item)
        return result


@dataclass
class Breadcrumb:
    type: Optional[str] = None
    item_list_element: Optional[List[ItemListElement]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Breadcrumb':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("@type"))
        item_list_element = from_union([lambda x: from_list(ItemListElement.from_dict, x), from_none], obj.get("itemListElement"))
        return Breadcrumb(type, item_list_element)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.item_list_element is not None:
            result["itemListElement"] = from_union([lambda x: from_list(lambda x: to_class(ItemListElement, x), x), from_none], self.item_list_element)
        return result


@dataclass
class MainEntityOfPage:
    type: Optional[List[str]] = None
    id: Optional[str] = None
    breadcrumb: Optional[Breadcrumb] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MainEntityOfPage':
        assert isinstance(obj, dict)
        type = from_union([lambda x: from_list(from_str, x), from_none], obj.get("@type"))
        id = from_union([from_str, from_none], obj.get("@id"))
        breadcrumb = from_union([Breadcrumb.from_dict, from_none], obj.get("breadcrumb"))
        return MainEntityOfPage(type, id, breadcrumb)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([lambda x: from_list(from_str, x), from_none], self.type)
        if self.id is not None:
            result["@id"] = from_union([from_str, from_none], self.id)
        if self.breadcrumb is not None:
            result["breadcrumb"] = from_union([lambda x: to_class(Breadcrumb, x), from_none], self.breadcrumb)
        return result


@dataclass
class Nutrition:
    type: Optional[str] = None
    calories: Optional[str] = None
    carbohydrate_content: Optional[str] = None
    cholesterol_content: Optional[str] = None
    fiber_content: Optional[str] = None
    protein_content: Optional[str] = None
    saturated_fat_content: Optional[str] = None
    sodium_content: Optional[str] = None
    sugar_content: Optional[str] = None
    fat_content: Optional[str] = None
    unsaturated_fat_content: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Nutrition':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("@type"))
        calories = from_union([from_str, from_none], obj.get("calories"))
        carbohydrate_content = from_union([from_str, from_none], obj.get("carbohydrateContent"))
        cholesterol_content = from_union([from_str, from_none], obj.get("cholesterolContent"))
        fiber_content = from_union([from_str, from_none], obj.get("fiberContent"))
        protein_content = from_union([from_str, from_none], obj.get("proteinContent"))
        saturated_fat_content = from_union([from_str, from_none], obj.get("saturatedFatContent"))
        sodium_content = from_union([from_str, from_none], obj.get("sodiumContent"))
        sugar_content = from_union([from_str, from_none], obj.get("sugarContent"))
        fat_content = from_union([from_str, from_none], obj.get("fatContent"))
        unsaturated_fat_content = from_union([from_str, from_none], obj.get("unsaturatedFatContent"))
        return Nutrition(type, calories, carbohydrate_content, cholesterol_content, fiber_content, protein_content, saturated_fat_content, sodium_content, sugar_content, fat_content, unsaturated_fat_content)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.calories is not None:
            result["calories"] = from_union([from_str, from_none], self.calories)
        if self.carbohydrate_content is not None:
            result["carbohydrateContent"] = from_union([from_str, from_none], self.carbohydrate_content)
        if self.cholesterol_content is not None:
            result["cholesterolContent"] = from_union([from_str, from_none], self.cholesterol_content)
        if self.fiber_content is not None:
            result["fiberContent"] = from_union([from_str, from_none], self.fiber_content)
        if self.protein_content is not None:
            result["proteinContent"] = from_union([from_str, from_none], self.protein_content)
        if self.saturated_fat_content is not None:
            result["saturatedFatContent"] = from_union([from_str, from_none], self.saturated_fat_content)
        if self.sodium_content is not None:
            result["sodiumContent"] = from_union([from_str, from_none], self.sodium_content)
        if self.sugar_content is not None:
            result["sugarContent"] = from_union([from_str, from_none], self.sugar_content)
        if self.fat_content is not None:
            result["fatContent"] = from_union([from_str, from_none], self.fat_content)
        if self.unsaturated_fat_content is not None:
            result["unsaturatedFatContent"] = from_union([from_str, from_none], self.unsaturated_fat_content)
        return result


@dataclass
class Publisher:
    type: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    logo: Optional[Image] = None
    brand: Optional[str] = None
    publishing_principles: Optional[str] = None
    same_as: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Publisher':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("@type"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        logo = from_union([Image.from_dict, from_none], obj.get("logo"))
        brand = from_union([from_str, from_none], obj.get("brand"))
        publishing_principles = from_union([from_str, from_none], obj.get("publishingPrinciples"))
        same_as = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sameAs"))
        return Publisher(type, name, url, logo, brand, publishing_principles, same_as)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        if self.logo is not None:
            result["logo"] = from_union([lambda x: to_class(Image, x), from_none], self.logo)
        if self.brand is not None:
            result["brand"] = from_union([from_str, from_none], self.brand)
        if self.publishing_principles is not None:
            result["publishingPrinciples"] = from_union([from_str, from_none], self.publishing_principles)
        if self.same_as is not None:
            result["sameAs"] = from_union([lambda x: from_list(from_str, x), from_none], self.same_as)
        return result


@dataclass
class RecipeInstruction:
    type: Optional[str] = None
    text: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'RecipeInstruction':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("@type"))
        text = from_union([from_str, from_none], obj.get("text"))
        return RecipeInstruction(type, text)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["@type"] = from_union([from_str, from_none], self.type)
        if self.text is not None:
            result["text"] = from_union([from_str, from_none], self.text)
        return result


@dataclass
class RecipeElement:
    context: Optional[str] = None
    type: Optional[List[str]] = None
    headline: Optional[str] = None
    date_published: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    author: Optional[List[Author]] = None
    description: Optional[str] = None
    image: Optional[Image] = None
    publisher: Optional[Publisher] = None
    name: Optional[str] = None
    aggregate_rating: Optional[AggregateRating] = None
    cook_time: Optional[str] = None
    nutrition: Optional[Nutrition] = None
    prep_time: Optional[str] = None
    recipe_category: Optional[List[str]] = None
    recipe_cuisine: Optional[List[str]] = None
    recipe_ingredient: Optional[List[str]] = None
    recipe_instructions: Optional[List[RecipeInstruction]] = None
    recipe_yield: Optional[List[int]] = None
    total_time: Optional[str] = None
    main_entity_of_page: Optional[MainEntityOfPage] = None
    about: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'RecipeElement':
        assert isinstance(obj, dict)
        context = from_union([from_str, from_none], obj.get("@context"))
        type = from_union([lambda x: from_list(from_str, x), from_none], obj.get("@type"))
        headline = from_union([from_str, from_none], obj.get("headline"))
        date_published = from_union([from_datetime, from_none], obj.get("datePublished"))
        date_modified = from_union([from_datetime, from_none], obj.get("dateModified"))
        author = from_union([lambda x: from_list(Author.from_dict, x), from_none], obj.get("author"))
        description = from_union([from_str, from_none], obj.get("description"))
        image = from_union([Image.from_dict, from_none], obj.get("image"))
        publisher = from_union([Publisher.from_dict, from_none], obj.get("publisher"))
        name = from_union([from_str, from_none], obj.get("name"))
        aggregate_rating = from_union([AggregateRating.from_dict, from_none], obj.get("aggregateRating"))
        cook_time = from_union([from_str, from_none], obj.get("cookTime"))
        nutrition = from_union([Nutrition.from_dict, from_none], obj.get("nutrition"))
        prep_time = from_union([from_str, from_none], obj.get("prepTime"))
        recipe_category = from_union([lambda x: from_list(from_str, x), from_none], obj.get("recipeCategory"))
        recipe_cuisine = from_union([lambda x: from_list(from_str, x), from_none], obj.get("recipeCuisine"))
        recipe_ingredient = from_union([lambda x: from_list(from_str, x), from_none], obj.get("recipeIngredient"))
        recipe_instructions = from_union([lambda x: from_list(RecipeInstruction.from_dict, x), from_none], obj.get("recipeInstructions"))
        recipe_yield = from_union([lambda x: from_list(lambda x: int(from_str(x)), x), from_none], obj.get("recipeYield"))
        total_time = from_union([from_str, from_none], obj.get("totalTime"))
        main_entity_of_page = from_union([MainEntityOfPage.from_dict, from_none], obj.get("mainEntityOfPage"))
        about = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("about"))
        return RecipeElement(context, type, headline, date_published, date_modified, author, description, image, publisher, name, aggregate_rating, cook_time, nutrition, prep_time, recipe_category, recipe_cuisine, recipe_ingredient, recipe_instructions, recipe_yield, total_time, main_entity_of_page, about)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.context is not None:
            result["@context"] = from_union([from_str, from_none], self.context)
        if self.type is not None:
            result["@type"] = from_union([lambda x: from_list(from_str, x), from_none], self.type)
        if self.headline is not None:
            result["headline"] = from_union([from_str, from_none], self.headline)
        if self.date_published is not None:
            result["datePublished"] = from_union([lambda x: x.isoformat(), from_none], self.date_published)
        if self.date_modified is not None:
            result["dateModified"] = from_union([lambda x: x.isoformat(), from_none], self.date_modified)
        if self.author is not None:
            result["author"] = from_union([lambda x: from_list(lambda x: to_class(Author, x), x), from_none], self.author)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.image is not None:
            result["image"] = from_union([lambda x: to_class(Image, x), from_none], self.image)
        if self.publisher is not None:
            result["publisher"] = from_union([lambda x: to_class(Publisher, x), from_none], self.publisher)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.aggregate_rating is not None:
            result["aggregateRating"] = from_union([lambda x: to_class(AggregateRating, x), from_none], self.aggregate_rating)
        if self.cook_time is not None:
            result["cookTime"] = from_union([from_str, from_none], self.cook_time)
        if self.nutrition is not None:
            result["nutrition"] = from_union([lambda x: to_class(Nutrition, x), from_none], self.nutrition)
        if self.prep_time is not None:
            result["prepTime"] = from_union([from_str, from_none], self.prep_time)
        if self.recipe_category is not None:
            result["recipeCategory"] = from_union([lambda x: from_list(from_str, x), from_none], self.recipe_category)
        if self.recipe_cuisine is not None:
            result["recipeCuisine"] = from_union([lambda x: from_list(from_str, x), from_none], self.recipe_cuisine)
        if self.recipe_ingredient is not None:
            result["recipeIngredient"] = from_union([lambda x: from_list(from_str, x), from_none], self.recipe_ingredient)
        if self.recipe_instructions is not None:
            result["recipeInstructions"] = from_union([lambda x: from_list(lambda x: to_class(RecipeInstruction, x), x), from_none], self.recipe_instructions)
        if self.recipe_yield is not None:
            result["recipeYield"] = from_union([lambda x: from_list(lambda x: from_str((lambda x: str(x))(x)), x), from_none], self.recipe_yield)
        if self.total_time is not None:
            result["totalTime"] = from_union([from_str, from_none], self.total_time)
        if self.main_entity_of_page is not None:
            result["mainEntityOfPage"] = from_union([lambda x: to_class(MainEntityOfPage, x), from_none], self.main_entity_of_page)
        if self.about is not None:
            result["about"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.about)
        return result


def recipe_from_dict(s: Any) -> List[RecipeElement]:
    return from_list(RecipeElement.from_dict, s)


def recipe_to_dict(x: List[RecipeElement]) -> Any:
    return from_list(lambda x: to_class(RecipeElement, x), x)
