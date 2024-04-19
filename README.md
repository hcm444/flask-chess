Once I was close to finishing a Pygame version of chess, I failed to make it multiplayer. 

I took my "logic" from this Pygame version and created a Flask framework based version of the game.

White moves, then black. Turns cannot be taken out of sequence. Technically, since this updates on a website it is multiplayer.

Movements are handled over at chessboard.html and communicated to the backend.

This version of the game features:
  1. proper piece movements
  2. Proper "multiplayer" turns
  3. En passant captures
  4. Castling (move the king two squares right or left if no pieces between and the king or target rook has not moved)
  5. Check
  6. Limiting pieces to moves that would put the player in check and also moves that get the player out of check

Many optimizations could take place in this project. Once the chess logic is entirely complete, we hope to move it to other files 
and keep app.py focused on multiplayer implementation logic. Will add accounts, login, could probably sign up for an email service.

The goal of this project is an ad free Chess game. 
