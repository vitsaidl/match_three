from collections import defaultdict
from match_three import GameInterface

def test_ball_dict_fills_with_expected_number_of_balls():
    fake_game_interface = GameInterface(None)
    fake_game_interface.ball_dict = defaultdict(dict)

    fake_game_interface._fill_ball_dict()

    expected_no_balls_in_dict = fake_game_interface.no_lines * \
    fake_game_interface.no_columns
    actual_no_balls_in_dict = 0
    for layer in fake_game_interface.ball_dict:
        actual_no_balls_in_dict += len(fake_game_interface.ball_dict[layer])
    assert expected_no_balls_in_dict == actual_no_balls_in_dict

def test_ball_dict_fills_with_balls():
    fake_game_interface = GameInterface(None)
    fake_game_interface.ball_dict = defaultdict(dict)

    fake_game_interface._fill_ball_dict()

    first_ball = fake_game_interface.ball_dict[0][0]
    expected_type = "<class 'match_three.Fields'>"
    actual_type = str(type(first_ball))
    assert expected_type == actual_type
