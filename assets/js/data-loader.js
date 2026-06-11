(function () {
  "use strict";

  const fallbackRestaurants = [
    ["quarry-bay-japanese-001", "Harbour Bento", "Quarry Bay", "Eastern Hong Kong", "Japanese", "$$", ["lunch", "dinner"], ["solo", "team lunch"], "quick", ["bento", "office friendly"], "A straightforward bento stop for a quick weekday meal.", "適合平日快速用餐的簡單便當選擇。", "适合工作日快速用餐的简便便当选择。", "Quick solo lunch or an easy team order.", "快速獨食午餐或簡單團隊訂餐。", "快速单人午餐或简单团队订餐。"],
    ["quarry-bay-chinese-002", "Steam & Rice", "Quarry Bay", "Eastern Hong Kong", "Chinese", "$", ["lunch", "dinner"], ["solo", "friends"], "quick", ["rice bowls", "casual"], "A casual rice-bowl option built for busy lunch breaks.", "為忙碌午休而設的輕鬆飯碗選擇。", "为忙碌午休设计的轻松饭碗选择。", "A fast meal when time matters.", "適合時間緊迫時快速用餐。", "适合时间紧迫时快速用餐。"],
    ["quarry-bay-cafe-003", "Desk Break Cafe", "Quarry Bay", "Eastern Hong Kong", "Cafe", "$$", ["lunch"], ["solo", "friends", "team lunch"], "normal", ["sandwiches", "coffee"], "A bright cafe placeholder for sandwiches and a calmer lunch.", "明亮的咖啡店，適合三文治和悠閒午餐。", "明亮的咖啡店，适合三明治和悠闲午餐。", "Coffee chats or a relaxed desk break.", "咖啡聊天或悠閒午休。", "咖啡聊天或悠闲午休。"],
    ["central-western-001", "Midday Table", "Central", "Central and Western Hong Kong", "Western", "$$$", ["lunch", "dinner"], ["date", "friends"], "relaxed", ["sit-down", "sharing"], "A relaxed Western-style placeholder for an unhurried meal.", "適合悠閒用餐的西式餐廳示例。", "适合悠闲用餐的西式餐厅示例。", "A longer lunch, dinner date, or catch-up.", "較長午餐、晚餐約會或聚會。", "较长午餐、晚餐约会或聚会。"],
    ["central-noodles-002", "Noodle Minute", "Central", "Central and Western Hong Kong", "Noodles", "$", ["lunch", "dinner"], ["solo", "team lunch"], "quick", ["noodles", "fast"], "A no-fuss noodle stop for a speedy Central meal.", "中環快速用餐的簡單麵食選擇。", "中环快速用餐的简单面食选择。", "Solo diners and teams short on time.", "適合獨食及時間有限的團隊。", "适合单人及时间有限的团队。"],
    ["central-thai-003", "Lime Lunchroom", "Central", "Central and Western Hong Kong", "Thai", "$$", ["lunch", "dinner"], ["friends", "team lunch"], "normal", ["sharing", "bright flavours"], "A friendly Thai placeholder with easy dishes for sharing.", "友善的泰式餐廳示例，適合分享菜式。", "友好的泰式餐厅示例，适合分享菜肴。", "Casual group lunches and after-work dinners.", "輕鬆團隊午餐及下班晚餐。", "轻松团队午餐及下班晚餐。"],
    ["kwun-tong-korean-001", "Seoul Workbench", "Kwun Tong", "Kwun Tong Hong Kong", "Korean", "$$", ["lunch", "dinner"], ["friends", "team lunch"], "normal", ["group meal", "comfort food"], "A casual Korean placeholder suited to small office groups.", "適合小型辦公室團隊的休閒韓式餐廳示例。", "适合小型办公室团队的休闲韩式餐厅示例。", "Team lunches and casual dinners with friends.", "團隊午餐及朋友輕鬆晚餐。", "团队午餐及朋友轻松晚餐。"],
    ["kwun-tong-fast-food-002", "Quick Corner", "Kwun Tong", "Kwun Tong Hong Kong", "Fast Food", "$", ["lunch", "dinner"], ["solo"], "quick", ["grab and go", "budget"], "A budget-friendly placeholder for a fast grab-and-go meal.", "價格親民、適合快速外帶的餐廳示例。", "价格亲民、适合快速外带的餐厅示例。", "A quick solo meal between meetings.", "會議之間的快速獨食。", "会议之间的快速单人餐。"],
    ["kwun-tong-chinese-003", "Neighbourhood Wok", "Kwun Tong", "Kwun Tong Hong Kong", "Chinese", "$$", ["lunch", "dinner"], ["friends", "team lunch"], "relaxed", ["sharing", "local style"], "A comfortable Chinese dining placeholder for shared plates.", "舒適的中式餐廳示例，適合分享菜式。", "舒适的中式餐厅示例，适合分享菜肴。", "A relaxed team meal or dinner with friends.", "悠閒團隊用餐或朋友晚餐。", "悠闲团队用餐或朋友晚餐。"]
  ].map(toRestaurant);

  function toRestaurant(item) {
    return {
      id: item[0], name: item[1], area: item[2], district: item[3], cuisine: item[4], budget: item[5],
      mealTypes: item[6], situations: item[7], speed: item[8], tags: item[9],
      description_en: item[10], description_zhHant: item[11], description_zhHans: item[12],
      recommendedFor_en: item[13], recommendedFor_zhHant: item[14], recommendedFor_zhHans: item[15],
      sourceNote: "Manually written placeholder. No reviews, ratings, photos, or menu text copied."
    };
  }

  async function loadRestaurants() {
    try {
      const response = await fetch("assets/data/restaurants.json");
      if (!response.ok) throw new Error("Restaurant data request failed.");
      return await response.json();
    } catch (error) {
      console.info("Using embedded placeholder data because the JSON file could not be loaded.", error);
      return fallbackRestaurants;
    }
  }

  window.RestaurantData = { loadRestaurants };
}());
