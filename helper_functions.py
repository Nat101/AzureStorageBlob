# ===================================================================================
# Description: This module contains general helper functions for data integration
#
#   01/20/2025 - Natalie Carlson
#                   Created
# ===================================================================================


import os


def refactor_path(file_path, os_name=None):
    """This function sets the path connectors depending on the standards of a specific os.
    If caller specifies the os name, use that, otherwise, use the current os."""
    
    if os_name is None:
        os_name = os.name
    
    if os_name == 'posix': # Unix (Linux and MacOS)
        file_path = file_path.replace('\\', '/')
    else: # Windows
        file_path = file_path.replace('/', '\\')
    
    return file_path