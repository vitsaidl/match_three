import numpy as np
import pytest
from match_three import GameInterface

@pytest.fixture
def fake_interface_preparation(scope="function"):
    fake_game_interface = GameInterface(None)
    fake_game_interface.part_of_three = np.zeros([fake_game_interface.no_lines,
                                                  fake_game_interface.no_columns])
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

def test_no_changes_in_part_of_three_for_no_three(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation

    fake_game_interface._is_part_of_vert_three(1)

    expected_array = np.zeros(fake_game_interface.no_columns)
    actual_array = fake_game_interface.part_of_three[:, 1]
    assert np.array_equal(actual_array, expected_array)

def test_changes_in_part_of_three_for_three(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation

    fake_game_interface.ball_dict[1][1].color = "red"
    fake_game_interface._is_part_of_vert_three(1)
    print(fake_game_interface.part_of_three)
    expected_array = np.zeros(fake_game_interface.no_columns)
    expected_array[0:3] = 1
    actual_array = fake_game_interface.part_of_three[:, 1]
    assert np.array_equal(actual_array, expected_array)

def test_changes_in_part_of_three_for_overlap(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation

    fake_game_interface.ball_dict[1][1].color = "red"
    fake_game_interface.ball_dict[3][1].color = "red"

    fake_game_interface._is_part_of_vert_three(1)
    print(fake_game_interface.part_of_three)
    expected_array = np.zeros(fake_game_interface.no_columns)
    expected_array[0:5] = 1
    expected_array[1:4] += 1
    expected_array[2] += 1
    actual_array = fake_game_interface.part_of_three[:, 1]
    assert np.array_equal(actual_array, expected_array)
