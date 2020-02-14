import os

from flask import current_app, safe_join

from scrawl.utils import find_pages, full_directory_remove


def get_pages(work_directory: str):
    pages = []

    dir_content = os.listdir(work_directory)

    for name in dir_content:
        fullname = os.path.join(work_directory, name)

        if os.path.isdir(fullname):
            pages.append(name)

    return pages


def get_sub_pages(page_name: str, sub_name_pages: list, work_directory: str):
    pages = []

    dir_content = os.listdir(os.path.join(work_directory, page_name))

    for name in dir_content:
        fullname = os.path.join(work_directory, page_name, name)

        if os.path.isdir(fullname):
            pages.append(name)

    return pages


def update_page(content: str, page_name: str, work_directory: str):
    full_file_path = safe_join(work_directory, page_name, 'content.html')

    if os.path.exists(full_file_path):  # Checking for page existence
        with open(full_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    return False


def get_page(page_name: str, work_directory: str):
    full_file_path = safe_join(work_directory, page_name, 'content.html')

    if os.path.exists(full_file_path):  # Checking for page existence
        with open(full_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        page_name, sub_name_pages = find_pages(page_name)

        sub_pages = get_sub_pages(
            page_name=page_name,
            sub_name_pages=sub_name_pages,
            work_directory=work_directory
        )

        page = {
            'content': content,
            'sub_pages': sub_pages,
            'finding_pages': (page_name, sub_name_pages)
        }

        return page

    return False


def create_page(page_name: str, work_directory: str):
    directory_path = os.path.join(work_directory, page_name)
    page_path = safe_join(directory_path, 'content.html')

    if not os.path.exists(os.path.join(work_directory, page_name)):  # Checking for page existence
        os.makedirs(directory_path)

        with open(page_path, 'a+', encoding='utf-8') as f:
            create_text = current_app.config['DEFAULT_TEXT']
            f.write(create_text)

        return True

    return False


def create_sub_page(page_name: str, sub_page_name: str, new_sub_page_name: str, work_directory: str):
    directory_params = [work_directory, page_name]

    # if sub_page_name:
    #     directory_params.append(sub_page_name)

    if new_sub_page_name:
        directory_params.append(new_sub_page_name)

    page_directory_path = safe_join(work_directory, page_name)
    full_directory_path = safe_join(*directory_params)
    full_file_path = safe_join(full_directory_path, 'content.html')

    print(full_directory_path, full_file_path)

    if os.path.exists(page_directory_path):  # Checking for page existence
        os.makedirs(full_directory_path)

        with open(full_file_path, 'a+', encoding='utf-8') as file:
            create_text = current_app.config['DEFAULT_TEXT']
            file.write(create_text)

        return True

    return False


def rename_page(new_page_name: str, page_name: str, sub_page_name: str, work_directory: str):
    directory_params = [work_directory, page_name]

    if sub_page_name:
        directory_params.append(sub_page_name)

    full_directory_path = safe_join(*directory_params)

    if os.path.exists(full_directory_path):  # Checking for page existence
        new_path = os.path.join(os.path.dirname(full_directory_path), new_page_name)
        os.rename(full_directory_path, new_path)
        return True

    return False


def delete_page(page_name: str, sub_page_name: str, work_directory: str):
    directory_params = [work_directory, page_name]

    if sub_page_name != 'null':
        directory_params.append(sub_page_name)

    file_params = directory_params + ['content.html']

    full_directory_path = safe_join(*directory_params)
    full_file_path = safe_join(*file_params)

    if os.path.exists(full_file_path):  # Checking for page existence
        full_directory_remove(path=full_directory_path, work_directory=work_directory)

    if sub_page_name != 'null':
        return True

    return False
