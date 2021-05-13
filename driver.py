
"""
Driver for testing bloxorz algorithms

"""

from bloxorz_problem import BloxorzProblem
from bloxorz import Board
import searchGeneric
import searchBFS
import BFSMultiPruneSearcher
import os
import glob
from searchProblem import Arc, Search_problem
import io
import csv
import pandas as pd

if __name__ == "__main__":
    board_names = glob.glob("boards/*.blx")
    for board_name in board_names:
        print("Loading board file %s" % (board_name,))
        with open(board_name) as file:
            board = Board.read_board(file)
        bp0 = BloxorzProblem(board)
        bp0.heuristic = bp0.heuristic1

        bfsmulti_searcher = searchBFS.BFSMultiPruneSearcher(bp0)
        bfsmulti_result = bfsmulti_searcher.search()
        if bfsmulti_result is None:
            print("For board %s, found no solution using BFS with Multipruning!" % (board_name,))


        else:
            bfsmulti_sequence = [arc.action for arc in bfsmulti_result.arcs()]
            print("For board %s using our BFS with Multipruning, found solution with length %d using %d expansions" % (
                board_name, len(bfsmulti_sequence), bfsmulti_searcher.num_expanded))

        amulti_searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
        astarmulti_result = amulti_searcher.search()

        if astarmulti_result is None:
            print("For board %s, found no solution using A* with Multipruning!" % (board_name,))


        else:
            astarmulti_sequence = [arc.action for arc in astarmulti_result.arcs()]
            print(
                "For board %s using our A* with Multipruning, found solution with length %d using %d expansions" % (
                    board_name, len(astarmulti_sequence), amulti_searcher.num_expanded))

        astar_searcher = searchGeneric.AStarSearcher(bp0)
        astar_result = astar_searcher.search()
        if astar_result is None:
            print("For board %s, found no solution using A Star!" % (board_name,))

        else:
            astar_sequence = [arc.action for arc in astar_result.arcs()]
            print("For board %s using our A* algorithm, found solution with length %d using %d expansions" % (
            board_name, len(astar_sequence), astar_searcher.num_expanded))

    print(); print()







