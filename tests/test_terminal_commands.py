import pytest

import core.terminal_commands as tc


def test_generate_git_config_commands_validate_username_input():
    """
    Tests if the generate_git_config_commands function raises an exception when the username input is empty.

    :return: None
    """
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands(None, "email@google.com")


def test_generate_git_config_commands_validate_user_email_input():
    """
    Tests if the generate_git_config_commands function raises an exception when the user email input is empty.

    :return: None
    """
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands("username", None)


def test_generate_git_config_commands_validate_username_input_empty():
    """
    Tests if the generate_git_config_commands function raises an exception when the username input is empty.

    :return: None
    """
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands("    ", "email@google.com")


def test_generate_git_config_commands_validate_user_email_input_empty():
    """
    Tests if the generate_git_config_commands function raises an exception when the user email input is empty.

    :return: None
    """
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands("username", "     ")


def test_generate_git_config_commands_local():
    """
    Tests if the generate_git_config_commands function generates the correct local git config commands.

    :return: None
    """
    username: str = "    myName_user     "
    email: str = "   myName_user@email.com  \n  "

    result: str = tc.generate_git_config_commands(username, email, is_global=False)

    assert (
        result
        == """git config user.name "myName_user"
git config user.email myName_user@email.com

git config user.name "myName_user"&&git config user.email myName_user@email.com"""
    )


def test_generate_git_config_commands_global():
    """
    Tests if the generate_git_config_commands function generates the correct global git config commands.

    :return: None
    """
    username: str = "    myName_user     "
    email: str = "   myName_user@email.com  \n  "

    result: str = tc.generate_git_config_commands(username, email)

    assert (
        result
        == """git config --global user.name "myName_user"
git config --global user.email myName_user@email.com

git config --global user.name "myName_user"&&git config --global user.email myName_user@email.com"""
    )


def test_join_commands_in_one():
    """
    Tests if the join_commands_in_one function correctly joins multiple commands into one command.

    :return: None
    """
    commands = ["cd folder/one", "git pull", "git commit -m 'message'"]
    result = tc.join_commands_in_one(commands)

    assert result == "cd folder/one && git pull && git commit -m 'message'"

    result_2 = tc.join_commands_in_one(commands, ignore_errors=True)

    assert result_2 == "cd folder/one & git pull & git commit -m 'message'"
