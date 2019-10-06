# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 08:36:06 2019

@author: Vit Saidl
"""

import tkinter
import random
from collections import defaultdict
import numpy as np

class GameStats():
    """Representing global game stats, e.g. score
    """
    def __init__(self):
        self.score = 0
        self.round = 1

    def increment_round(self):
        """Increments round variable by 1
        """
        self.round += 1

    def get_round(self):
        """Returns current round value
        """
        return self.round

    def add_score(self, points):
        """Increment score variable by given value

        Args:
            points(integer): Number of additional points
        """
        self.score += points

    def get_score(self):
        """Returns current score value
        """
        return int(self.score)

class PointContainer():
    """Representing point - crate for two coordinates
    """
    def __init__(self, x_axis, y_axis):
        """Initializatioon - filling the crate
        """
        self.x_axis = x_axis
        self.y_axis = y_axis

class Fields():
    """Representing individual fields with balls
    """
    USED_COLORS = {0: "red",
                   1: "green",
                   2: "blue",
                   3: "black",
                   4: "cyan",
                   5: "violet",
                   6: "purple"}
    NO_USED_COLORS = len(USED_COLORS)

    def __init__(self, game_window, x_axis, y_axis,
                 top_left_point, bottom_right_point):
        """Sets ball parameters and draws in on the game board

        Args:
            game_window(tkinter.Canvas): Container where balls are drawn
            x_axis(integer): Horizontal position on the game grid
            y_axis(integer): Vertical position on the game grid
            top_left_point(PointContainer): Coordinates of field top left point
            on game board
            bottom_right_point(PointContainer): Coordinates of field bottom right
            point on game board
        """
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.color = Fields.USED_COLORS[random.randrange(Fields.NO_USED_COLORS)]
        self.create_ball(game_window, top_left_point, bottom_right_point)

    def reset_color(self, game_window):
        """Reseting ball color to random color and redrawing it

        Args:
            game_window(tkinter.Canvas): Container where balls are drawn
        """
        self.color = Fields.USED_COLORS[random.randrange(Fields.NO_USED_COLORS)]
        self.redraw_color(game_window)

    def redraw_to_yellow_color(self, game_window):
        """Reseting ball color to yellow and redrawing it

        Args:
            game_window(tkinter.Canvas): Container where balls are drawn
        """
        self.color = "yellow"
        self.redraw_color(game_window)

    def redraw_color(self, game_window):
        """Redrawing ball with current color

        Args:
            game_window(tkinter.Canvas): Container where balls are drawn
        """
        game_window.itemconfig(self.ball, fill=self.color)

    def create_ball(self, game_window, top_left_point, bottom_right_point):
        """Draws ball on the game board

        Args:
            game_window(tkinter.Canvas): Container where balls are drawn
            top_left_point(PointContainer): Coordinates of field top left point
            on game board
            bottom_right_point(PointContainer): Coordinates of field bottom right
            point on game board
        """
        self.ball = game_window.create_oval(
            top_left_point.x_axis,
            top_left_point.y_axis,
            bottom_right_point.x_axis,
            bottom_right_point.y_axis,
            fill=self.color, width=2)

    def create_highlight(self, game_window, top_left_point, bottom_right_point):
        """Creating highligh around field selected by user

        Args:
            game_window(tkinter.Canvas): Container where balls are drawn
            top_left_point(PointContainer): Coordinates of field top left point
            on game board
            bottom_right_point(PointContainer): Coordinates of field bottom right
            point on game board
        """
        self.highlight = game_window.create_rectangle(
            top_left_point.x_axis,
            top_left_point.y_axis,
            bottom_right_point.x_axis,
            bottom_right_point.y_axis,
            outline="yellow", width=5)

    def destroy_highlight(self, game_window):
        """Destroying highligh around field previously selected by user

        Args:
            game_window(tkinter.Canvas): Container where balls are drawn
        """
        game_window.delete(self.highlight)

    def is_neighbour(self, another_field):
        """Testing whether filds are neighbours

        Args:
            another_field(Fields): Another instance of Fields class

        Returns:
            bool: True means that fields are neighbours
        """
        x_another = another_field.x_axis
        y_another = another_field.y_axis

        x_difference = self.x_axis - x_another
        y_difference = self.y_axis - y_another
        abs_sum_difference = abs(x_difference)+abs(y_difference)
        return (abs_sum_difference == 1)

class GameInterface():
    """Representing game board
    """
    _instance = None

    def _set_interface_params(self, master_window):
        """Setting class parameters - de facto replacement for __init__ function

        Class is created as singleton, thus __new__ is used and __init__ is
        ommited (__init__ would be called on each class call regardles on previous
        instance existence).

        Args:
            master_window(tkinter.Tk):Tkinter widget where whole game takes place
        """
        self.width_game_field = 500
        self.height_game_field = 500
        self.height_interface = 50
        self.window_horiz_offset = 10

        self.no_lines = 10
        self.no_columns = self.no_lines

        self.line_height = self.height_game_field // self.no_lines
        self.column_width = self.width_game_field // self.no_columns

        window_width = self.width_game_field+2*self.window_horiz_offset
        window_height = self.height_game_field + self.height_interface
        self.game_window = tkinter.Canvas(master_window,
                                          width=window_width,
                                          height=window_height)
        self.game_window.bind("<Button-1>", self.left_mouse_click)
        self.game_window.pack()

        self.ball_dict = defaultdict(dict)
        self._fill_ball_dict()

        self.selected_field = None
        self.part_of_three = np.zeros([self.no_lines, self.no_columns])

        self.game_stat = GameStats()

        text_y_position = self.height_interface/2
        self.text_points = self.game_window.create_text(
            self.window_horiz_offset,
            text_y_position, anchor=tkinter.W,
            font="Purisa",
            text="Points: 0")
        self.round_counter = self.game_window.create_text(
            8*self.width_game_field/9,
            text_y_position, anchor=tkinter.W,
            font="Purisa",
            text="Round: 1")

        self._cleaning_from_three(initial_cleansing=True)

    def _fill_ball_dict(self):
        """Fills dictionary with individual balls
        """
        for line in range(self.no_lines):
            for column in range(self.no_columns):
                left_upper_corner = PointContainer(
                    self.window_horiz_offset+column*self.column_width,
                    self.height_interface+line*self.line_height)
                right_lower_corner = PointContainer(
                    self.window_horiz_offset+(column+1)*self.column_width,
                    self.height_interface+(line+1)*self.line_height)
                self.ball_dict[line][column] = Fields(
                    self.game_window, line, column,
                    left_upper_corner, right_lower_corner)

    def _cleaning_from_three(self, initial_cleansing=False):
        """Goes though game board, finds all large enough groups of one colored
        balls and replaces them (and awards points for it)

        Args:
            initial_cleansing(bool): True means that recolored balls don't go
            through yellow phase
        """
        nonzeros, number_of_nonzeros = self.get_three_locations()
        if (number_of_nonzeros and not initial_cleansing) > 0:
            self._update_score()
            self.game_window.after(200, self.draw_yellow_balls,
                                   number_of_nonzeros, nonzeros)
        elif (number_of_nonzeros and initial_cleansing) > 0:
            self.draw_new_balls(number_of_nonzeros, nonzeros,
                                initial_cleansing=True)

    def draw_yellow_balls(self, number_of_balls, balls_coordinates):
        """Change color of chosen balls and after a certain time, calls
        function draw_new_balls

        Args:
            number_of_balls(integer): Number of chosen balls
            balls_coordinates(tuple(numpy.ndarray)):tuple of two arrays - first
            with x-location, second with y-location of chosen balls
            initial_cleansing(bool): True means that recolored balls don't go
            through yellow phase
        """

        for index in range(number_of_balls):
            index_x = (balls_coordinates[0])[index]
            index_y = (balls_coordinates[1])[index]
            self.ball_dict[index_x][index_y].redraw_to_yellow_color(self.game_window)
        time_delay = 200
        self.game_window.after(
            time_delay, self.draw_new_balls,
            number_of_balls, balls_coordinates)

    def draw_new_balls(self, number_of_balls, balls_coordinates,
                       initial_cleansing=False):
        """Resets color of chosen balls and check if 3+ long line of same
        colored balls is created

        Args:
            number_of_balls(integer): Number of chosen balls
            balls_coordinates(tuple(numpy.ndarray)):tuple of two arrays - first
            with x-location, second with y-location of chosen balls
            initial_cleansing(bool): True means that recolored balls don't go
            through yellow phase
        """
        self._reset_three_balls(number_of_balls, balls_coordinates)
        self._cleaning_from_three(initial_cleansing)

    def get_three_locations(self):
        """Returns coordinates of lines with 3+ same colored balls and how many
        of these balls are

        Additionaly it writes to self.part_of_three info about number
        of lines each ball is participating

        Returns:
            tuple(integer, tuple(numpy.ndarray)): First element is number of balls,
            second tuple of two arrays - first with x-location, second with
            y-location of all these balls
        """
        self.part_of_three = np.zeros([self.no_lines, self.no_columns])
        self.find_three()
        nonzeros = np.where(self.part_of_three > 0)
        number_of_nonzeros = len(nonzeros[0])
        return (nonzeros, number_of_nonzeros)

    def is_three_created(self, first, second):
        """Changes color of two balls and check if line of 3+ is created

        first(Fields): Field with first ball
        second(Fields): Field with second ball
        """
        first.color, second.color = second.color, first.color
        nonzeros, number_of_nonzeros = self.get_three_locations()
        if number_of_nonzeros == 0:
            first.color, second.color = second.color, first.color
        else:
            self._update_score()
            self._update_round()
            first.redraw_color(self.game_window)
            second.redraw_color(self.game_window)
            self.game_window.after(200, self.draw_yellow_balls,
                                   number_of_nonzeros, nonzeros)

    def _update_round(self):
        """Updates round value and update label
        """
        self.game_stat.increment_round()
        self._write_rounds()

    def _update_score(self):
        """Updates score value and score label
        """
        self.game_stat.add_score(self.part_of_three.sum())
        self._write_points()

    def find_left_mouse_click(self, event):
        """Determines on which ball in game board user clicked

        Args:
            event(tkinter.Event): Object with information about user click
        """
        loc_x_axis = event.x
        loc_y_axis = event.y

        clicked_upper_interface = (loc_y_axis < self.height_interface)
        clicked_left_offset = (loc_x_axis < self.window_horiz_offset)
        clicked_right_offset = (loc_x_axis > \
                                self.window_horiz_offset+self.width_game_field)

        if clicked_upper_interface:
            print("User clicked on inteface")
            return None
        elif (clicked_left_offset or clicked_right_offset):
            print("User clicked on left/right edge")
            return None
        else:
            loc_x_field = loc_x_axis - self.window_horiz_offset
            loc_y_field = loc_y_axis - self.height_interface

            y_field = loc_x_field // self.column_width
            x_field = loc_y_field // self.line_height
            print("User clicked into field: ", x_field, y_field)

            return (x_field, y_field)

    def left_mouse_click(self, event):
        """Processing user click

        If user click on inteface above game board, destroy ball highlight
        and otherwise do nothing
        If user click on left/right edge, destroy ball highlight
        and otherwise do nothing
        If user click on board on certain ball and no other ball is selected,
        select clicked ball
        If user click on board on certain ball and other ball is selected,
        test if they are neighours and if yes, if they can change place

        Args:
            event(tkinter.Event): Object with information about user click
        """
        clicked_field = self.find_left_mouse_click(event)
        if (clicked_field is not None and self.selected_field is None):
            field_no_x, field_no_y = clicked_field

            left_upper_corner = PointContainer(
                self.window_horiz_offset+field_no_y*self.column_width,
                self.height_interface+field_no_x*self.line_height)
            right_lower_corner = PointContainer(
                self.window_horiz_offset+(field_no_y+1)*self.column_width,
                self.height_interface+(field_no_x+1)*self.line_height)
            affected_field = self.ball_dict[field_no_x][field_no_y]
            affected_field.create_highlight(
                self.game_window,
                left_upper_corner,
                right_lower_corner)
            self.selected_field = affected_field
        elif (clicked_field is not None and self.selected_field is not None):
            field_no_x, field_no_y = clicked_field

            affected_field = self.ball_dict[field_no_x][field_no_y]
            are_neighbours = self.selected_field.is_neighbour(affected_field)
            if are_neighbours:
                self.is_three_created(self.selected_field, affected_field)
            self.selected_field.destroy_highlight(self.game_window)
            self.selected_field = None
        else:
            if self.selected_field is not None:
                self.selected_field.destroy_highlight(self.game_window)
                self.selected_field = None

    def _write_points(self):
        """Updates score label with current score value
        """
        self.game_window.itemconfig(
            self.text_points,
            text=f"Points: {self.game_stat.get_score()}")

    def _write_rounds(self):
        """Updates round label with current round value
        """
        self.game_window.itemconfig(
            self.round_counter,
            text=f"Round: {self.game_stat.get_round()}")

    def _reset_three_balls(self, number_of_nonzeros, nonzeros):
        """Randomly resets color of same-colored balls forming cluster during
        initialization

        Args:
            number_of_nonzeros(int): Number of balls to reset
            nonzeros(numpy.ndarray): Tuple of two numpy arrays - first with \
            x-axis, second with y-axis of reseted ball
        """
        for index in range(number_of_nonzeros):
            index_x = (nonzeros[0])[index]
            index_y = (nonzeros[1])[index]
            self.ball_dict[index_x][index_y].reset_color(self.game_window)

    def _find_horiz_three_all_lines(self):
        """Looks for clusters of three in every line of game board
        """
        for line_id in range(0, self.no_lines):
            self._is_part_of_horiz_three(line_id)

    def _is_part_of_horiz_three(self, line_id):
        """Looks for clusters of three in given line

        Args:
            line_id(int): Number identifying searched line
        """
        color_first = self.ball_dict[line_id][0].color
        color_second = self.ball_dict[line_id][1].color
        first_two_same_color = (color_first == color_second)
        for column_id in range(2, self.no_columns):
            color_third = self.ball_dict[line_id][column_id].color
            if (first_two_same_color and (color_second == color_third)):
                self.part_of_three[line_id][column_id] += 1
                self.part_of_three[line_id][column_id-1] += 1
                self.part_of_three[line_id][column_id-2] += 1
            color_first = color_second
            color_second = color_third
            first_two_same_color = (color_first == color_second)

    def _find_vert_three_all_lines(self):
        """Looks for clusters of three in every column of game board
        """
        for column_id in range(0, self.no_columns):
            self._is_part_of_vert_three(column_id)

    def _is_part_of_vert_three(self, column_id):
        """Looks for clusters of three in given line

        Args:
            line_id(int): Number identifying searched line
        """
        color_first = self.ball_dict[0][column_id].color
        color_second = self.ball_dict[1][column_id].color
        first_two_same_color = (color_first == color_second)
        for line_id in range(2, self.no_lines):
            color_third = self.ball_dict[line_id][column_id].color
            if (first_two_same_color and (color_second == color_third)):
                self.part_of_three[line_id][column_id] += 1
                self.part_of_three[line_id-1][column_id] += 1
                self.part_of_three[line_id-2][column_id] += 1
            color_first = color_second
            color_second = color_third
            first_two_same_color = (color_first == color_second)

    def find_three(self):
        """Looks for clusters of three and writes its finding into part_of_three
        dict
        """
        self._find_horiz_three_all_lines()
        self._find_vert_three_all_lines()

    def _draw_grid_horiz_line(self, horiz_index):
        """Draws horizontal lines for game board

        Args:
            horiz_index(int): Number of the line; used for determining where \
            to draw the line
        """
        self.game_window.create_line(
            self.window_horiz_offset,
            self.height_interface + self.line_height*horiz_index,
            self.width_game_field+self.window_horiz_offset,
            self.height_interface+self.line_height*horiz_index,
            fill="black", width=3)

    def _draw_grid_vert_line(self, vert_index):
        """Draws vertical lines for game board

        Args:
            vert_index(int): Number of the line; used for determining where \
            to draw the line
        """
        self.game_window.create_line(
            self.window_horiz_offset+vert_index*self.column_width,
            self.height_interface,
            self.window_horiz_offset+vert_index*self.column_width,
            self.height_interface+self.height_game_field,
            fill="black", width=3)

    def draw_grid(self):
        """Draws grid for game board
        """
        for line_index in range(self.no_lines+1):
            self._draw_grid_horiz_line(line_index)
        for column_index in range(self.no_columns+1):
            self._draw_grid_vert_line(column_index)

    def __new__(cls, master_window, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            print("Creating new instance")
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance._set_interface_params(master_window)
            cls._instance.draw_grid()
        else:
            print("Returning already created instance")
        return cls._instance

if __name__ == "__main__":
    master = tkinter.Tk()
    master.title("Connect three")
    novyInterface = GameInterface(master)
    tkinter.mainloop()
