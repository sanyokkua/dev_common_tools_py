import pytest
import core.terminal_commands as tc


def test_generate_git_config_commands_validate_username_input():
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands(None, "email@google.com")


def test_generate_git_config_commands_validate_user_email_input():
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands("username", None)


def test_generate_git_config_commands_validate_username_input_empty():
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands("    ", "email@google.com")


def test_generate_git_config_commands_validate_user_email_input_empty():
    with pytest.raises(tc.UserNameOrEmailIsEmptyException) as ex:
        tc.generate_git_config_commands("username", "     ")


def test_generate_git_config_commands_local():
    username: str = "    myName_user     "
    email: str = "   myName_user@email.com  \n  "

    result: str = tc.generate_git_config_commands(username, email, is_global=False)

    assert result == """git config user.name "myName_user"
git config user.email myName_user@email.com

git config user.name "myName_user"&&git config user.email myName_user@email.com"""


def test_generate_git_config_commands_global():
    username: str = "    myName_user     "
    email: str = "   myName_user@email.com  \n  "

    result: str = tc.generate_git_config_commands(username, email)

    assert result == """git config --global user.name "myName_user"
git config --global user.email myName_user@email.com

git config --global user.name "myName_user"&&git config --global user.email myName_user@email.com"""
