from pathlib import Path


def read_file(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


def sort_user(d_lines):

    def get_user(line: str):
        user = line.split()[0]
        return user

    re_d_lines = sorted(d_lines, key=get_user, reverse=True)
    return re_d_lines


def sort_command(d_lines):

    def get_command(line: str):
        parts = line.split(None, 10)  # 11列に分割（COMMANDまで）
        if len(parts) >= 11:
            return parts[10].strip()
        return ""

    re_d_lines = sorted(d_lines, key=get_command, reverse=True)
    return re_d_lines


def write_file(path: Path, re_lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write(re_lines)


if __name__ == "__main__":
    lines = read_file(Path("ps.txt"))
    header, *d_lines = lines
    re_d_lines = sort_command(d_lines)
    re_lines = header + "".join(re_d_lines)
    write_file("re_ps.txt", re_lines)
