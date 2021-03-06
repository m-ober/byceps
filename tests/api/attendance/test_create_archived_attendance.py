"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.services.ticketing import attendance_service

from tests.helpers import create_user


def test_create_archived_attendance(
    api_client, api_client_authz_header, party, user
):
    before = attendance_service.get_attended_parties(user.id)
    assert before == []

    response = _send_request(
        api_client, api_client_authz_header, user.id, party.id
    )
    assert response.status_code == 204

    _assert_attended_party_ids(user.id, [party.id])


def test_create_archived_attendance_idempotency(
    api_client, api_client_authz_header, party
):
    user = create_user('AnotherUser')

    before = attendance_service.get_attended_parties(user.id)
    assert before == []

    # First addition. Should add the party.
    response = _send_request(
        api_client, api_client_authz_header, user.id, party.id
    )
    assert response.status_code == 204
    _assert_attended_party_ids(user.id, [party.id])

    # Second addition for same user and party. Should be ignored.
    response = _send_request(
        api_client, api_client_authz_header, user.id, party.id
    )
    assert response.status_code == 204
    _assert_attended_party_ids(user.id, [party.id])


def _send_request(api_client, api_client_authz_header, user_id, party_id):
    url = f'/api/attendances/archived_attendances'
    headers = [api_client_authz_header]
    json_data = {
        'user_id': str(user_id),
        'party_id': str(party_id),
    }

    return api_client.post(url, headers=headers, json=json_data)


def _assert_attended_party_ids(user_id, expected):
    parties = attendance_service.get_attended_parties(user_id)
    actual = [party.id for party in parties]
    assert actual == expected
