# -*- coding: utf-8 -*-
"""向 data/evidence.json 追加第二批证据（M3·E 包：扩到 40+ 条）。
全部数值出自站内精读笔记（status=verified，source 标注笔记转述的原文表号）。
"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
P = pathlib.Path(__file__).resolve().parents[1] / "data" / "evidence.json"
rows = json.loads(P.read_text(encoding="utf-8"))
have = {r["evidence_id"] for r in rows}

ADD = [
    # CBraMod
    ("cbramod-t2-tuab-balacc", "cbramod", "表 2（站内 cbramod.md 转述）", "cbramod-base", "tuab", "微调", "balanced accuracy", {"value": 0.8289}, "", "TUAB 官方划分", "原报告口径"),
    ("cbramod-ablation-attn", "cbramod", "附录消融（站内 comparison.md 转述）", "cbramod-base", None, "消融", "注意力头分配", {"best": "4:4 时空头", "note": "6:2 / 2:6 偏科均下降"}, "", "", "十字交叉注意力消融：空间与时间依赖同等重要"),
    # LaBraM
    ("labram-t-tuab-balacc", "labram", "表（站内 comparison.md 转述）", "labram-base", "tuab", "微调", "balanced accuracy", {"value": 0.814}, "", "TUAB 官方划分", "Yao 自跑口径 0.8140 与原报告互证"),
    ("labram-data-scaling-tuev", "labram", "其数据量消融（站内 blog 转述）", "labram-base", "tuev", "微调", "相对 2500h 版本达成率", {"tuev_at_500h_pct": 90}, "%", "", "Base 500h 预训练在 TUEV 达到 2500h 版本的 90%+"),
    # LUNA
    ("luna-tuar-sota", "luna", "表（站内 datasets.md 引用）", "luna-base", None, "微调", "TUAR 伪迹分类准确率", {"value": 0.921}, "", "", "TUAR 5 类伪迹任务上为其对比中 SOTA"),
    ("luna-tuab-bottleneck", "luna", "其消融（站内 blog 转述）", "luna-base", "tuab", "微调", "相对全注意力差距", {"gap_pp": 1}, "pp", "", "隐空间瓶颈的代价：TUAB 上落后全注意力约 1pp"),
    ("luna-flops-8000ch", "luna", "其表 4（效率对照）", "luna-base", None, "FLOPs 对照", "8000 通道前向计算量", {"luna_gflops": 23, "biot_gflops": 4156}, "GFLOPs", "", "约 1/180；Base 16-bit 约 14MB"),
    # NeuroRVQ / BrainRVQ
    ("neurorvq-recon-mse", "neurorvq", "其重构表（站内 references 转述）", "neurorvq", None, "tokenizer 重构", "EEG 重构 MSE", {"neurorvq": 0.016, "labram": 1.071}, "", "同数据同口径", "低 67 倍"),
    ("neurorvq-ecg-43class", "neurorvq", "其 ECG 表（站内 references 转述）", "neurorvq", None, "微调", "ECG 43 类分类", {"note": "较最强基线翻倍"}, "", "", "幅相分离重构对 ECG 同样有效"),
    # EEGPT
    ("eegpt-lp-sota", "eegpt", "其表（站内 eegpt.md 转述）", "eegpt-main", None, "线性探针", "多任务平均", {"note": "linear probing 即达其对比中 SOTA"}, "", "", "对齐目标（JEPA 式）+ 掩码重构双自监督的冻结可用性证据"),
    # BrainGPT
    ("braingpt-ar-vs-mae", "braingpt", "表 V（站内 braingpt.md 转述）", "braingpt-giant", None, "同架构同损失对照", "五任务平均准确率差", {"ar_minus_mae_pp": 2.5}, "pp", "", "L2 损失最优时自回归较掩码重构平均高 2.5pp；作者归因时序因果结构，限于该五任务"),
    ("braingpt-mt-smalltask", "braingpt", "表 VI（站内 blog 转述）", "braingpt-giant", None, "12 基准联合训练", "认知负荷任务增益", {"gain_pp": 3.9}, "pp", "", "多任务信息载体是电极节点被多任务梯度共同更新；小任务受益最大"),
    # NeuroLM
    ("neurolm-perplexity-scaling", "neurolm", "§3.6（站内 blog 转述）", "neurolm-xl", None, "预训练规模", "验证困惑度", {"note": "L 与 XL 两档接近，十亿级参数未训满（作者观点）"}, "", "", "25000h 语料上的模型缩放观察"),
    # NeuroDETR
    ("neurodetr-f1-all-first", "neurodetr", "其主表（站内 neurodetr.md 转述）", None, None, "事件检测", "事件级 F1", {"note": "8 数据集全部第一"}, "", "", "多尺度 VQ 事件记忆 + DETR 式集合预测"),
    # CodeBrain
    ("codebrain-token-bridge", "codebrain", "站内 codebrain.md", None, None, "架构定性", "token 角色", {"note": "token 退守预训练目标，未作下游输入"}, "", "", "与 TFM（token 作输入）构成 token 用途的两极"),
    # Not-All-EEG
    ("not-all-eeg-tsfid", "not-all-eeg", "其主表（站内 not-all-eeg.md 转述）", None, None, "生成评估", "TS-FID 相对复现 JET", {"reduction_pct": [40, 62]}, "%", "", "位置自适应时间调度（PATS）+ 因子化时空注意力 + 频率加权多分辨率频谱损失"),
    # EEGDM
    ("eegdm-spsw-recall", "eegdm", "其表（站内 eegdm.md 转述）", "eegdm-encoder", None, "微调", "少数类召回（SPSW）", {"minority_recall_pct": [10, 18]}, "%", "", "被 EEGDM 用作批评 CBraMod 容量分配的证据；类不均衡场景鲁棒"),
    # REVE 补充
    ("reve-channel-pruning-mi", "reve", "其稀疏性实验（站内 reve.md 转述）", "reve-base", "physionet-mi", "通道递减", "MI 任务准确率", {"ch64": 0.824, "ch1": 0.66}, "", "", "空间信息密集任务优雅退化；想象语音则 0.565→0.209 接近随机"),
    ("reve-fewshot-20", "reve", "其少样本表（站内 reve.md 转述）", "reve-base", None, "20-shot", "纯预训练权重 vs 跨数据集微调", {"pretrain_only": 0.723, "cross_ft": 0.817}, "", "", "跨数据集微调再 +9.4pp"),
    ("reve-isruc-kappa", "reve", "表 2（站内 reve.md 转述）", "reve-base", None, "微调", "ISRUC 平衡精度 / Kappa", {"bacc": 0.7819, "kappa": 0.75}, "", "", "平衡精度略低 CBraMod 0.7865 但 Kappa 0.7500 更高；REVE 修正了基线下巴电极混入 bug"),
    # JET 补充
    ("jet-tsfid-baseline", "jet", "项目页 quantitative-comparison（站内 jet.md 转述）", "jet-generator", None, "生成评估", "TS-FID", {"note": "较 EEG-GAN / Vanilla Diffusion 强基线低 40%+"}, "", "", "对照限于该论文的三项基准"),
    # EEGArena 补充
    ("eegarena-fm-lead", "eegarena", "§3（站内 eegarena.md 转述）", None, None, "统一管线横评", "定性结论", {"conclusion": "FM 大多领先监督基线，但参数量不预测性能"}, "", "", "30 FM × 25 监督基线 × 57 任务"),
    # Kuruppu 补充
    ("kuruppu-tuev-f1-range", "kuruppu-critical-review", "§4.3 与其图 3(b)", None, "tuev", "微调", "F1 跨模型范围", {"range": [0.7, 0.83]}, "", "TUEV 官方划分", "仅 4 个 FM 可比；TUAB 或已饱和（传统方法 85–87%，其引 [152]）"),
    # Défossez scaling
    ("defossez-meg-retrieval", "defossez-speech", "其主结果（站内 defossez-speech.md 转述）", None, None, "零样本检索", "3 秒 MEG 千余候选检索", {"note": "详见其笔记"}, "", "", "脑信号-语音对比对齐轴线的源头工作"),
]

for eid, pid, src, mid, ds, proto, metric, value, unit, split, note in ADD:
    if eid in have:
        continue
    rows.append({
        "evidence_id": eid, "paper_id": pid, "source": src,
        "model_id": mid if mid else None, "dataset": ds,
        "protocol": proto, "metric": metric, "value": value,
        "unit": unit, "split": split, "status": "verified", "note": note,
    })

P.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("evidence 总数:", len(rows))
