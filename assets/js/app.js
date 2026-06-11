(function () {
  "use strict";

  const translations = {
    en: {
      heroTitle: "Lunch decision, sorted.", heroSubtitle: "Filter a few options, pick at random, or let the roulette decide.", startButton: "Find food",
      stepOne: "Step 1", filtersHeading: "Narrow it down", districtLabel: "District", mealLabel: "Meal", cuisineLabel: "Cuisine", budgetLabel: "Budget", situationLabel: "Situation", speedLabel: "Speed", resetButton: "Reset filters",
      matchesLabel: "Current matches", resultsHeading: "Restaurant ideas", resultCount: "{count} matches", empty: "No restaurants match those filters. Try resetting a few choices.",
      quickChoiceLabel: "Quick choice", randomHeading: "Pick one for me", randomText: "One click, one answer from your current matches.", pickButton: "Pick For Me",
      makeItFunLabel: "Make it fun", rouletteHeading: "Spin the lunch roulette", rouletteText: "Watch the options shuffle before the winner lands.", spinButton: "Spin Roulette",
      exploreLabel: "Explore", districtsHeading: "Popular districts", districtComingSoon: "District page coming soon", footerText: "A simple, manually curated way to decide what to eat in Hong Kong.", recommended: "Recommended for",
      all: "All", lunch: "Lunch", dinner: "Dinner", solo: "Solo", friends: "Friends", date: "Date", family: "Family", teamLunch: "Team Lunch", quick: "Quick", normal: "Normal", relaxed: "Relaxed"
    },
    zhHant: {
      heroTitle: "午餐決定，搞定。", heroSubtitle: "篩選選項、隨機抽選，或交給輪盤決定。", startButton: "尋找美食",
      stepOne: "第一步", filtersHeading: "縮小選擇", districtLabel: "地區", mealLabel: "餐別", cuisineLabel: "菜式", budgetLabel: "預算", situationLabel: "場合", speedLabel: "速度", resetButton: "重設篩選",
      matchesLabel: "目前結果", resultsHeading: "餐廳靈感", resultCount: "{count} 個結果", empty: "沒有符合條件的餐廳，請重設部分篩選。",
      quickChoiceLabel: "快速選擇", randomHeading: "幫我選一間", randomText: "按一下，從目前結果中得到一個答案。", pickButton: "幫我選",
      makeItFunLabel: "有趣一點", rouletteHeading: "轉動午餐輪盤", rouletteText: "觀看選項跳動，等待結果揭曉。", spinButton: "轉動輪盤",
      exploreLabel: "探索", districtsHeading: "熱門地區", districtComingSoon: "地區頁面即將推出", footerText: "以簡單、人工整理的方式決定在香港吃甚麼。", recommended: "推薦場合",
      all: "全部", lunch: "午餐", dinner: "晚餐", solo: "獨食", friends: "朋友", date: "約會", family: "家庭", teamLunch: "團隊午餐", quick: "快速", normal: "一般", relaxed: "悠閒"
    },
    zhHans: {
      heroTitle: "午餐决定，搞定。", heroSubtitle: "筛选选项、随机抽选，或交给轮盘决定。", startButton: "寻找美食",
      stepOne: "第一步", filtersHeading: "缩小选择", districtLabel: "地区", mealLabel: "餐别", cuisineLabel: "菜式", budgetLabel: "预算", situationLabel: "场合", speedLabel: "速度", resetButton: "重置筛选",
      matchesLabel: "当前结果", resultsHeading: "餐厅灵感", resultCount: "{count} 个结果", empty: "没有符合条件的餐厅，请重置部分筛选。",
      quickChoiceLabel: "快速选择", randomHeading: "帮我选一家", randomText: "按一下，从当前结果中得到一个答案。", pickButton: "帮我选",
      makeItFunLabel: "有趣一点", rouletteHeading: "转动午餐轮盘", rouletteText: "观看选项跳动，等待结果揭晓。", spinButton: "转动轮盘",
      exploreLabel: "探索", districtsHeading: "热门地区", districtComingSoon: "地区页面即将推出", footerText: "以简单、人工整理的方式决定在香港吃什么。", recommended: "推荐场合",
      all: "全部", lunch: "午餐", dinner: "晚餐", solo: "单人", friends: "朋友", date: "约会", family: "家庭", teamLunch: "团队午餐", quick: "快速", normal: "一般", relaxed: "悠闲"
    }
  };

  const filterOptions = {
    district: ["All", "Quarry Bay", "Central", "Kwun Tong"],
    meal: ["All", "Lunch", "Dinner"],
    cuisine: ["All", "Japanese", "Chinese", "Korean", "Thai", "Indian", "Vietnamese", "Western", "Cafe", "Fast Food", "Noodles"],
    budget: ["All", "$", "$$", "$$$"],
    situation: ["All", "Solo", "Friends", "Date", "Family", "Team Lunch"],
    speed: ["All", "Quick", "Normal", "Relaxed"]
  };

  const state = { restaurants: [], filtered: [], language: "en" };
  const elements = {};

  function t(key) { return translations[state.language][key] || translations.en[key] || key; }
  function optionLabel(value) {
    const key = value === "Team Lunch" ? "teamLunch" : value.toLowerCase();
    return t(key) === key ? value : t(key);
  }

  function populateFilters() {
    Object.entries(filterOptions).forEach(([name, options]) => {
      const select = elements[name];
      const current = select.value;
      select.innerHTML = options.map((value) => `<option value="${value}">${optionLabel(value)}</option>`).join("");
      select.value = current || "All";
    });
  }

  function applyTranslations() {
    document.documentElement.lang = state.language === "en" ? "en" : state.language === "zhHant" ? "zh-Hant" : "zh-Hans";
    document.querySelectorAll("[data-i18n]").forEach((node) => { node.textContent = t(node.dataset.i18n); });
    populateFilters();
    renderRestaurants();
  }

  function restaurantMatches(restaurant) {
    return (elements.district.value === "All" || restaurant.area === elements.district.value)
      && (elements.meal.value === "All" || restaurant.mealTypes.includes(elements.meal.value.toLowerCase()))
      && (elements.cuisine.value === "All" || restaurant.cuisine === elements.cuisine.value)
      && (elements.budget.value === "All" || restaurant.budget === elements.budget.value)
      && (elements.situation.value === "All" || restaurant.situations.includes(elements.situation.value.toLowerCase()))
      && (elements.speed.value === "All" || restaurant.speed === elements.speed.value.toLowerCase());
  }

  function applyFilters() {
    state.filtered = state.restaurants.filter(restaurantMatches);
    renderRestaurants();
    elements.randomResult.textContent = "";
    elements.rouletteResult.textContent = "";
  }

  function renderRestaurants() {
    state.filtered = state.restaurants.filter(restaurantMatches);
    elements.resultCount.textContent = t("resultCount").replace("{count}", state.filtered.length);

    if (!state.filtered.length) {
      elements.results.innerHTML = `<p class="empty-state">${t("empty")}</p>`;
      return;
    }

    elements.results.innerHTML = state.filtered.map((restaurant) => `
      <article class="restaurant-card">
        <div class="restaurant-meta">${restaurant.area} · ${restaurant.cuisine} · ${restaurant.budget}</div>
        <h3>${restaurant.name}</h3>
        <ul class="tags">${restaurant.tags.map((tag) => `<li>${tag}</li>`).join("")}</ul>
        <p>${restaurant[`description_${state.language}`]}</p>
        <p class="recommended"><strong>${t("recommended")}:</strong> ${restaurant[`recommendedFor_${state.language}`]}</p>
      </article>
    `).join("");
  }

  function pickRandom() {
    if (!state.filtered.length) {
      elements.randomResult.textContent = t("empty");
      return;
    }
    elements.randomResult.textContent = state.filtered[Math.floor(Math.random() * state.filtered.length)].name;
  }

  function cacheElements() {
    ["district", "meal", "cuisine", "budget", "situation", "speed"].forEach((name) => { elements[name] = document.getElementById(`${name}-filter`); });
    elements.language = document.getElementById("language");
    elements.form = document.getElementById("filter-form");
    elements.results = document.getElementById("restaurant-results");
    elements.resultCount = document.getElementById("result-count");
    elements.randomButton = document.getElementById("random-button");
    elements.randomResult = document.getElementById("random-result");
    elements.rouletteButton = document.getElementById("roulette-button");
    elements.rouletteResult = document.getElementById("roulette-result");
  }

  async function init() {
    cacheElements();
    populateFilters();
    state.restaurants = await window.RestaurantData.loadRestaurants();
    state.filtered = state.restaurants.slice();

    elements.form.addEventListener("change", applyFilters);
    elements.form.addEventListener("reset", () => window.setTimeout(applyFilters));
    elements.language.addEventListener("change", (event) => { state.language = event.target.value; applyTranslations(); });
    elements.randomButton.addEventListener("click", pickRandom);
    elements.rouletteButton.addEventListener("click", () => window.RestaurantRoulette.spin(state.filtered, elements.rouletteResult, elements.rouletteButton, t("empty")));
    applyTranslations();
  }

  document.addEventListener("DOMContentLoaded", init);
}());
