import subprocess
from pathlib import Path


def cli_model_generate(input_path: str, output_path: str, class_name: str) -> None:
    subprocess.run(
        [
            "datamodel-codegen",
            "--input",
            input_path,
            "--input-file-type",
            "json",
            "--class-name",
            class_name,
            "--output",
            output_path,
        ],
        check=True,
    )


if __name__ == "__main__":
    models = [
        ("dev/f488.json", "dev/f488_mdl.py", "PokemonForm"),
        ("dev/p488.json", "dev/p488_mdl.py", "Pokemon"),
        ("dev/s488.json", "dev/s488_mdl.py", "PokemonSpecies"),
    ]

    for input_path, output_path, class_name in models:
        print(f"Generating {class_name} from {input_path}")
        cli_model_generate(input_path, output_path, class_name)
