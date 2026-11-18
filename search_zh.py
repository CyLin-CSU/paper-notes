# -*- coding: utf-8 -*-
"""构建钩子扩展：中文分词增强的搜索索引（jieba）。

在 MkDocs 原生 search 插件生成索引后，把中文长词切分为更细粒度，
使「掩码」「码本」等词能命中「掩码码字预测」这类内容。
"""
import json
import pathlib
import re

import jieba

ROOT = pathlib.Path(__file__).resolve().parent

# 连字符词与站点专名加入词典，避免被切碎
jieba.add_word("Uni-NTFM")
jieba.add_word("REVE")

# 领域词加入词典，避免被切碎
for w in ["掩码建模", "码本", "码字", "自回归", "梯度反转", "向量量化", "掩码预测",
          "运动想象", "睡眠分期", "情绪识别", "异常检测", "事件分类", "通道注意力",
          "电极级", "单通道", "预训练", "微调", "线性注意力", "对比学习", "指令微调",
          "多任务", "基础模型", "频谱图", "时频", "电极图", "tokenizer", "masked",
          "批判性综述", "领域综述", "综述速览", "线性探针", "数据规模", "评测基准",
          "跨被试", "跨会话", "跨设备", "位置编码", "条件位置编码", "词元化",
          "scaling", "law", "channel", "hours", "linear", "probing", "ood"]:
    jieba.add_word(w)


TAG_RE = re.compile(r"<[^>]+>")

# 受控同义词（方案 C 首批五组）：索引文本包含规范词时，追加同义词，
# 使中英任一写法都能命中同一批文档。
SYNONYMS = [
    ("脑电", ["EEG", "electroencephalography"]),
    ("EEG", ["脑电", "electroencephalogram"]),
    ("运动想象", ["MI", "motor imagery"]),
    ("线性探针", ["linear probing", "frozen features"]),
    ("数据规模", ["scaling law", "scaling"]),
    ("电极布局", ["montage", "电极配置", "导联配置"]),
]


def _clean(text: str) -> str:
    """去掉索引正文里的 HTML 标签，避免搜索摘要出现裸露的 <span>/<li> 片段。"""
    return TAG_RE.sub(" ", text)


def _expand_synonyms(title: str, text: str) -> str:
    """按受控同义词表扩展：doc 含规范词（中或英）时补齐其余写法。"""
    hay = title + " " + text
    extra = []
    for canonical, alts in SYNONYMS:
        if canonical in hay or any(a.lower() in hay.lower() for a in alts):
            extra.extend(alts)
            if canonical not in hay:
                extra.append(canonical)
    return (" " + " ".join(sorted(set(extra)))) if extra else ""


def on_post_build(config, **kwargs):
    # 索引路径跟随实际输出目录（自定义 --site-dir 时同样生效）
    index = pathlib.Path(config.get("site_dir", "site")) / "search" / "search_index.json"
    if not index.exists():
        return
    data = json.loads(index.read_text(encoding="utf-8"))
    docs = data.get("docs", [])
    for doc in docs:
        title = _clean(doc.get("title", ""))
        text = _clean(doc.get("text", ""))
        text = text + _expand_synonyms(title, text)
        seg = " ".join(w for w in jieba.cut(title + " " + text) if w.strip())
        doc["text"] = seg
    index.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"[hooks] 搜索索引已完成 jieba 中文分词与受控同义词扩展（{len(docs)} 条）")
