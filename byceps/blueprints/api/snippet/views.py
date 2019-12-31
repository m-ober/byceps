"""
byceps.blueprints.api.snippet.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import jsonify

from ....services.snippet import service as snippet_service
from ....services.snippet.transfer.models import Scope
from ....util.framework.blueprint import create_blueprint
from ....util.views import create_empty_json_response

from ...snippet.templating import get_snippet_context


blueprint = create_blueprint('api_snippet', __name__)


@blueprint.route('/by_name/<scope_type>/<scope_name>/<snippet_name>')
def view_by_name(scope_type, scope_name, snippet_name):
    """Return the current version of the snippet with that name in that
    scope.
    """
    scope = Scope(scope_type, scope_name)
    version = snippet_service.find_current_version_of_snippet_with_name(
        scope, snippet_name
    )
    if version is None:
        return create_empty_json_response(404)

    content = _get_content(version)

    return jsonify({
        'type': version.snippet.type_.name,
        'version': version.id,
        'content': content,
    })


def _get_content(version):
    context = get_snippet_context(version)

    content = {
        'body': context['body'],
    }

    if version.snippet.is_document:
        content.update({
            'title': context['title'],
            'head': context['head'],
        })

    return content