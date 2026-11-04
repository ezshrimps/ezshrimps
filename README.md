<a href="https://ezshrimps.com"><img src="assets/header.svg" width="100%" alt="Izzy Xia · 好奇心驱动，做真正用得上的小工具。Curiosity-driven. Shipping small AI tools people actually use."></a>

<b>在 SVTR 做 AI 创投数据，下班做给自己用的小工具：学日语、拆难题、给自己盖一座小镇。下面每个作品都是这样一点点长出来的。</b><br>
<b>I build AI venture data tools at SVTR, and small tools for my own life after hours: learning Japanese, cracking stuck problems, building myself a little town. Every project below grew out of that.</b>

<a href="https://github.com/ezshrimps?tab=repositories"><img src="https://img.shields.io/github/stars/ezshrimps?style=for-the-badge&logo=github&label=stars&color=FFA657" alt="total stars"></a> <a href="https://github.com/ezshrimps?tab=followers"><img src="https://img.shields.io/github/followers/ezshrimps?style=for-the-badge&logo=github&label=followers&color=39D3BB" alt="followers"></a> <a href="https://ezshrimps.com"><img src="https://img.shields.io/badge/ezshrimps.com-0d1117?style=for-the-badge&logo=googlechrome&logoColor=white" alt="ezshrimps.com"></a> <a href="https://svtr.ai"><img src="https://img.shields.io/badge/work-svtr.ai-0d1117?style=for-the-badge&logo=databricks&logoColor=FFA657" alt="svtr.ai"></a>

<img src="assets/divider-bp.svg" width="100%" alt="">

## 🤖 BP-Parser-for-SVTR

<a href="https://github.com/ezshrimps/BP-Parser-for-SVTR"><img src="assets/card-bp.svg" width="100%" alt="BP-Parser：一份 BP 丢进来，一条投资记录走出去。"></a>

<b>一份 BP 丢进来，一条投资记录走出去。</b>PDF 或一段文字都行，Claude 读完后把公司、赛道、轮次、金额、创始人拆成字段，一键填进 SVTR 的飞书创投库。人只需要最后看一眼。<br>
<b>Drop in a pitch deck, get a deal record out.</b> PDF or plain text: Claude reads it, splits out company, sector, round, amount and founders, and fills them into SVTR's Feishu venture database. A human just takes the last look.

<a href="https://github.com/ezshrimps/BP-Parser-for-SVTR"><img src="https://img.shields.io/github/stars/ezshrimps/BP-Parser-for-SVTR?style=for-the-badge&logo=github&label=BP-Parser&color=FFA657" alt="BP-Parser on GitHub"></a>

### 📡 特色：`tail -f svtr/funding.log`

> 从 BP 解析出来的数据最后都汇进 SVTR AI 创投库，这个主页也直接接着它：GitHub Action 每天通过 [svtr.ai](https://svtr.ai) 的 MCP 接口，拉取过去 7 天金额最大的 5 笔 AI 融资，刷新到下面这张表。<br>
> Parsed decks end up in the SVTR AI Venture Database, and this profile reads from it too: a daily GitHub Action pulls the five biggest AI rounds of the past 7 days through svtr.ai's MCP server and refreshes the table below.

<!-- FUNDING:START -->
| Date | Company | Sector | Round | Amount | Lead |
|---|---|---|---|---:|---|
| 11-03 | **Fal.ai** | Dev Platforms | Series D+ | $1.3B | Bessemer Venture Partners |
| 11-04 | **Agility Robotics** | Robotics | IPO | $465M | — |
| 11-04 | **凌川科技** | Compute | Series B | $139M | 亦庄国投屹唐盛和基金 + |
| 11-03 | **墨芯科技** | Compute | Series C | $139M | — |
| 11-04 | **EloElo Group** | Social & Media | Series C | $80M | NBCUniversal + |
<!-- FUNDING:END -->

<sub>→ full stream at [svtr.ai/stream](https://svtr.ai/stream?lang=en)</sub>

<img src="assets/divider-lyrics.svg" width="100%" alt="">

## 🎌 Japanese Lyrics Parser

<a href="https://japanese-songs-lyrics-parser.vercel.app"><img src="assets/card-lyrics.svg" width="100%" alt="Lyrics Parser：每一句歌词，都是一堂日语课。"></a>

<b>每一句歌词，都是一堂日语课。</b>贴进一整首日文歌，每个汉字上标好平假名，整句给出罗马音和中文翻译，再把语法一个词一个词拆开。灵感来自 B 站 UP 主卷心儿。网页版之外，还有一个微信小程序版本「虾学日语歌」。<br>
<b>Every lyric is a Japanese lesson.</b> Paste a whole song: every kanji gets its furigana, every line gets romaji and a translation, and the grammar is broken down word by word. There's a web app and a WeChat mini-program.

<a href="https://japanese-songs-lyrics-parser.vercel.app"><img src="https://img.shields.io/badge/▶_Try_it-试一试-1f9e8c?style=for-the-badge" alt="Try it"></a>
<a href="https://github.com/ezshrimps/Japanese-Songs-Lyrics-Parser"><img src="https://img.shields.io/github/stars/ezshrimps/Japanese-Songs-Lyrics-Parser?style=for-the-badge&logo=github&label=web&color=39D3BB" alt="web on GitHub"></a>
<a href="https://github.com/ezshrimps/ShrimpLyricsParser"><img src="https://img.shields.io/github/stars/ezshrimps/ShrimpLyricsParser?style=for-the-badge&logo=wechat&logoColor=white&label=%E5%B0%8F%E7%A8%8B%E5%BA%8F&color=39D3BB" alt="mini-program on GitHub"></a>
<a href="https://github.com/ezshrimps/ShrimpWxBackend"><img src="https://img.shields.io/github/stars/ezshrimps/ShrimpWxBackend?style=for-the-badge&logo=nextdotjs&label=backend&color=39D3BB" alt="backend on GitHub"></a>

<img src="assets/divider-triz.svg" width="100%" alt="">

## 💡 ShrimpTRIZ

<a href="https://shrimp-triz.vercel.app"><img src="assets/card-triz.svg" width="100%" alt="ShrimpTRIZ：卡住的问题，交给 40 条发明原理。"></a>

<b>卡住的问题，交给 40 条发明原理。</b>受 AutoTRIZ 论文启发：说出你想改进什么、又怕牺牲什么，它帮你理清背后的技术矛盾，再从 40 条发明原理里挑出值得一试的方向。<br>
<b>Stuck? Let 40 inventive principles have a go.</b> Inspired by AutoTRIZ: describe what you want to improve and what you're afraid to lose, and it untangles the contradiction underneath and picks principles worth trying.

<a href="https://shrimp-triz.vercel.app"><img src="https://img.shields.io/badge/▶_Try_it-试一试-b08800?style=for-the-badge" alt="Try it"></a>

<img src="assets/divider-planet.svg" width="100%" alt="">

## 🪐 personal-little-planet

<img src="assets/card-planet.svg" width="100%" alt="Little Planet：一座可以走进去的漂浮小镇。">

<b>一座可以走进去的漂浮小镇。</b>我的个人说明书不是一页简历，而是一座 Three.js 小镇：九个可以推门进去的室内场景，收着我的爱好、藏品和旅行地图，还有我的摄影作品。还在慢慢盖。<br>
<b>A personal manual you can walk into.</b> Not a résumé page but a floating Three.js town: nine interiors to step into, holding my hobbies, collections, travel map and photography. Still under construction.

<img src="https://img.shields.io/badge/🔒_private-施工中_·_coming_soon-A493FF?style=for-the-badge" alt="private, coming soon">

<img src="assets/divider-end.svg" width="100%" alt="">

## 📦 更多作品 · More

| | 作品 | 一句话 |
|---|---|---|
| 📱 | **SVTR-MiniProgram** 🔒 | SVTR AI 创投库的微信小程序，按公司、赛道、机构、人物、毕业学校查数据 · SVTR's venture database as a WeChat mini-program |
| 📒 | [**attention-is-all-i-read**](https://github.com/ezshrimps/attention-is-all-i-read) | 我的研究日志和方法论 · My research log and methods |
| 🍎 | [**Shrimp-Accounting**](https://github.com/ezshrimps/Shrimp-Accounting) | 记录每日收支的 iOS App · An iOS app for daily finances |
| 🌐 | [**Personal-Website**](https://github.com/ezshrimps/Personal-Website) | [ezshrimps.com](https://ezshrimps.com)：编程、摄影、音游和匹克球 · Code, photography, rhythm games and pickleball |
| 🧩 | [**huggingface-based-AI-generate-similar-icon**](https://github.com/ezshrimps/huggingface-based-AI-generate-similar-icon) | 用 Hugging Face 模型生成风格相近的图标 · Generate look-alike icons with Hugging Face models |
| 🖼️ | [**Artwork-from-CS116**](https://github.com/ezshrimps/Artwork-from-CS116) | 用 CS116 学到的视觉技术做出来的"人造照片" · Synthetic photos made with CS116 vision techniques |
| 🧪 | [**CS117_final_project**](https://github.com/ezshrimps/CS117_final_project) | UCI CS117 课程期末项目 · Course final project |
| 🏓 | [**PickleBallScoringRules**](https://github.com/ezshrimps/PickleBallScoringRules) | 匹克球计分规则，太好玩了！ · Pickleball is toooo funnnnn |

**🤝 开源贡献 · Contributions**：给 [RealtimeTTS](https://github.com/ezshrimps/RealtimeTTS) 修了 `text_to_stream.py` 的一个 bug；在 [iDesignGPT](https://github.com/ezshrimps/VisualiDesignGPT) 的框架下加了一个可视化模块。

<details>
<summary><b>🕒 最近在写 · Recently pushed</b></summary>
<br>

<!-- ACTIVITY:START -->
- `2026-05-04` [BP-Parser-for-SVTR](https://github.com/ezshrimps/BP-Parser-for-SVTR)
- `2026-03-21` [AI-Image-Gen-Arena-with-Replicate](https://github.com/ezshrimps/AI-Image-Gen-Arena-with-Replicate)
- `2026-03-19` [ShrimpLyricsParser](https://github.com/ezshrimps/ShrimpLyricsParser)
- `2026-03-19` [ShrimpWxBackend](https://github.com/ezshrimps/ShrimpWxBackend)
- `2026-03-19` [Japanese-Songs-Lyrics-Parser](https://github.com/ezshrimps/Japanese-Songs-Lyrics-Parser)
<!-- ACTIVITY:END -->

</details>

<img src="assets/divider-end.svg" width="100%" alt="">

<a href="https://ezshrimps.com"><img src="assets/footer.svg" width="100%" alt="觉得有意思的话，点一颗 star 就是对我最大的鼓励。ezshrimps.com · svtr.ai"></a>

<p align="center">
<!-- UPDATED:START -->
<sub>last sync: 2026-11-04 21:35 UTC</sub>
<!-- UPDATED:END -->
</p>
