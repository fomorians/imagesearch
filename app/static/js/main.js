(function() {
  const HTML_ENDPOINT = '/nearest'; //'https://babi-164320.appspot.com/predict';
  const API_ENDPOINT = '/api/nearest'; //'https://babi-164320.appspot.com/predict';
  const IMAGE_ROOT = '/images';
  const MAX_RANGE = 100;

  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  function fetchRelated(image_id) {
    const url = `${API_ENDPOINT}/${image_id}`
    return fetch(url).then(res => res.json());
  }

  class App {
    constructor() {
      this.first_el = document.getElementById('first');
      this.randomize_el = document.getElementById('randomize');
      this.result_els = document.getElementsByClassName('result');

      this.randomize_el.setAttribute("data-id", getRandomInt(1, MAX_RANGE));
      this.randomize_el.addEventListener('click', this.getImages.bind(this, this.randomize_el));
      window.addEventListener('popstate', this.getPrevState.bind(this));

      _.each(this.result_els, (result_el, i) => {
        result_el.addEventListener('click', this.getImages.bind(this, result_el));
      })
    }

    update(results) {
      const first = results.shift()
      this.first_el.setAttribute("src", `${IMAGE_ROOT}/${first.image}`);
      this.randomize_el.setAttribute("data-id", getRandomInt(1, MAX_RANGE));

      _.each(results, (result, i) => {
        const result_el = this.result_els[i];
        result_el.setAttribute("data-id", result.id);
        result_el.setAttribute("src", `${IMAGE_ROOT}/${result.image}`);
      });
    }

    getPrevState(e) {
        e.preventDefault();
        this.update(e.state.results);
    }

    getImages(el, e) {
      e.preventDefault();
      const image_id = el.getAttribute("data-id");
      fetchRelated(image_id).then(data => {
        history.pushState(data, null, `${HTML_ENDPOINT}/${image_id}`);
        this.update(data.results);
      });
    }

    start() {
      const image_id = getRandomInt(1, MAX_RANGE);
      fetchRelated(image_id).then(data => {
        this.update(data.results);
      });
    }
  }

  const app = new App();
}).call(this);
