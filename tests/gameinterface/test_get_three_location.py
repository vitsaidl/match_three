import pytest
from match_three import GameInterface

@pytest.fixture
def fake_interface_preparation(scope="function"):
    fake_game_interface = GameInterface(None)
    colors = {0:"black", 1:"red", 2:"green"}

    for row_index in range(fake_game_interface.no_lines):
        for column_index in range(fake_game_interface.no_lines):
            if row_index % 2 == 0:
                fake_game_interface.ball_dict[row_index][column_index].color = \
                colors[column_index%3]
            else:
                fake_game_interface.ball_dict[row_index][column_index].color = \
                colors[(column_index+1)%3]
    yield fake_game_interface
    del fake_game_interface

def test_no_three_in_dict_right_amount_of_found_balls(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    ball_loc_in_three, number_of_balls_in_three = fake_game_interface.get_three_locations()
    assert number_of_balls_in_three == 0
    assert len(ball_loc_in_three[0]) == 0

def test_one_three_in_dict_right_amount_of_found_balls(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    fake_game_interface.ball_dict[0][1].color = "black"
    fake_game_interface.ball_dict[0][2].color = "black"
    #so we have 3 and not 4 same colored balls in line
    fake_game_interface.ball_dict[0][3].color = "blue"
    ball_loc_in_three, number_of_balls_in_three = fake_game_interface.get_three_locations()
    assert number_of_balls_in_three == 3
    assert len(ball_loc_in_three[0]) == 3

def test_one_three_in_dict_right_balls_coordinates(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    fake_game_interface.ball_dict[0][1].color = "black"
    fake_game_interface.ball_dict[0][2].color = "black"
    #so we have 3 and not 4 same colored balls in line
    fake_game_interface.ball_dict[0][3].color = "blue"
    ball_loc_in_three, number_of_balls_in_three = fake_game_interface.get_three_locations()

    expected_first_x = 0
    expected_first_y = 0
    expected_second_x = 0
    expected_second_y = 1
    expected_third_x = 0
    expected_third_y = 2
    actual_first_x = ball_loc_in_three[0][0]
    actual_first_y = ball_loc_in_three[1][0]
    actual_second_x = ball_loc_in_three[0][1]
    actual_second_y = ball_loc_in_three[1][1]
    actual_third_x = ball_loc_in_three[0][2]
    actual_third_y = ball_loc_in_three[1][2]
    assert expected_first_x == actual_first_x
    assert expected_first_y == actual_first_y
    assert expected_second_x == actual_second_x
    assert expected_second_y == actual_second_y
    assert expected_third_x == actual_third_x
    assert expected_third_y == actual_third_y

def test_threeplus_overlaps_corrent_amount_of_balls(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    fake_game_interface.ball_dict[0][1].color = "black"
    fake_game_interface.ball_dict[0][2].color = "black"
    fake_game_interface.ball_dict[1][2].color = "black"
    fake_game_interface.ball_dict[2][2].color = "black"
    ball_loc_in_three, number_of_balls_in_three = fake_game_interface.get_three_locations()
    assert number_of_balls_in_three == 7
    assert len(ball_loc_in_three[0]) == 7
