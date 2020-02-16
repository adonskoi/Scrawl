import os
import sys

from flask import jsonify, make_response

sys.setrecursionlimit(100)


def find_pages(page_name: str):
    page_data = page_name.split('/')

    if len(page_data) > 1:
        return page_data

    return page_data[0], ''


def render_error(message: str, status_code=500):
    content = jsonify(detail=message)
    return make_response(content, status_code)


def __full_directory_remove(path: str):
    if os.path.exists(path):
        for the_file in os.listdir(path):
            file_path = os.path.join(path, the_file)

            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)

                else:
                    __full_directory_remove(file_path)

            except OSError as error:
                print('Deleting error:', error)

        os.rmdir(path)


def full_directory_remove(path: str, work_directory: str):
    content_directory = os.path.join(work_directory, path)
    __full_directory_remove(content_directory)
