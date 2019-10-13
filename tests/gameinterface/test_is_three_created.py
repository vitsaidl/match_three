import pytest
from match_three import GameInterface

@pytest.fixture
def fake_interface_preparation(scope="function"):
    fake_game_interface = GameInterface(None)
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

def test_after_flip_three_is_not_created_and_flip_is_reversed(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    #colors of balls
    #BRGBRGBRG
    #RGBRGBRGB
    #BRGBRGBRG
    #etc.
    first_ball = fake_game_interface.ball_dict[0][1]
    second_ball = fake_game_interface.ball_dict[0][2]
    fake_game_interface.is_three_created(first_ball, second_ball)
    assert first_ball.color == "red"
    assert second_ball.color == "green"

def test_after_flip_three_is_created_and_flip_is_preserved(fake_interface_preparation):
    fake_game_interface = fake_interface_preparation
    #colors of balls
    #BRGRRGBRG
    #RGBRGBRGB
    #BRGBRGBRG
    #etc.
    fake_game_interface.ball_dict[0][3].color = "red"

    first_ball = fake_game_interface.ball_dict[0][1]
    second_ball = fake_game_interface.ball_dict[0][2]
    fake_game_interface.is_three_created(first_ball, second_ball)
    assert first_ball.color == "green"
    assert second_ball.color == "red"
