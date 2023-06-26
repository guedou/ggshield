from typing import Any, List

import click


# Use https://github.com/click-contrib/click-default-group instead?


class DefaultCommandGroup(click.Group):
    """allow a default command for a group"""
    default_command: str | None = None

    def command(self, *args: Any, **kwargs: Any) -> Any:
        default_command: bool = kwargs.pop("default_command", False)
        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<>")
        decorator = super(DefaultCommandGroup, self).command(*args, **kwargs)

        if default_command:

            def new_decorator(f: Any) -> click.Command:
                cmd: click.Command = decorator(f)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx: click.Context, args: List[str]) -> Any:
        try:
            # test if the command parses
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.UsageError:
            # command did not parse, assume it is the default command
            if self.default_command is not None:
                args.insert(0, self.default_command)
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
