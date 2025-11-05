import argparse
import json
import os

def discover_server_files(base_dir: str, parent_dirs: list) -> dict:
    servers = {}

    for parent in parent_dirs:
        parent_path = os.path.join(base_dir, parent)
        if not os.path.isdir(parent_path):
            continue

        for entry in os.listdir(parent_path):
            subdir = os.path.join(parent_path, entry)
            if not os.path.isdir(subdir):
                continue

            for fname in os.listdir(subdir):
                if not fname.endswith(".py"):
                    continue
                if fname.startswith("_"):
                    continue

                full_path = os.path.abspath(os.path.join(subdir, fname))
                name = os.path.splitext(fname)[0]
                if name in servers:
                    name = f"{entry}_{name}"

                servers[name] = {
                    "command": "cmd",
                    "args": [
                        "/c",
                        f"{base_dir}\\.venv\\Scripts\\activate.bat && fastmcp run {full_path}"
                    ]
                }

    return servers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generate claude_desktop_config.json by discovering MCP server python files "
            "inside the provided parent directories (default: mal_mcp_servers and safe_mcp_servers)."
        )
    )
    parser.add_argument(
        "-d",
        "--dirs",
        nargs="+",
        help=(
            "Parent directories to scan. Provide one or more names relative to the script, "
            "e.g. -d mal_mcp_servers or -d mal_mcp_servers safe_mcp_servers. If omitted, both are used. "
            "You may also pass comma-separated values (they will be split)."
        ),
    )

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.dirs:
        parents = []
        for token in args.dirs:
            parts = [p.strip() for p in token.split(",") if p.strip()]
            parents.extend(parts)
    else:
        parents = ["mal_mcp_servers", "safe_mcp_servers"]

    discovered = discover_server_files(base_dir, parents)

    config = {"mcpServers": discovered}

    output_path = os.path.join(base_dir, "claude_desktop_config.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"설정 파일 생성 완료: {output_path}")