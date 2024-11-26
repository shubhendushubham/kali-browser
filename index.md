---
layout: home
title: "KQL Query Search"
---

<div class="search-container">
    <input type="text" class="search-box" placeholder="type your Query here" id="searchQuery">
    <button onclick="fetchKQLResults()">Fetch from GitHub</button>
    <button onclick="chatWithOpenAI()">Chat with OpenAI</button>
    <div id="results"></div>
</div>
