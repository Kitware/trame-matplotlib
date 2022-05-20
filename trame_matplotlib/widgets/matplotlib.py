from trame_client.widgets.core import AbstractElement
from trame_matplotlib import module


try:
    import mpld3
except:
    print(
        "\nmpld3 is missing, if you want your matplotlib figure to work install it\n   $ pip install mpld3\n"
    )

try:
    from trame_client.encoders.numpy import encode

    has_numpy = True
except ImportError:
    has_numpy = False


def no_encoding(_data):
    return _data


ENCODER = encode if has_numpy else no_encoding


class Figure(AbstractElement):
    """
    Create a matplotlib figure viewer element

    :param figure: Matplotlib figure to show (default: None)

    >>> component1 = Figure(figure=fig1)
    >>> component2 = Figure()
    >>> component2.update(fig1)
    """
    _next_id = 0

    def __init__(self, figure=None, **kwargs):
        Figure._next_id += 1
        self._key = f"trame__matplotlib_{Figure._next_id}"

        super().__init__("vue-matplotlib", **kwargs)
        if self.server:
            self.server.enable_module(module)

        self._attributes["name"] = f'name="{self._key}"'
        self._attributes["spec"] = f':spec="{self._key}"'
        self._figure = figure
        self.update()

    def update(self, figure=None, **kwargs):
        """
        Update the figure to show.

        :param figure: Matplotlib figure object
        """
        if figure:
            self._figure = figure

        if self._figure:
            self.server.state[self._key] = ENCODER(mpld3.fig_to_dict(self._figure))

    @property
    def key(self):
        """Return the name of the state variable used internally"""
        return self._key

    @staticmethod
    def to_data(chart, **kwargs):
        """
        Serialize matplotlib figure
        """
        return ENCODER(mpld3.fig_to_dict(chart))
