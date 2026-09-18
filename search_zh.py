# -*- coding: utf-8 -*-
"""构建钩子扩展：中文分词增强的搜索索引（jieba）。

在 MkDocs 原生 search 插件生成索引后，把中文长词切分为更细粒度，
使「掩码」「码本」等词能命中「掩码码字预测」这类内容。
"""
import json
import pathlib

import jieba

ROOT = pathlib.Path(__file__).resolve().parent
SEARCH_INDEX = ROOT / "site" / "search" / "search_index.json"

# 领域词加入词典，避免被切碎
for w in ["掩码建模", "码本", "码字", "自回归", "梯度反转", "向量量化", "掩码预测",
          "运动想象", "睡眠分期", "情绪识别", "异常检测", "事件分类", "通道注意力",
          "电极级", "单通道", "预训练", "微调", "线性注意力", "对比学习", "指令微调",
          "多任务", "基础模型", "频谱图", "时频", "电极图", "tokenizer", "masked"]:
    jieba.add_word(w)


def on_post_build(config, **kwargs):
    if not SEARCH_INDEX.exists():
        return
    data = json.loads(SEARCH_INDEX.read_text(encoding="utf-8"))
    docs = data.get("docs", [])
    for doc in docs:
        title = doc.get("title", "")
        text = doc.get("text", "")
        seg = " ".join(w for w in jieba.cut(title + " " + text) if w.strip())
        doc["text"] = seg
    SEARCH_INDEX.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"[hooks] 搜索索引已完成 jieba 中文分词（{len(docs)} 条）")
