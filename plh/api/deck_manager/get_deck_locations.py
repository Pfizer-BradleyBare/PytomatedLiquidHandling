from plh.hal import centrifuge, deck_location, heat_cool_shake, magnetic_rack, vacuum


def get_deck_locations() -> deck_location.DeckLocationBase:

    devices = (
        heat_cool_shake.devices
        | centrifuge.devices
        | magnetic_rack.devices
        | vacuum.devices
    ).values()
    # These devices use special positions on deck that our not considered open when not in use.
    # Filter the deck positions out.
