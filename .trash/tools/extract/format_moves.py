from dev.p488_mdl import Pokemon


def format_moves_pretty(poke_data: dict) -> list[str]:
    pokemon = Pokemon(**poke_data)
    lines = []

    for move_entry in pokemon.moves:
        move_name = move_entry.move.name
        move_id = move_entry.move.url.strip("/").split("/")[-1]
        version_names = [v.version_group.name for v in move_entry.version_group_details]

        lines.append(f"【{move_name}】 (ID: {move_id})")
        lines.append(f"  - versions: {', '.join(version_names)}")
        lines.append("")  # 空行で区切る

    return lines
