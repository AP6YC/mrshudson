"""
    _utils.py

# Description
This files contains utilities internal to the `mrshudson` project.
"""


def _docstring_parameter(*sub):
    """This decorator replaces the __doc__ attribute of a function with a format string using the provided arguments.
    """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec


_ARG_ARGS = """
    *args: the subdirectories/files to join to the path.
"""

_ARG_PROJECT_STATE = """
    project_state (ProjectState, optional): The stateful representation of the project structure to use. Defaults to :const:`DEFAULT_PROJECT_STATE`.
"""

_ARG_ARGS_PROJECT_STATE = f"""
Args:
    {_ARG_ARGS}
    {_ARG_PROJECT_STATE}
"""
