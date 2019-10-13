import numpy as np
import pytest
from match_three import GameInterface

@pytest.fixture
def fake_interface_preparation(scope="function"):
    fake_game_interface = GameInterface(None)
    fake_game_interface.part_of_three = np.zeros([fake_game_interface.no_lines,
                                                  fake_game_interface.no_columns])
    fake_game_interface.game_stat.score = 0
    colors = {0:"black", 1:"red", 2:"green"}

    for row_index in range(fake_game_interface.no_lines):
        for column_index in range(fake_game_interface.no_lines):
            if row_index % 2 == 0:
                fake_game_interface.ball_dict[row_index][column_index].color =\
                colors[column_index%3]
            else:
                fake_game_interface.ball_dict[row_index][column_index].color =\
                colors[(column_index+1)%3]
    yield fake_game_interface
    del fake_game_interface

def test_update_score_increments_score_for_normal_three(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    fake_game_interface.ball_dict[0][2].color = "red"
    fake_game_interface.ball_dict[0][3].color = "red"
    fake_game_interface.ball_dict[0][4].color = "green"
    fake_game_interface.find_three()

    fake_game_interface._update_score()
    expected_score = 3
    actual_score = fake_game_interface.game_stat.get_score()
    assert expected_score == actual_score

def test_update_score_increments_score_for_overlap(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    fake_game_interface.ball_dict[0][2].color = "red"
    fake_game_interface.ball_dict[0][3].color = "red"
    fake_game_interface.ball_dict[1][3].color = "red"
    fake_game_interface.ball_dict[2][3].color = "red"
    fake_game_interface.find_three()

    fake_game_interface._update_score()
    expected_score = 12
    actual_score = fake_game_interface.game_stat.get_score()
    assert expected_score == actual_score
