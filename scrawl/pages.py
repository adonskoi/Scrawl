from flask import (Blueprint, current_app, redirect, render_template, request, url_for)

from scrawl import pages_utils
from scrawl.utils import render_error

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
    work_directory = current_app.config['PAGES_PATH']
    pages = pages_utils.get_pages(work_directory=work_directory)
    pages_with_sub_pages = pages_utils.get_pages_info(work_directory=work_directory)
    return render_template('base.html', pages=pages, pages_with_sub_pages=pages_with_sub_pages)


@bp.route('/pages/<path:page_name>', methods=('GET', 'POST'))
def render_page(page_name):
    work_directory = current_app.config['PAGES_PATH']

    if request.method == 'POST':
        # todo: security
        content = request.form.get('content')

        if content is None:
            return render_error('The content parameter is missing')

        elif not content:
            content = current_app.config['DEFAULT_TEXT']

        content = content.strip()  # Purification of the content from the extra spaces

        print(content)

        status = pages_utils.update_page(
            content=content,
            page_name=page_name,
            work_directory=work_directory
        )

        if not status:
            return render_error('There is no such page', status_code=404)

    pages = pages_utils.get_pages(work_directory=work_directory)
    page = pages_utils.get_page(page_name=page_name, work_directory=work_directory)
    pages_with_sub_pages = pages_utils.get_pages_info(work_directory=work_directory)

    if not page:
        return redirect(url_for('pages.index'))  # If there is no page redirect to the main page

    page_name, sub_page_name = page['finding_pages']

    return render_template(
        'base.html', pages=pages, current_page=page_name, current_sub_page=sub_page_name,
        content=page['content'], sub_pages=page['sub_pages'], pages_with_sub_pages=pages_with_sub_pages,
    )


@bp.route('/create_page', methods=['POST'])
def create_page():
    # todo: security;
    # http://lucumr.pocoo.org/2010/12/24/common-mistakes-as-web-developer/
    page_name = request.form['page_name']
    work_directory = current_app.config['PAGES_PATH']

    status = pages_utils.create_page(page_name=page_name, work_directory=work_directory)

    message = 'The page was created successfully' if status else 'The page with this name already exists'

    print(message)

    return redirect(url_for('pages.render_page', page_name=page_name))


@bp.route('/create_sub_page', methods=['POST'])
def create_sub_page():
    # todo: security;
    # http://lucumr.pocoo.org/2010/12/24/common-mistakes-as-web-developer/
    page_name = request.form['page_name']
    sub_page_name = request.form['sub_page_name']
    new_sub_page_name = request.form['new_sub_page_name']
    work_directory = current_app.config['PAGES_PATH']

    status = pages_utils.create_sub_page(page_name=page_name, sub_page_name=sub_page_name,
                                         new_sub_page_name=new_sub_page_name, work_directory=work_directory)

    if not status:
        return redirect(url_for('pages.index'))  # If there is no page redirect to the main page

    return redirect(url_for('pages.render_page', page_name='%s/%s' % (page_name, sub_page_name)))


@bp.route('/rename_page', methods=['POST'])
def rename_page():
    # todo: security;
    # http://lucumr.pocoo.org/2010/12/24/common-mistakes-as-web-developer/
    page_name = request.form['page_name']
    sub_page_name = request.form['sub_page_name']
    new_page_name = request.form['new_page_name']
    work_directory = current_app.config['PAGES_PATH']

    status = pages_utils.rename_page(new_page_name=new_page_name, page_name=page_name,
                                     sub_page_name=sub_page_name, work_directory=work_directory)

    if not status:
        return redirect(url_for('pages.index'))  # If there is no page redirect to the main page

    new_url = new_page_name
    if sub_page_name:
        new_url = '%s/%s' % (page_name, new_page_name)

    return redirect(url_for('pages.render_page', page_name=new_url))


@bp.route('/delete_page', methods=['POST'])
def delete_page():
    # todo: security;
    # http://lucumr.pocoo.org/2010/12/24/common-mistakes-as-web-developer/
    page_name = request.form['page_name']
    sub_page_name = request.form['sub_page_name']
    work_directory = current_app.config['PAGES_PATH']

    status = pages_utils.delete_page(page_name=page_name, sub_page_name=sub_page_name,
                                     work_directory=work_directory)

    if status:
        return redirect(url_for('pages.render_page', page_name=page_name))

    return redirect(url_for('pages.index'))
