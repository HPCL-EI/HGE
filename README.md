## Requirements
We only tested our code in the following enviroment:

* Ubuntu 16.04
* Anaconda3 5.2.0
* Python 3.6.5

### Installing GE
To use Grammar Evolution (GE), you need to:

```
cd ESI/PonyGE2
pip install -e .
```

## Plot behavior tree

```
(sudo) apt-get install python-pydot python-pydot-ng graphviz
```

Then visualize a BT for testing:

```
cd ESI/esi/bt/_test
python plot_BT.py
```

That will create bt.dot, bt.png and bt.svg in the outputs dir.

# License
This project is licensed under the Apache License - see the [LICENSE.md](LICENSE) file for details

# Acknowledgments

* Mesa team
* Aadesh Neupane
