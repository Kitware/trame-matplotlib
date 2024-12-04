import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, client, matplotlib

from mpld3 import plugins, utils

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# Add d3 for JS code
server.enable_module(
    dict(scripts=["https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.js"])
)

# -----------------------------------------------------------------------------
# Chart examples from:
#   - http://jakevdp.github.io/blog/2013/12/19/a-d3-viewer-for-matplotlib/
# -----------------------------------------------------------------------------


class LinkedDragPlugin(plugins.PluginBase):
    JAVASCRIPT = r"""
    DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    DragPlugin.prototype.constructor = DragPlugin;
    DragPlugin.prototype.requiredProps = ["idpts", "idline", "idpatch"];
    DragPlugin.prototype.defaultProps = {}
    function DragPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    DragPlugin.prototype.draw = function(){
        var patchobj = mpld3.get_element(this.props.idpatch, this.fig);
        var ptsobj = mpld3.get_element(this.props.idpts, this.fig);
        var lineobj = mpld3.get_element(this.props.idline, this.fig);

        var drag = d3.drag()
            .subject(function(d) { return {x:ptsobj.ax.x(d[0]),
                                          y:ptsobj.ax.y(d[1])}; })
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);

        lineobj.path.attr("d", lineobj.datafunc(ptsobj.offsets));
        patchobj.path.attr("d", patchobj.datafunc(ptsobj.offsets,
                                                  patchobj.pathcodes));
        lineobj.data = ptsobj.offsets;
        patchobj.data = ptsobj.offsets;

        ptsobj.elements()
           .data(ptsobj.offsets)
           .style("cursor", "default")
           .call(drag);

        function dragstarted(d) {
          d3.event.sourceEvent.stopPropagation();
          d3.select(this).classed("dragging", true);
        }

        function dragged(d, i) {
          d[0] = ptsobj.ax.x.invert(d3.event.x);
          d[1] = ptsobj.ax.y.invert(d3.event.y);
          d3.select(this)
            .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
          lineobj.path.attr("d", lineobj.datafunc(ptsobj.offsets));
          patchobj.path.attr("d", patchobj.datafunc(ptsobj.offsets,
                                                    patchobj.pathcodes));
        }

        function dragended(d, i) {
          d3.select(this).classed("dragging", false);
        }
    }

    mpld3.register_plugin("drag", DragPlugin);
    """

    def __init__(self, points, line, patch):
        if isinstance(points, mpl.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {
            "type": "drag",
            "idpts": utils.get_id(points, suffix),
            "idline": utils.get_id(line),
            "idpatch": utils.get_id(patch),
        }


def figure_size():
    if state.figure_size is None:
        return {}

    dpi = state.figure_size.get("dpi")
    rect = state.figure_size.get("size")
    w_inch = rect.get("width") / dpi / 2
    h_inch = rect.get("height") / dpi / 2

    return {
        "figsize": (w_inch, h_inch),
        "dpi": dpi,
    }


def FirstDemo():
    fig, ax = plt.subplots(**figure_size())

    Path = mpath.Path
    path_data = [
        (Path.MOVETO, (1.58, -2.57)),
        (Path.CURVE4, (0.35, -1.1)),
        (Path.CURVE4, (-1.75, 2.0)),
        (Path.CURVE4, (0.375, 2.0)),
        (Path.LINETO, (0.85, 1.15)),
        (Path.CURVE4, (2.2, 3.2)),
        (Path.CURVE4, (3, 0.05)),
        (Path.CURVE4, (2.0, -0.5)),
        (Path.CLOSEPOLY, (1.58, -2.57)),
    ]
    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor="r", alpha=0.5)
    ax.add_patch(patch)

    # plot control points and connecting lines
    x, y = zip(*path.vertices[:-1])
    points = ax.plot(x, y, "go", ms=10)
    line = ax.plot(x, y, "-k")

    ax.grid(True, color="gray", alpha=0.5)
    ax.axis("equal")
    ax.set_title("Drag Points to Change Path", fontsize=18)

    plugins.connect(fig, LinkedDragPlugin(points[0], line[0], patch))

    return fig


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("active_figure", "figure_size")
def update_chart(active_figure, **kwargs):
    ctrl.update_figure(globals()[active_figure]())


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

state.trame__title = "Matplotly"

with SinglePageLayout(server) as layout:
    layout.title.set_text("trame ❤️ matplotlib")
    client.Script(LinkedDragPlugin.JAVASCRIPT)

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("active_figure", "FirstDemo"),
            items=(
                "figures",
                [
                    {"text": "First Demo", "value": "FirstDemo"},
                ],
            ),
            hide_details=True,
            dense=True,
        )

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            with client.SizeObserver("figure_size"):
                html_figure = matplotlib.Figure(style="position: absolute")
                ctrl.update_figure = html_figure.update

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
