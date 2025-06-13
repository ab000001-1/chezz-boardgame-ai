## Chezz AI Move Generator

#### Overview

This project implements a program to compute all valid moves for a given board state in Chezz, a chess variant. 
The program reads a board configuration from standard input and generates output files (board.000, board.001, etc.) 
representing all possible next board states based on Chezz rules.

## Chezz Rules
## Chezz is played on an 8x8 checkered board with unique pieces:

#### Flinger (F): Moves like a king (1 square, 8 directions) but cannot capture. Can fling an adjacent friendly piece in the same direction, landing on an empty square or capturing an enemy (except King), destroying the flung piece.

#### Peon (P): Moves like a chess pawn (1 square forward, captures diagonally, no en passant, promotes to Zombie at board's end).

#### Knight (N), Queen (Q), King (K), Bishop (B), Rook (R): Move and capture as in chess (no castling for King).

#### Cannon (C): Moves 1 square (up, down, left, right), cannot capture. Fires diagonally, removing all pieces (friend or foe) along the path.

#### Zombie (Z): Moves 1 square (up, down, left, right), captures by moving onto enemy pieces.

#### Contagion: After a move, enemy pieces (except King/Zombie) adjacent to a player's Zombies (4 directions) turn into that player's Zombies.

#### Endgame: Game ends when a King is captured.

## Input/Output

#### Input: A board file (e.g., board.txt) with:

#### First line: Player turn (w or b) and 3 integers.

#### Board section: JSON-like format with piece positions (e.g., a1: 'wF').

#### Last 3 lines: Reserved integers.

## Output: Files (board.000, board.001, etc.) in the same format, each representing a valid board after a legal move.

## Usage

#### Place a board file (e.g., board.txt) in the project directory.

#### Run the compile script: ./compile

#### Execute the program: ./a3 < board.txt

#### Check generated board files for all possible moves.

