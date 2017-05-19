(function() {
  const API_ENDPOINT = '//fomoro-website.appspot.com/api/related-images';
  const IMAGE_ROOT = '//storage.googleapis.com/fomoro-website-related-images/thumbs';
  const MAX_RANGE = 1000;

  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  function fetchRelated(image_id) {
    const url = `${API_ENDPOINT}/${image_id}/sets/3`
    return fetch(url).then(res => res.json());
  }

  class App {
    constructor() {
      this.first_el = document.getElementById('first');
      this.result_els = document.getElementsByClassName('result');
      this.randomize_el = document.getElementById('randomize');

      this.randomize_el.setAttribute("data-id", getRandomInt(1, MAX_RANGE));
      this.randomize_el.addEventListener('click', this.getImages.bind(this, this.randomize_el));

      _.each(document.querySelectorAll('.section a'), (el, i) => {
        el.addEventListener('click', this.getImages.bind(this, el));
      })

      window.addEventListener('popstate', this.getPrevState.bind(this));
    }

    update(results) {
      this.randomize_el.setAttribute("data-id", getRandomInt(1, MAX_RANGE));
      _.each(_.flatten(results), (result, i) => {
        let result_el = this.result_els[i];
        result_el.setAttribute("data-id", result.id);
        result_el.setAttribute("src", `${IMAGE_ROOT}/${result.image}`);
      });
    }

    getPrevState(e) {
        e.preventDefault();
        this.update(e.state.images);
    }

    getImages(el, e) {
      e.preventDefault();

      let image_id = el.getAttribute("data-id");
      if (!image_id) {
        let img_el = el.getElementsByTagName('img')[0];
        image_id = img_el.getAttribute("data-id");
      }

      fetchRelated(image_id).then(data => {
        history.pushState({'images':data}, null, `/imagesearch/#/${image_id}`);
        this.update(data);
      });
    }

    start() {
      let image_id = parseInt(window.location.hash.split('/').pop());
      if (Number.isNaN(image_id) || image_id < 0 || image_id > MAX_RANGE) {
        image_id = getRandomInt(1, MAX_RANGE);
      }

      fetchRelated(image_id).then(data => {
        this.update(data);
      });
    }
  }

  const app = new App();
  app.start();
}).call(this);
