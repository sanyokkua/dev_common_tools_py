import core.string_utils as su

GIT_CONFIG_USER_NAME = 'git config{}user.name "{}"'
GIT_CONFIG_USER_EMAIL = "git config{}user.email {}"


class UserNameOrEmailIsEmptyException(Exception):
    """
    An exception that is raised when a username or email is empty.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes a new instance of the UserNameOrEmailIsEmptyException class.

        :param message: The error message.
        """
        Exception.__init__(self, message)


def generate_git_config_commands(
    user_name: str, user_email: str, is_global: bool = True
) -> str:
    """
    Generates git config commands for setting user name and email.

    :param user_name: The user name to set.
    :param user_email: The user email to set.
    :param is_global: Whether to set the config globally. Default is True.
    :return: A string containing the generated git config commands.
    """
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


def join_commands_in_one(commands: list[str], ignore_errors: bool = False) -> str:
    """
    Joins a list of commands into a single command string.

    :param commands: The list of commands to join.
    :param ignore_errors: Whether to ignore errors when executing the commands. Default is False.
    :return: A string containing the joined commands.
    """
    separator: str = " & " if ignore_errors else " && "
    result = su.join_lines(commands, separator=separator)
    return result
