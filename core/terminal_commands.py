import core.string_utils as su

GIT_CONFIG_USER_NAME = 'git config{}user.name "{}"'
GIT_CONFIG_USER_EMAIL = "git config{}user.email {}"


class UserNameOrEmailIsEmptyException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


def generate_git_config_commands(
    user_name: str, user_email: str, is_global: bool = True
) -> str:
    if (
        not user_name
        or not user_email
        or len(user_name.strip()) == 0
        or len(user_email.strip()) == 0
    ):
        raise UserNameOrEmailIsEmptyException(
            "Passed user name ({}) and email ({}) are not correct".format(
                user_name, user_email
            )
        )
    global_flag: str = " --global " if is_global else " "
    git_config_name: str = GIT_CONFIG_USER_NAME.format(global_flag, user_name.strip())
    git_config_email: str = GIT_CONFIG_USER_EMAIL.format(
        global_flag, user_email.strip()
    )
    commands: list[str] = [git_config_name, git_config_email]

    commands_separate: str = su.join_lines(commands, "\n")
    commands_to_execute_batch: str = su.join_lines(commands, "&&")

    return su.join_lines(
        [commands_separate, "", commands_to_execute_batch], separator="\n"
    )
