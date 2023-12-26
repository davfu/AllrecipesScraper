from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Image:
    type: Optional[str] = None
    url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        height = from_union([from_int, from_none], obj.get("height"))
        width = from_union([from_int, from_none], obj.get("width"))
        return Image(type, url, height, width)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        return result


@dataclass
class Nutrition:
    cals: Optional[int] = None
    protein: Optional[int] = None
    carbs: Optional[int] = None
    fat: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Nutrition':
        assert isinstance(obj, dict)
        cals = from_union([from_int, from_none], obj.get("cals"))
        protein = from_union([from_int, from_none], obj.get("protein"))
        carbs = from_union([from_int, from_none], obj.get("carbs"))
        fat = from_union([from_int, from_none], obj.get("fat"))
        return Nutrition(cals, protein, carbs, fat)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.cals is not None:
            result["cals"] = from_union([from_int, from_none], self.cals)
        if self.protein is not None:
            result["protein"] = from_union([from_int, from_none], self.protein)
        if self.carbs is not None:
            result["carbs"] = from_union([from_int, from_none], self.carbs)
        if self.fat is not None:
            result["fat"] = from_union([from_int, from_none], self.fat)
        return result


@dataclass
class Recipe:
    url: Optional[str] = None
    title: Optional[str] = None
    rating: Optional[float] = None
    rev_count: Optional[int] = None
    category: Optional[List[str]] = None
    cuisine: Optional[List[str]] = None
    ingredients: Optional[List[str]] = None
    time: Optional[str] = None
    nutrition: Optional[Nutrition] = None
    image: Optional[Image] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Recipe':
        assert isinstance(obj, dict)
        url = from_union([from_str, from_none], obj.get("url"))
        title = from_union([from_str, from_none], obj.get("title"))
        rating = from_union([from_float, from_none], obj.get("rating"))
        rev_count = from_union([from_int, from_none], obj.get("rev_count"))
        category = from_union([lambda x: from_list(from_str, x), from_none], obj.get("category"))
        cuisine = from_union([lambda x: from_list(from_str, x), from_none], obj.get("cuisine"))
        ingredients = from_union([lambda x: from_list(from_str, x), from_none], obj.get("ingredients"))
        time = from_union([from_str, from_none], obj.get("time"))
        nutrition = from_union([Nutrition.from_dict, from_none], obj.get("nutrition"))
        image = from_union([Image.from_dict, from_none], obj.get("image"))
        return Recipe(url, title, rating, rev_count, category, cuisine, ingredients, time, nutrition, image)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.rating is not None:
            result["rating"] = from_union([to_float, from_none], self.rating)
        if self.rev_count is not None:
            result["rev_count"] = from_union([from_int, from_none], self.rev_count)
        if self.category is not None:
            result["category"] = from_union([lambda x: from_list(from_str, x), from_none], self.category)
        if self.cuisine is not None:
            result["cuisine"] = from_union([lambda x: from_list(from_str, x), from_none], self.cuisine)
        if self.ingredients is not None:
            result["ingredients"] = from_union([lambda x: from_list(from_str, x), from_none], self.ingredients)
        if self.time is not None:
            result["time"] = from_union([from_str, from_none], self.time)
        if self.nutrition is not None:
            result["nutrition"] = from_union([lambda x: to_class(Nutrition, x), from_none], self.nutrition)
        if self.image is not None:
            result["image"] = from_union([lambda x: to_class(Image, x), from_none], self.image)
        return result


def recipe_from_dict(s: Any) -> Recipe:
    return Recipe.from_dict(s)


def recipe_to_dict(x: Recipe) -> Any:
    return to_class(Recipe, x)
