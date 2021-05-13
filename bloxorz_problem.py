##############################################################################
#
# File:         bloxorz_problem.py
# Date:         Wed 31 Aug 2011  11:40
# Author:       Ken Basye
# Description:  Bloxorz search problem
#
##############################################################################

import cs210_utils
from searchProblem import Arc, Search_problem
import searchGeneric
import searchBFS

# import searchBranchAndBound
import io
from bloxorz import Board, next_position


class BloxorzProblem(Search_problem):
    """
    >>> board_string = (
    ... '''BLOX 1
    ... 5 3
    ... X X X O O
    ... S X G X O
    ... W W W W X
    ... ''')

    >>> fake_file = io.StringIO(board_string)
    >>> board0 = Board.read_board(fake_file)
    >>> bp0 = BloxorzProblem(board0)
    >>> bp0.start
    ((0, 1), (0, 1))

    >>> searcher = searchBFS.BFSSearcher(bp0)
    >>> path = searcher.search()
    2507 paths have been expanded and 2399 paths remain in the frontier

    >>> path
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> a_pos, b_pos = path.end()
    >>> a_pos == b_pos == board0.goal
    True

    >>> searcher = searchBFS.BFSMultiPruneSearcher(bp0)
    >>> path = searcher.search()
    16 paths have been expanded and 1 paths remain in the frontier

    >>> path
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()
    1259 paths have been expanded and 1880 paths remain in the frontier

    >>> path
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))


    >>> bp0.heuristic = bp0.heuristic1
    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()
    845 paths have been expanded and 1369 paths remain in the frontier

    >>> path
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> bp0.heuristic = bp0.heuristic1
    >>> searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
    >>> path = searcher.search()
    15 paths have been expanded and 1 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

"""

    def __init__(self, board):
        """
        Build a problem instance from a board
        """
        self.board = board
        self.start = (board.start, board.start)
        self.goal = (board.goal, board.goal)

    def start_node(self):
        """Returns start node"""
        return self.start

    def is_goal(self, node):
        """Returns True if node is a goal"""
        return node == self.goal

    def neighbors(self,node):
        """
        Given a node, return a sequence of Arcs usable
        from this node. 
        """
        ACTIONS = tuple(('U', 'D', 'L', 'R'))
        lst = []
        for action in ACTIONS:
            next_pos = next_position(node, action)
            if Board.legal_position(self.board, next_pos):
                lst.append(Arc(node, next_pos, 1, action))
        return lst


    def heuristic (self, node):
        return 0

    def heuristic1(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""

        pos1, pos2 = node
        ((ax, ay), (ax2, ay2)) = pos1, pos2
        pos = self.goal
        (gx, gy) = pos[0]
        dx = abs(ax - gx)
        dy = abs(ay - gy)
        dx2 = abs(ax2 - gy)
        dy2 = abs(ay2 - gy)
        if dx +dy > dx2+dy2:
            dist = dx + dy
            li = dx2 + dy2
        else:
            dist = dx2 + dy2
            li = dx + dy
        D = (li)/1.5
        h = D * (dist)
        return h



if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()

