"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import pytest

from byceps.services.tourney import (
    match_comment_service as comment_service,
    match_service,
)


def test_get_comment(api_client, api_client_authz_header, comment):
    url = f'/api/tourney/match_comments/{comment.id}'
    headers = [api_client_authz_header]

    response = api_client.get(url, headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.get_json() == {
        'comment_id': str(comment.id),
        'match_id': str(comment.match_id),
        'created_at': comment.created_at.isoformat(),
        'creator': {
            'user_id': str(comment.created_by.id),
            'screen_name': comment.created_by.screen_name,
            'suspended': False,
            'deleted': False,
            'avatar_url': None,
            'is_orga': False,
        },
        'body_text': 'Denn man tau.',
        'body_html': 'Denn man tau.',
        'last_edited_at': None,
        'last_editor': None,
        'hidden': False,
        'hidden_at': None,
        'hidden_by_id': None,
    }


def test_get_comment_with_edited_comment(
    api_client, api_client_authz_header, edited_comment
):
    comment = edited_comment

    url = f'/api/tourney/match_comments/{comment.id}'
    headers = [api_client_authz_header]

    response = api_client.get(url, headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.get_json() == {
        'comment_id': str(comment.id),
        'match_id': str(comment.match_id),
        'created_at': comment.created_at.isoformat(),
        'creator': {
            'user_id': str(comment.created_by.id),
            'screen_name': comment.created_by.screen_name,
            'suspended': False,
            'deleted': False,
            'avatar_url': None,
            'is_orga': False,
        },
        'body_text': '[b]So nicht[/b], Freundchen!',
        'body_html': '<strong>So nicht</strong>, Freundchen!',
        'last_edited_at': comment.last_edited_at.isoformat(),
        'last_editor': {
            'user_id': str(comment.last_edited_by.id),
            'screen_name': comment.last_edited_by.screen_name,
            'suspended': False,
            'deleted': False,
            'avatar_url': None,
            'is_orga': False,
        },
        'hidden': False,
        'hidden_at': None,
        'hidden_by_id': None,
    }


# helpers


@pytest.fixture
def match(app):
    return match_service.create_match()


@pytest.fixture
def comment(app, match, user):
    return comment_service.create_comment(match.id, user.id, 'Denn man tau.')


@pytest.fixture
def edited_comment(app, comment, admin):
    comment_service.update_comment(
        comment.id, admin.id, '[b]So nicht[/b], Freundchen!'
    )
    return comment_service.get_comment(comment.id)
