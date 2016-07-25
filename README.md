# Cheshire Bot
An experimental chess engine coded from scratch as a test ground for AI stuff.
Required Python libs:
* numpy
* PyOpenCL
* PyQt4
* more to come as the project progresses....

To run, simply execute `test_qt.py` or for gui-less operation, there are a bunch of `main1,2,3()` functions in `test_cl.py` you could rename to `main()`.

Currently the engine only supports the exhaustive search of all legal moves (caveat: promotion is always to a queen, I will have to re-write quite a bit of code to offer the player the choice of pieces), so you can start the qt gui and play a nice match of chess against yourself, and you should be able to play just about any legal chess match. For added help, when you click a field, you can display all legal moves from that position, or if you undo the field selection, you can print all legal moves for every piece to stdout.

Coming soon:
* evaluation function of a move
* pruned tree search

Coming not so soon:
* reinforcement learning
