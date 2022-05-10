import mpld3 from 'mpld3';

export default {
  name: 'VueMatplotlib',
  props: {
    name: {
      type: String,
      default: 'default',
    },
    spec: {
      type: Object,
    },
  },
  watch: {
    spec() {
      this.drawFigure(true);
    },
  },
  methods: {
    drawFigure(clearElem = false) {
      if (this.spec) {
        mpld3.draw_figure(this.name, this.spec, null, clearElem);
      } else {
        mpld3.remove_figure(this.name);
      }
    },
  },
  mounted() {
    if (this.spec) {
      this.drawFigure();
    }
  },
  beforeDestroy() {
    mpld3.remove_figure(this.name);
  },
};
