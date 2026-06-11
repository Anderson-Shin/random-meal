(function () {
  "use strict";

  function spin(candidates, output, button, emptyMessage) {
    if (!candidates.length) {
      output.textContent = emptyMessage;
      return Promise.resolve(null);
    }

    button.disabled = true;
    output.classList.add("is-spinning");
    let ticks = 0;

    return new Promise((resolve) => {
      const timer = window.setInterval(() => {
        output.textContent = candidates[Math.floor(Math.random() * candidates.length)].name;
        ticks += 1;

        if (ticks >= 12) {
          window.clearInterval(timer);
          const winner = candidates[Math.floor(Math.random() * candidates.length)];
          output.textContent = winner.name;
          output.classList.remove("is-spinning");
          button.disabled = false;
          resolve(winner);
        }
      }, 110);
    });
  }

  window.RestaurantRoulette = { spin };
}());
