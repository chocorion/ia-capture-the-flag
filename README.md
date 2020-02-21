# IA CTF

Capture the Flag sandbox opposing AI teams

# Running

### Run examples

`./Game.py`

This starts a game with the default AI on both sides.

`make runExample`

This also starts a game with the default AI on both sides, but maybe you prefer using make. :)

`make runAstar`

This starts a game with two AIs using A*.

### Run your own AI :

The program can be started with :

`./Game.py <path_to_player1>`

or even :

`./Game.py <path_to_player1> <path_to_player2>`

When unspecified, the default AI will be selected for the missing parameter.

The path to your player is an import statement for your AI which has to implement domain.Player.

For example, if you create your own AI under `./ai/myAwesomeAI/player.py`, then test it with :

`./Game.py ai.myAwesomeAI.player`

Be careful : Your player's class must always be named 'myPlayer', and has to extend 'Player'.

## Testing

### Run Unit tests

`make tests`

### Visually

Use these default key bindings to toggle different Debug views :

- A : Toggle collision map preview for the default bots
- Z : Display the coordinates of the currently hovered block in the top left of the screen
