"""
:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.services.seating import area_service, seat_service
from byceps.services.ticketing import category_service, event_service, \
    ticket_service

from tests.base import AbstractAppTestCase


class TicketAssignmentServiceTestCase(AbstractAppTestCase):

    def setUp(self):
        super().setUp()

        self.owner = self.create_user('Ticket_Owner')

        self.create_brand_and_party()

        self.category_id = self.create_category('Premium').id

        self.ticket = ticket_service.create_ticket(self.category_id,
                                                   self.owner.id)

    def test_appoint_and_withdraw_user_manager(self):
        manager = self.create_user('Ticket_Manager')

        assert self.ticket.user_managed_by_id is None

        # appoint user manager

        ticket_service.appoint_user_manager(self.ticket.id, manager.id,
                                            self.owner.id)
        assert self.ticket.user_managed_by_id == manager.id

        events_after_appointment = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_appointment) == 1

        appointment_event = events_after_appointment[0]
        assert appointment_event.event_type == 'user-manager-appointed'
        assert appointment_event.data == {
            'appointed_user_manager_id': str(manager.id),
            'initiator_id': str(self.owner.id),
        }

        # withdraw user manager

        ticket_service.withdraw_user_manager(self.ticket.id, self.owner.id)
        assert self.ticket.user_managed_by_id is None

        events_after_withdrawal = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_withdrawal) == 2

        withdrawal_event = events_after_withdrawal[1]
        assert withdrawal_event.event_type == 'user-manager-withdrawn'
        assert withdrawal_event.data == {
            'initiator_id': str(self.owner.id),
        }

    def test_appoint_and_withdraw_user(self):
        user = self.create_user('Ticket_User')

        assert self.ticket.used_by_id is None

        # appoint user

        ticket_service.appoint_user(self.ticket.id, user.id, self.owner.id)
        assert self.ticket.used_by_id == user.id

        events_after_appointment = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_appointment) == 1

        appointment_event = events_after_appointment[0]
        assert appointment_event.event_type == 'user-appointed'
        assert appointment_event.data == {
            'appointed_user_id': str(user.id),
            'initiator_id': str(self.owner.id),
        }

        # withdraw user

        ticket_service.withdraw_user(self.ticket.id, self.owner.id)
        assert self.ticket.used_by_id is None

        events_after_withdrawal = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_withdrawal) == 2

        withdrawal_event = events_after_withdrawal[1]
        assert withdrawal_event.event_type == 'user-withdrawn'
        assert withdrawal_event.data == {
            'initiator_id': str(self.owner.id),
        }

    def test_appoint_and_withdraw_seat_manager(self):
        manager = self.create_user('Ticket_Manager')

        assert self.ticket.seat_managed_by_id is None

        # appoint seat manager

        ticket_service.appoint_seat_manager(self.ticket.id, manager.id,
                                            self.owner.id)
        assert self.ticket.seat_managed_by_id == manager.id

        events_after_appointment = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_appointment) == 1

        appointment_event = events_after_appointment[0]
        assert appointment_event.event_type == 'seat-manager-appointed'
        assert appointment_event.data == {
            'appointed_seat_manager_id': str(manager.id),
            'initiator_id': str(self.owner.id),
        }

        # withdraw seat manager

        ticket_service.withdraw_seat_manager(self.ticket.id, self.owner.id)
        assert self.ticket.seat_managed_by_id is None

        events_after_withdrawal = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_withdrawal) == 2

        withdrawal_event = events_after_withdrawal[1]
        assert withdrawal_event.event_type == 'seat-manager-withdrawn'
        assert withdrawal_event.data == {
            'initiator_id': str(self.owner.id),
        }

    def test_occupy_and_release_seat(self):
        area = self.create_area('main', 'Main Hall')
        seat = seat_service.create_seat(area, 0, 0, self.category_id)

        assert self.ticket.occupied_seat_id is None

        # occupy seat

        ticket_service.occupy_seat(self.ticket.id, seat.id, self.owner.id)
        assert self.ticket.occupied_seat_id == seat.id

        events_after_occupation = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_occupation) == 1

        occupation_event = events_after_occupation[0]
        assert occupation_event.event_type == 'seat-occupied'
        assert occupation_event.data == {
            'seat_id': str(seat.id),
            'initiator_id': str(self.owner.id),
        }

        # release seat

        ticket_service.release_seat(self.ticket.id, self.owner.id)
        assert self.ticket.occupied_seat_id is None

        events_after_release = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_release) == 2

        release_event = events_after_release[1]
        assert release_event.event_type == 'seat-released'
        assert release_event.data == {
            'initiator_id': str(self.owner.id),
        }

    def test_switch_seat(self):
        area = self.create_area('main', 'Main Hall')
        seat1 = seat_service.create_seat(area, 0, 1, self.category_id)
        seat2 = seat_service.create_seat(area, 0, 2, self.category_id)

        self.ticket.occupied_seat_id = seat1.id

        # switch seat

        ticket_service.switch_seat(self.ticket.id, seat2.id, self.owner.id)
        assert self.ticket.occupied_seat_id == seat2.id

        events_after_switch = event_service.get_events_for_ticket(
            self.ticket.id)
        assert len(events_after_switch) == 1

        switch_event = events_after_switch[0]
        assert switch_event.event_type == 'seat-switched'
        assert switch_event.data == {
            'old_seat_id': str(seat1.id),
            'new_seat_id': str(seat2.id),
            'initiator_id': str(self.owner.id),
        }
    # -------------------------------------------------------------------- #
    # helpers

    def create_area(self, slug, title):
        return area_service.create_area(self.party.id, slug, title)

    def create_category(self, title):
        return category_service.create_category(self.party.id, title)
