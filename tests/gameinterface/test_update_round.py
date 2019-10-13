from match_three import GameInterface

def test_update_round_increments_round_counter():
    fake_game_interface = GameInterface(None)
    fake_game_interface.game_stat.round = 1
    assert fake_game_interface.game_stat.get_round() == 1
    fake_game_interface._update_round()
    assert fake_game_interface.game_stat.get_round() == 2
