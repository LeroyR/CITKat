from flask import Blueprint, Markup, render_template, abort, current_app, safe_join
from markdown import Markdown

markdown_content_blueprint = Blueprint(name='markdown_content', import_name=__name__, url_prefix='/content')


@markdown_content_blueprint.route('/<path:fullpath>/')
def markdown_content(fullpath):
    if 'content-directory' not in current_app.config:
        err_msg = "<div class='alert alert-danger' role='alert'><svg height='16' class='octicon octicon-alert' viewBox='0 0 16 16' version='1.1' width='16' aria-hidden='true'><use xlink:href='#alert'></svg><code>citkat.config['content-directory']</code> is not set!</div>"
        if fullpath == 'Home':
            title = 'Home'
            content = Markup("<h1>Welcome!</h1>" + err_msg)
            return render_template('layout.html', **locals())
        return abort(500, err_msg)
    md = Markdown(extensions=['markdown.extensions.extra',
                              'markdown.extensions.toc',
                              'markdown.extensions.meta'])
    try:
        f = open(safe_join(current_app.config['content-directory'], fullpath) + '.md', 'rb')
    except IOError:
        abort(404)
    else:
        with f:
            content = Markup(md.convert(f.read()))
            title = 'Undefined'
            if 'title' in md.Meta:
                title = md.Meta['title'][0]
            return render_template('layout.html', **locals())
