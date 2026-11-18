---
title: 阅读清单
tags: [工具, 阅读清单]
---

# 阅读清单

> 收藏保存在**当前浏览器**（localStorage，键 `paper-notes.reading.v1`）——在各论文笔记页的标题下点「保存阅读」加入。导出 JSON 可换设备恢复；导入前会显示新增/更新的条目数。禁用脚本时本页仅显示说明，笔记本身照常可读。

<div class="rl-tools">

<button id="rl-export" type="button">导出 JSON</button>
<input type="file" id="rl-file" accept=".json" style="display:inline-block">
<button id="rl-import" type="button">导入</button>
<button id="rl-clear" type="button">清空</button>

</div>

<div id="rl-list" class="rl-list"></div>

维护约定：导出文件带 `version` 字段，旧版 ID 可经 paper_id 映射恢复；导出仅包含你主动收藏的条目，不包含浏览历史。

---

**相关阅读**：[论文库](library.md) ｜ [模型对比](models.md) ｜ [实验证据](evidence.md) ｜ [首页](index.md)
