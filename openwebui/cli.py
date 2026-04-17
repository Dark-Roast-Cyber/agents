"""Simple CLI for exploring the OpenWebUI API."""

from __future__ import annotations

import argparse
import json
from typing import Any

from .chat import chat_completion
from .client import OpenWebUIError, get_client
from .functions import list_functions
from .knowledge import list_knowledge
from .models import create_model, delete_model, export_models, get_model, list_models
from .prompts import list_prompts
from .skills import list_skills
from .sync import import_agents, plan_sync, push_agents, push_commands, push_skills
from .tools import list_tools


def _print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, default=str))


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="python -m openwebui")
    subparsers = parser.add_subparsers(dest="resource", required=True)

    models_parser = subparsers.add_parser("models")
    models_subparsers = models_parser.add_subparsers(dest="action", required=True)
    models_subparsers.add_parser("list")

    models_get = models_subparsers.add_parser("get")
    models_get.add_argument("id")

    models_create = models_subparsers.add_parser("create")
    models_create.add_argument("--id", required=True)
    models_create.add_argument("--name", required=True)
    models_create.add_argument("--base-model")
    models_create.add_argument("--description")
    models_create.add_argument("--system-prompt")

    models_delete = models_subparsers.add_parser("delete")
    models_delete.add_argument("id")

    models_subparsers.add_parser("export")

    for name in ("tools", "functions", "prompts", "knowledge", "skills"):
        resource_parser = subparsers.add_parser(name)
        resource_subparsers = resource_parser.add_subparsers(
            dest="action", required=True
        )
        resource_subparsers.add_parser("list")

    sync_parser = subparsers.add_parser("sync")
    sync_subparsers = sync_parser.add_subparsers(dest="action", required=True)
    sync_subparsers.add_parser("plan")

    sync_push = sync_subparsers.add_parser("push")
    sync_push.add_argument("target", choices=("agents", "commands", "skills", "all"))

    sync_import = sync_subparsers.add_parser("import")
    sync_import.add_argument("target", choices=("agents",))

    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("--model", required=True)
    chat_parser.add_argument("--message", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.resource == "models":
            if args.action == "list":
                _print_json(list_models())
            elif args.action == "get":
                _print_json(get_model(args.id))
            elif args.action == "create":
                _print_json(
                    create_model(
                        id=args.id,
                        name=args.name,
                        base_model_id=args.base_model,
                        description=args.description,
                        system_prompt=args.system_prompt,
                    )
                )
            elif args.action == "delete":
                _print_json(delete_model(args.id))
            elif args.action == "export":
                _print_json(export_models())
        elif args.resource == "tools":
            _print_json(list_tools())
        elif args.resource == "functions":
            _print_json(list_functions())
        elif args.resource == "prompts":
            _print_json(list_prompts())
        elif args.resource == "knowledge":
            _print_json(list_knowledge())
        elif args.resource == "skills":
            _print_json(list_skills())
        elif args.resource == "chat":
            _print_json(
                chat_completion(
                    model=args.model,
                    messages=[{"role": "user", "content": args.message}],
                )
            )
        elif args.resource == "sync":
            client = get_client()
            if args.action == "plan":
                _print_json(plan_sync(client))
            elif args.action == "push":
                if args.target == "agents":
                    _print_json(push_agents(client))
                elif args.target == "commands":
                    _print_json(push_commands(client))
                elif args.target == "skills":
                    _print_json(push_skills(client))
                elif args.target == "all":
                    _print_json(
                        {
                            "agents": push_agents(client),
                            "commands": push_commands(client),
                            "skills": push_skills(client),
                        }
                    )
            elif args.action == "import" and args.target == "agents":
                _print_json(import_agents(client))
    except OpenWebUIError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    return 0
