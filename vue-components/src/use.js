import mpld3 from 'mpld3';
import components from './components';

export function install(Vue) {
  Object.keys(components).forEach((name) => {
    Vue.component(name, components[name]);
  });

  // Expose mpld3 globaly
  window.mpld3 = mpld3;
}
