import inspect
from src.extract.transform import JsonTransformer

methods = [
    name
    for name, obj in inspect.getmembers(JsonTransformer, predicate=inspect.isfunction)
]

if __name__ == "__main__":
    print(",".join(methods))
