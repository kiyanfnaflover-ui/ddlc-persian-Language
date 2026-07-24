const BOT_TOKEN = "8310735571:AAGqGX1Vfh6JKaKgD_H_lObELAq1vCi99J8";
const API_KEY = "d1bd196c8c335e9f5607d042b65bc97bfaedb1e0ba97ba02137b98b3c3421fdf85447db827af7e36b0e961acc8fe649c4d933a42df7e60b486b07c4e71e4bc2f";
const USER_ID = "6357308";

const SOURCE_API = 'api'; const SOURCE_WORLD = 'world'; const SOURCE_BOTH = 'both';

const CHARACTER_POOL = [
  "raiden_shogun", "ganyu", "hu_tao", "keqing", "eula_(genshin_impact)", "furina_(genshin_impact)",
  "clorinde", "navia_(genshin_impact)", "nilou_(genshin_impact)", "yelan_(genshin_impact)",
  "mona_(genshin_impact)", "kamisato_ayaka", "fischl_(genshin_impact)", "jean_(genshin_impact)",
  "kafka_(honkai_star_rail)", "march_7th", "firefly_(honkai_star_rail)", "ruan_mei_(honkai_star_rail)",
  "acheron_(honkai_star_rail)", "black_swan_(honkai_star_rail)", "sparkle_(honkai_star_rail)", "tingyun_(honkai_star_rail)",
  "ellen_joe", "nicole_demara", "anby_demara", "grace_howard", "zhu_yuan",
  "alice_(nikke)", "rapi_(nikke)", "anis_(nikke)", "viper_(nikke)",
  "shiroko_(blue_archive)", "asuna_(blue_archive)", "karin_(blue_archive)", "toki_(blue_archive)",
  "hatsune_miku", "sakura_haruno", "hyuuga_hinata", "tifa_lockhart", "yorha_2b", "ahri", "lucina",
  "makima", "power_(chainsaw_man)", "reze_(chainsaw_man)", "yor_forger", "marin_kitagawa",
  "zero_two_(darling_in_the_franxx)", "asuka_langley", "rei_ayanami", "rem_(re_zero)",
  "emilia_(re_zero)", "aqua_(konosuba)", "megumin", "chika_fujiwara", "kaguya_shinomiya",
  "saber_(fate)", "tousaka_rin", "kurumi_tokisaki", "nezuko_kamado", "kochou_shinobu",
  "mitsuri_kanroji", "nami_(one_piece)", "nico_robin", "boa_hancock", "esdeath",
  "lucy_(cyberpunk)", "rebecca_(cyberpunk)", "jinx_(league_of_legends)",
  "marnie_(pokemon)", "lillie_(pokemon)", "serena_(pokemon)", "pyra_(xenoblade)",
  "mythra_(xenoblade)", "yumeko_jabami", "albedo_(overlord)", "rory_mercury",
  "frieren", "fern_(frieren)", "yor_briar", "cyberpunk_edgerunners"
];

const userPrefs = {};

const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.142 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
];

function rotateHeaders(customReferer) {
  const ua = USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
  const headers = {
    'User-Agent': ua,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
  };
  if (customReferer) headers['Referer'] = customReferer;
  return headers;
}

addEventListener('fetch', event => {
  if (event.request.method === "POST") {
    event.respondWith(handleWebhook(event.request));
  } else {
    event.respondWith(new Response("Expected POST request", { status: 400 }));
  }
});

function getUserPref(chatId) {
  return userPrefs[chatId] || { mode: 'photo', source: SOURCE_BOTH };
}

function setUserPref(chatId, prefs) {
  userPrefs[chatId] = { ...getUserPref(chatId), ...prefs };
}

async function handleWebhook(request) {
  try {
    const update = await request.json();
    if (update.callback_query) {
      await handleCallbackQuery(update.callback_query);
      return new Response("OK", { status: 200 });
    }
    if (update.message && update.message.text) {
      const chatId = update.message.chat.id;
      const text = update.message.text.trim();
      const lowerText = text.toLowerCase();

      if (lowerText === '/start') { delete userPrefs[chatId]; await sendMainMenu(chatId); return new Response("OK", { status: 200 }); }
      if (lowerText === '/about' || lowerText === '/abaut') { await sendAboutInfo(chatId); return new Response("OK", { status: 200 }); }

      if (lowerText.startsWith('/video ')) { setUserPref(chatId, { source: SOURCE_BOTH }); await processMediaRequest(chatId, text.substring(7).trim(), 'video', SOURCE_BOTH); }
      else if (lowerText.startsWith('/gif ')) { setUserPref(chatId, { source: SOURCE_BOTH }); await processMediaRequest(chatId, text.substring(5).trim(), 'gif', SOURCE_BOTH); }
      else if (lowerText.startsWith('/photo ')) { setUserPref(chatId, { source: SOURCE_BOTH }); await processMediaRequest(chatId, text.substring(7).trim(), 'photo', SOURCE_BOTH); }
      else if (lowerText.startsWith('/search ')) { setUserPref(chatId, { source: SOURCE_BOTH }); await processMediaRequest(chatId, text.substring(8).trim(), 'photo', SOURCE_BOTH); }
      else if (!lowerText.startsWith('/')) {
        const pref = getUserPref(chatId);
        let mode = pref.mode;
        let source = pref.source;
        if (update.message.reply_to_message && update.message.reply_to_message.text) {
          const rt = update.message.reply_to_message.text;
          if (rt.includes("VIDEO")) mode = 'video'; else if (rt.includes("GIF")) mode = 'gif';
          if (rt.includes("SRC=api")) source = SOURCE_API; else if (rt.includes("SRC=world")) source = SOURCE_WORLD; else if (rt.includes("SRC=both")) source = SOURCE_BOTH;
        }
        await processMediaRequest(chatId, text, mode, source);
      }
    }
    return new Response("OK", { status: 200 });
  } catch (error) {
    console.error("Webhook Error:", error.message);
    return new Response("OK", { status: 200 });
  }
}

async function handleCallbackQuery(cb) {
  const chatId = cb.message.chat.id;
  const data = cb.data;
  const msgId = cb.message.message_id;
  await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/answerCallbackQuery`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ callback_query_id: cb.id })
  });

  if (data === "menu_photo") { setUserPref(chatId, { mode: 'photo', source: SOURCE_BOTH }); await sendForceReply(chatId, "PHOTO [SRC=both]", "🖼 عکس (۲۰ تا) - ترکیبی"); }
  else if (data === "menu_video") { setUserPref(chatId, { mode: 'video', source: SOURCE_BOTH }); await sendForceReply(chatId, "VIDEO [SRC=both]", "🎥 ویدیو (۵ تا) - ترکیبی"); }
  else if (data === "menu_gif") { setUserPref(chatId, { mode: 'gif', source: SOURCE_BOTH }); await sendForceReply(chatId, "GIF [SRC=both]", "🎞 گیف (۱۰ تا) - ترکیبی"); }
  else if (data === "menu_about") { await sendAboutInfo(chatId); }
  else if (data === "source_api") { setUserPref(chatId, { source: SOURCE_API }); await sendForceReply(chatId, "PHOTO [SRC=api]", "🔵 فقط API (rule34.xxx)"); }
  else if (data === "source_world") { setUserPref(chatId, { source: SOURCE_WORLD }); await sendForceReply(chatId, "PHOTO [SRC=world]", "🟢 فقط World (rule34.world)"); }
  else if (data === "source_both") { setUserPref(chatId, { source: SOURCE_BOTH }); await sendForceReply(chatId, "PHOTO [SRC=both]", "🟣 ترکیبی (API+World)"); }
  else if (data === "menu_tags") {
    const randomTags = shuffleArray([...CHARACTER_POOL]).slice(0, 6);
    const keyboard = [];
    for (let i = 0; i < randomTags.length; i += 2) {
      const row = [{ text: randomTags[i].replace(/_/g, ' '), callback_data: `search_${randomTags[i]}` }];
      if (randomTags[i + 1]) row.push({ text: randomTags[i + 1].replace(/_/g, ' '), callback_data: `search_${randomTags[i + 1]}` });
      keyboard.push(row);
    }
    keyboard.push([{ text: "🔙 بازگشت به منو", callback_data: "menu_main" }]);
    await sendTelegramMessage('editMessageText', { chat_id: chatId, message_id: msgId, text: "🌟 **تگ‌های پیشنهادی:**\nیک شخصیت را انتخاب کنید:", parse_mode: "Markdown", reply_markup: { inline_keyboard: keyboard } });
  }
  else if (data === "menu_main") { await sendTelegramMessage('editMessageText', { chat_id: chatId, message_id: msgId, text: getMainMenuText(), parse_mode: "Markdown", reply_markup: { inline_keyboard: getMainMenuKeyboard() } }); }
  else if (data.startsWith("search_")) { setUserPref(chatId, { mode: 'photo', source: SOURCE_BOTH }); await processMediaRequest(chatId, data.replace("search_", ""), 'photo', SOURCE_BOTH); }
}

async function sendForceReply(chatId, marker, label) {
  await sendTelegramMessage('sendMessage', {
    chat_id: chatId,
    text: `**[${marker}]** ${label}\nنام شخصیت را بنویسید:`,
    parse_mode: "Markdown",
    reply_markup: { force_reply: true, selective: true }
  });
}

function getMainMenuText() { return "👋 *به ربات خوش آمدید!*\n\n🔹 ۵۰٪ از API rule34.xxx\n🔹 ۵۰٪ از Web Scraping rule34.world\n\n👇 گزینه مورد نظر را انتخاب کنید:"; }

function getMainMenuKeyboard() {
  return [
    [{ text: "🖼 عکس (۲۰ تا)", callback_data: "menu_photo" }],
    [{ text: "🎥 ویدیو (۵ تا)", callback_data: "menu_video" }, { text: "🎞 گیف (۱۰ تا)", callback_data: "menu_gif" }],
    [{ text: "🌟 تگ‌های پیشنهادی", callback_data: "menu_tags" }],
    [{ text: "🔵 فقط API", callback_data: "source_api" }, { text: "🟢 فقط World", callback_data: "source_world" }],
    [{ text: "🟣 ترکیبی", callback_data: "source_both" }],
    [{ text: "ℹ️ درباره ربات", callback_data: "menu_about" }]
  ];
}

async function sendMainMenu(chatId) { await sendTelegramMessage('sendMessage', { chat_id: chatId, text: getMainMenuText(), parse_mode: "Markdown", reply_markup: { inline_keyboard: getMainMenuKeyboard() } }); }

async function sendAboutInfo(chatId) {
  await sendTelegramMessage('sendMessage', {
    chat_id: chatId,
    text: "🤖 *درباره ربات:*\n\n🔹 منبع ۱: **API Rule34.xxx** (رسمی)\n🔹 منبع ۲: **Web Scraping Rule34.world**\n🔹 حالت پیش‌فرض: **ترکیبی ۵۰-۵۰**\n\nمی‌توانید از دکمه‌های منبع در منو، منبع دلخواه را انتخاب کنید.\n\nتوسعه یافته توسط: K_F_",
    parse_mode: "Markdown"
  });
}

async function processMediaRequest(chatId, tags, type, source) {
  if (!tags || tags.trim() === "") return sendTelegramMessage('sendMessage', { chat_id: chatId, text: "⚠️ لطفاً یک نام معتبر به انگلیسی وارد کنید." });
  let count = type === 'video' ? 5 : type === 'gif' ? 10 : 20;
  let typeName = type === 'video' ? 'ویدیو' : type === 'gif' ? 'گیف' : 'عکس';
  let sourceLabel = source === SOURCE_API ? '(API)' : source === SOURCE_WORLD ? '(World)' : '(API+World)';
  const statusMsg = await sendTelegramMessage('sendMessage', { chat_id: chatId, text: `🔍 جستجوی ${typeName} ${sourceLabel} برای '${tags}'...`, parse_mode: "Markdown" });
  const results = await fetchSmartMedia(tags, type, count, source);
  if (results.length === 0) {
    if (statusMsg && statusMsg.ok && statusMsg.result) await sendTelegramMessage('deleteMessage', { chat_id: chatId, message_id: statusMsg.result.message_id });
    await sendTelegramMessage('sendMessage', { chat_id: chatId, text: `❌ محتوایی برای '${tags}' یافت نشد.`, reply_markup: { inline_keyboard: getMainMenuKeyboard() } });
    return;
  }
  try {
    if (type === 'photo') {
      const chunks = [];
      for (let i = 0; i < results.length; i += 10) chunks.push(results.slice(i, i + 10));
      for (const chunk of chunks) {
        const mediaGroup = chunk.map(url => ({ type: 'photo', media: url }));
        const sendRes = await sendTelegramMessage('sendMediaGroup', { chat_id: chatId, media: mediaGroup });
        if (!sendRes || !sendRes.ok) { for (const url of chunk) { await sendTelegramMessage('sendPhoto', { chat_id: chatId, photo: url }); await sleep(200); } }
        await sleep(1000);
      }
    } else {
      const method = type === 'video' ? 'sendVideo' : 'sendAnimation';
      for (const url of results) { await sendTelegramMessage(method, { chat_id: chatId, [type === 'video' ? 'video' : 'animation']: url }); await sleep(500); }
    }
  } catch (e) { console.error("Error sending media:", e.message); }
  if (statusMsg && statusMsg.ok && statusMsg.result) await sendTelegramMessage('deleteMessage', { chat_id: chatId, message_id: statusMsg.result.message_id });
  await sendTelegramMessage('sendMessage', { chat_id: chatId, text: `✨ ارسال **${typeName}** از **${sourceLabel}** پایان یافت!\n\n👇 برای جستجوی بعدی:`, parse_mode: "Markdown", reply_markup: { inline_keyboard: getMainMenuKeyboard() } });
}

async function fetchSmartMedia(rawTag, type, requiredCount, source) {
  let primaryTag = optimizeTags(rawTag);
  if (source === SOURCE_API) return (await fetchFromAPI(primaryTag, type, requiredCount)).slice(0, requiredCount);
  if (source === SOURCE_WORLD) return (await fetchFromWorld(primaryTag, type, requiredCount)).slice(0, requiredCount);
  const apiTarget = Math.ceil(requiredCount / 2);
  const worldTarget = requiredCount - apiTarget;
  let [apiRes, worldRes] = await Promise.all([fetchFromAPI(primaryTag, type, requiredCount), fetchFromWorld(primaryTag, type, requiredCount)]);
  let final = [...apiRes.slice(0, apiTarget), ...worldRes.slice(0, worldTarget)];
  let remaining = requiredCount - final.length;
  if (remaining > 0) { let extras = [...apiRes.slice(apiTarget), ...worldRes.slice(worldTarget)]; final = [...final, ...extras.slice(0, remaining)]; }
  return shuffleArray(final);
}

async function fetchFromAPI(tagStr, type, maxCount) {
  let r34Tags = tagStr;
  if (type === 'video') r34Tags += " video"; if (type === 'gif') r34Tags += " gif"; if (type === 'photo') r34Tags += " -video -gif";
  let tempMedia = []; const seenUrls = new Set();
  const getPage = async (page) => {
    const url = `https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&tags=${encodeURIComponent(r34Tags)}&pid=${page}&limit=100&api_key=${API_KEY}&user_id=${USER_ID}`;
    try {
      const res = await fetch(url, { headers: { 'User-Agent': rotateHeaders()['User-Agent'] } });
      if (!res.ok) return; const data = await res.json();
      if (Array.isArray(data)) { for (const item of data) { let fileUrl = item.file_url || item.sample_url; if (!fileUrl) continue; if (fileUrl.startsWith('//')) fileUrl = 'https:' + fileUrl; const lowUrl = fileUrl.toLowerCase(); if (type === 'video' && !lowUrl.endsWith('.mp4')) continue; if (type === 'gif' && !lowUrl.endsWith('.gif')) continue; if (type === 'photo' && (lowUrl.endsWith('.mp4') || lowUrl.endsWith('.webm') || lowUrl.endsWith('.gif'))) continue; if (!seenUrls.has(fileUrl)) { seenUrls.add(fileUrl); tempMedia.push(fileUrl); } } }
    } catch (e) { }
  };
  let randomPage = Math.floor(Math.random() * 3); await getPage(randomPage);
  if (tempMedia.length < maxCount && randomPage !== 0) await getPage(0);
  return shuffleArray(tempMedia);
}

async function fetchFromWorld(tagStr, type, maxCount) {
  let scrapeTags = tagStr;
  if (type === 'video') scrapeTags += " video";
  if (type === 'gif') scrapeTags += " gif";
  if (type === 'photo') scrapeTags += " -video -gif";
  const encodedQuery = encodeURIComponent(scrapeTags);
  let tempMedia = [];
  const seenUrls = new Set();

  // Strategy 1: Try the SSR search page with correct Accept-Encoding
  try {
    const searchUrl = `https://rule34.world/?tags=${encodedQuery}`;
    const headers = rotateHeaders('https://rule34.world/');
    headers['Accept'] = 'application/json, text/html, */*';
    const res = await fetch(searchUrl, { headers });
    if (res.ok) {
      const html = await res.text();
      if (html.length > 1000) {
        // Extract post IDs from og:url meta tags or Angular state
        const postIdRegex = /rule34\.world\/post\/(\d+)/g;
        let m;
        const postIds = [];
        while ((m = postIdRegex.exec(html)) !== null) {
          postIds.push(parseInt(m[1]));
        }
        // Also try to extract from the ng-state JSON
        const ngStateMatch = html.match(/<script id="ng-state"[^>]*>([\s\S]*?)<\/script>/);
        if (ngStateMatch) {
          try {
            const ngState = JSON.parse(ngStateMatch[1]);
            for (const key of Object.keys(ngState)) {
              if (key.startsWith('get:/api/v2/post/')) {
                const postData = ngState[key];
                if (postData && postData.id) {
                  postIds.push(postData.id);
                }
              }
            }
          } catch (e) {}
        }

        // Deduplicate
        const uniqueIds = [...new Set(postIds)];
        for (const postId of uniqueIds) {
          if (tempMedia.length >= maxCount) break;
          // Construct the full-res URL using the folder pattern: folder = Math.floor(postId / 1000)
          const folder = Math.floor(postId / 1000);
          const imageUrl = `https://rule34.world/posts/${folder}/${postId}/${postId}.jpg`;
          const lowUrl = imageUrl.toLowerCase();
          if (type === 'video' && !lowUrl.endsWith('.mp4')) continue;
          if (type === 'gif' && !lowUrl.endsWith('.gif')) continue;
          if (type === 'photo' && (lowUrl.endsWith('.mp4') || lowUrl.endsWith('.webm') || lowUrl.endsWith('.gif'))) continue;
          if (!seenUrls.has(imageUrl)) {
            seenUrls.add(imageUrl);
            tempMedia.push(imageUrl);
          }
        }
      }
    }
  } catch (e) {
    console.error("World search page error:", e.message);
  }

  // Strategy 2: Try the internal API directly (bypasses Cloudflare WAF for SPA routes)
  if (tempMedia.length < maxCount) {
    try {
      const apiUrl = `https://rule34.world/api/v2/search?tags=${encodedQuery}&limit=${maxCount * 2}`;
      const headers = rotateHeaders('https://rule34.world/');
      headers['Accept'] = 'application/json, text/html, */*';
      headers['Referer'] = 'https://rule34.world/';
      const res = await fetch(apiUrl, { headers });
      if (res.ok) {
        const contentType = res.headers.get('content-type') || '';
        if (contentType.includes('json')) {
          const data = await res.json();
          if (Array.isArray(data)) {
            for (const item of data) {
              if (tempMedia.length >= maxCount) break;
              const postId = item.id;
              if (!postId) continue;
              const folder = Math.floor(postId / 1000);
              let imageUrl = item.file_url || item.sample_url || `https://rule34.world/posts/${folder}/${postId}/${postId}.jpg`;
              if (imageUrl.startsWith('//')) imageUrl = 'https:' + imageUrl;
              if (imageUrl.startsWith('/')) imageUrl = 'https://rule34.world' + imageUrl;
              const lowUrl = imageUrl.toLowerCase();
              if (type === 'video' && !lowUrl.endsWith('.mp4')) continue;
              if (type === 'gif' && !lowUrl.endsWith('.gif')) continue;
              if (type === 'photo' && (lowUrl.endsWith('.mp4') || lowUrl.endsWith('.webm') || lowUrl.endsWith('.gif'))) continue;
              if (!seenUrls.has(imageUrl)) {
                seenUrls.add(imageUrl);
                tempMedia.push(imageUrl);
              }
            }
          }
        }
      }
    } catch (e) {
      console.error("World API error:", e.message);
    }
  }

  // Strategy 3: Fetch individual post pages for full-res images (works for Node.js bot)
  if (tempMedia.length < maxCount) {
    const searchPageUrl = `https://rule34.world/?tags=${encodedQuery}`;
    try {
      const headers = rotateHeaders('https://rule34.world/');
      const res = await fetch(searchPageUrl, { headers });
      if (res.ok) {
        const html = await res.text();
        const postIdRegex = /rule34\.world\/post\/(\d+)/g;
        let m;
        const postIds = [];
        while ((m = postIdRegex.exec(html)) !== null) {
          postIds.push(parseInt(m[1]));
        }
        const uniqueIds = [...new Set(postIds)];
        for (const postId of uniqueIds) {
          if (tempMedia.length >= maxCount) break;
          if (seenUrls.has(`id:${postId}`)) continue;
          seenUrls.add(`id:${postId}`);
          try {
            const postUrl = `https://rule34.world/post/${postId}`;
            const postRes = await fetch(postUrl, { headers: rotateHeaders(postUrl) });
            if (!postRes.ok) continue;
            const postHtml = await postRes.text();
            // Extract file URL from ng-state JSON
            const ngStateMatch = postHtml.match(/<script id="ng-state"[^>]*>([\s\S]*?)<\/script>/);
            if (ngStateMatch) {
              try {
                const ngState = JSON.parse(ngStateMatch[1]);
                const postKey = `get:/api/v2/post/${postId}`;
                const postData = ngState[postKey];
                if (postData && postData.width && postData.height) {
                  const folder = Math.floor(postId / 1000);
                  const fileUrl = `https://rule34.world/posts/${folder}/${postId}/${postId}.jpg`;
                  if (!seenUrls.has(fileUrl)) {
                    seenUrls.add(fileUrl);
                    tempMedia.push(fileUrl);
                  }
                }
              } catch (e) {}
            } else {
              // Fallback: extract from og:image meta tag
              const ogMatch = postHtml.match(/<meta[^>]+property="og:image"[^>]+content="([^"]+)"/);
              if (ogMatch) {
                let imgUrl = ogMatch[1];
                if (imgUrl.startsWith('//')) imgUrl = 'https:' + imgUrl;
                if (imgUrl.startsWith('/')) imgUrl = 'https://rule34.world' + imgUrl;
                if (!seenUrls.has(imgUrl)) {
                  seenUrls.add(imgUrl);
                  tempMedia.push(imgUrl);
                }
              }
            }
          } catch (e) {
            console.error("Error fetching post", postId, ":", e.message);
          }
        }
      }
    } catch (e) {
      console.error("World post scraping error:", e.message);
    }
  }

  tempMedia = Array.from(new Set(tempMedia));
  return shuffleArray(tempMedia);
}

function optimizeTags(userInput) {
  const cleanedInput = userInput.toLowerCase().trim();
  if (cleanedInput === "girl friend fnf") return "girlfriend_(friday_night_funkin)";
  if (cleanedInput === "vannesa fanf") return "vanessa_(fnaf)";
  let cleaned = cleanedInput.replace(/\s+/g, ' ');
  let underscoreVersion = cleaned.replace(/ /g, '_');
  if (CHARACTER_POOL.includes(underscoreVersion)) return underscoreVersion;
  if (cleaned.length >= 3) {
    let match = CHARACTER_POOL.find(char => { const n = char.replace(/_/g, ''); const i = cleaned.replace(/_/g, '').replace(/\s+/g, ''); return n.includes(i) || i.includes(n); });
    if (match) return match;
    const words = cleaned.split(' ');
    if (words.length > 1) { match = CHARACTER_POOL.find(char => { const cn = char.replace(/_/g, ' '); return words.every(w => cn.includes(w)); }); if (match) return match; }
  }
  return underscoreVersion;
}

function shuffleArray(array) { for (let i = array.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [array[i], array[j]] = [array[j], array[i]]; } return array; }

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function sendTelegramMessage(method, payload) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/${method}`;
  try {
    const response = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    return await response.json();
  } catch (e) { console.error("Telegram API Error:", e.message); return null; }
}