# Character Generation Paper Watch

一个面向 **AI 生成式角色建模、Text-to-Live2D、动漫角色生成、Live2D 数字人建模与可控编辑** 的论文与代码追踪仓库。

This repository tracks recent papers, project pages, demos, and code repositories related to **generative character modeling**, **Text-to-Live2D**, **anime character generation**, and **Stable Diffusion-based controllable character generation**.

---

## 🎯 Research Focus

本仓库主要服务于以下研究方向：

- AI generative character modeling
- Text-to-Live2D
- Anime character generation
- 2D / 2.5D digital humans
- Stable Diffusion-based character generation
- Controllable character editing
- Layered character representation
- Live2D-ready asset generation
- Character consistency and identity preservation
- Pose / expression / attribute-controlled character generation

当前重点关注如何从 **文本描述或参考图像** 生成 **可编辑、可控、可动画化的 2D / 2.5D 动漫角色模型**。

---

## 🔬 Core Topics

| Area | Keywords |
|---|---|
| Text-to-Character | text-to-character, text-to-avatar, anime character generation |
| Text-to-Live2D | Live2D generation, image-to-Live2D, layered assets, part decomposition |
| Stable Diffusion | Stable Diffusion, Latent Diffusion, ControlNet, LoRA, IP-Adapter, DreamBooth |
| Character Control | pose control, expression editing, attribute editing, identity consistency |
| Layered Modeling | layered character generation, character segmentation, part-aware generation |
| Animation-ready Avatars | animatable character, riggable 2D avatar, talking avatar, portrait animation |
| Digital Humans | 2D digital human, virtual avatar, anime digital human |

---

## 📌 Scope

本仓库优先追踪以下类型的研究工作：

### Core Relevance

直接与以下方向相关的论文和代码会被视为核心相关：

- Text-to-Live2D
- Image-to-Live2D
- 文本驱动动漫角色生成
- Stable Diffusion 角色一致性生成
- 角色姿态、表情、属性可控编辑
- 分层角色素材生成
- 角色部件分解与分割
- 可绑定、可驱动、可动画化 2D / 2.5D 角色建模

### Strong Relevance

以下方向与本研究强相关：

- reference-guided character generation
- subject-driven character generation
- pose-guided character generation
- expression-guided character editing
- LoRA / DreamBooth-based character personalization
- ControlNet / IP-Adapter-based character control
- anime avatar generation
- 2D digital human generation

### Edge Relevance

以下方向可能具有参考价值，但需要人工判断：

- 一般 text-to-image generation
- 一般 image editing
- 一般 portrait animation
- 一般 3D human reconstruction
- 一般 digital human generation
- 与角色建模间接相关的 diffusion model 改进方法

边缘相关项目不会强行归入核心方向，除非其方法能够明显迁移到 **Text-to-Live2D、动漫角色建模或可控角色编辑**。

---

## 🗂 Repository Structure

```text
character-generation-paper-watch/
├── README.md
├── reports/
│   └── YYYY-MM-DD.md
├── index/
│   └── papers.json
├── memory/
│   ├── seen-character-generation-papers.md
│   ├── pending-character-generation-review.md
│   └── run-notes.md
├── prompts/
│   └── agent-instructions.md
└── scripts/
    └── paper_watch.py
```

---

## 📰 Reports

每次运行后，报告会保存到：

```text
reports/YYYY-MM-DD.md
```

每篇报告默认包含以下部分：

1. **新发现**
2. **重要更新**
3. **待人工确认**
4. **趋势观察**

### Report Format

每个新发现项目通常包含：

- 标题
- 论文链接
- 项目链接
- 代码链接
- Demo / 模型权重链接
- 发布时间或首次发现时间
- 相关性等级
- 研究问题概述
- 方法亮点
- 与 Stable Diffusion / LDM 的关系
- 与 Text-to-Live2D / 动漫角色建模的关系
- 代码状态总结
- 为什么值得关注

---

## 🧠 Paper Index

结构化论文索引保存在：

```text
index/papers.json
```

每条记录至少包含以下字段：

```json
{
  "title": "",
  "aliases": [],
  "paper_url": "",
  "project_url": "",
  "code_url": "",
  "demo_url": "",
  "model_url": "",
  "first_seen_date": "",
  "last_updated_date": "",
  "publication_date": "",
  "authors": [],
  "venue_or_source": "",
  "relevance_level": "",
  "topics": [],
  "uses_stable_diffusion": null,
  "uses_lora": null,
  "uses_controlnet": null,
  "uses_ip_adapter": null,
  "supports_live2d": null,
  "supports_layered_character": null,
  "supports_character_editing": null,
  "supports_animation": null,
  "code_status": "",
  "dedupe_status": "",
  "report_path": "",
  "notes": ""
}
```

---

## 🏷 Relevance Levels

| Level | Meaning |
|---|---|
| `core` | 直接相关：Text-to-Live2D、分层角色生成、可动画化 2D / 2.5D 角色建模 |
| `strong` | 强相关：动漫角色生成、SD 角色控制、角色一致性、可控编辑 |
| `edge` | 边缘相关：方法有迁移价值，但不是直接面向角色建模 |
| `pending` | 待确认：相关性、重复性或代码对应关系尚不明确 |

---

## 💻 Code Status

| Status | Meaning |
|---|---|
| `official_full` | 官方仓库，包含较完整训练 / 推理 / 数据处理代码 |
| `official_inference_only` | 官方仓库，仅包含推理代码 |
| `official_demo_only` | 官方仓库，仅提供 demo 或在线演示 |
| `official_placeholder` | 官方仓库存在，但代码尚未正式发布 |
| `unofficial` | 第三方复现或非官方实现 |
| `not_found` | 暂未找到代码 |
| `unclear` | 代码与论文对应关系不明确 |

---

## 🔍 Discovery Sources

本仓库优先从以下公开来源追踪新论文与代码：

- arXiv
- Papers with Code
- OpenReview
- CVPR / ICCV / ECCV / SIGGRAPH / SIGGRAPH Asia / NeurIPS / ICLR / AAAI / ACM MM
- 项目主页
- 实验室主页
- 作者主页
- GitHub
- Hugging Face
- Gradio / Demo 页面
- Awesome lists
- 研究博客与论文索引页

---

## 🔎 Search Keywords

常用搜索关键词包括：

```text
text-to-Live2D
Live2D generation
image-to-Live2D
anime character generation diffusion
text-to-character generation
text-to-avatar generation
cartoon character generation Stable Diffusion
layered character generation
animatable character generation
riggable character generation
controllable character editing diffusion
character consistency Stable Diffusion
reference-guided character generation
subject-driven character generation
pose-guided character generation
expression-guided character editing
ControlNet character generation
LoRA anime character
IP-Adapter character
DreamBooth character personalization
2D avatar generation diffusion
digital human anime generation
character part decomposition
character segmentation animation
```

---

## 🔁 Deduplication Rules

去重时不仅检查标题完全匹配，还会综合判断：

- 标题大小写、标点、缩写和副标题差异
- arXiv 版本与会议版本差异
- 项目名、论文名、GitHub 仓库名不一致的情况
- 是否为同一作者团队
- 是否共享相同方法名、模型名、数据集名或 demo 页面
- 是否只是旧论文新增代码、demo 或模型权重
- 是否已存在于 `index/papers.json`
- 是否已记录在 `memory/seen-character-generation-papers.md`
- 是否已出现在过往 `reports/YYYY-MM-DD.md`

如果无法确认是否重复，默认放入 **待人工确认**，而不是直接作为新发现。

---

## 🧾 Memory Files

长期追踪记录保存在：

```text
memory/seen-character-generation-papers.md
memory/pending-character-generation-review.md
memory/run-notes.md
```

### `seen-character-generation-papers.md`

记录已确认发现并报告过的论文，包括：

- 标题
- 标准化别名
- 论文链接
- 项目链接
- 代码链接
- 首次发现日期
- 是否已有代码
- 是否与 Stable Diffusion 相关
- 是否与 Live2D / 分层角色建模相关

### `pending-character-generation-review.md`

记录暂时无法确认的候选项目，包括：

- 可能重复的项目
- 相关性不明确的项目
- 代码对应关系不清晰的项目
- 需要人工进一步确认的疑点

### `run-notes.md`

记录每次运行的搜索情况，包括：

- 日期
- 搜索关键词
- 主要来源
- 新发现数量
- 待确认数量
- 异常情况
- 未发现新增时的搜索覆盖说明

---

## 🤖 Agent Instructions

用于 ChatGPT Agent 的完整追踪指令建议保存在：

```text
prompts/agent-instructions.md
```

该 Agent 负责：

- 搜索最新论文、项目主页和代码仓库
- 判断是否与生成式角色建模相关
- 检查代码是否官方、完整、可复现
- 对比历史记录进行去重
- 输出中文研究日报或周报
- 更新 `reports/`、`index/` 和 `memory/`

---

## 🧪 Relation to My Research

本仓库重点支持以下研究问题：

> 如何从文本描述或参考图像生成可编辑、可控、可动画化的 2D / 2.5D 动漫角色，并进一步映射到 Live2D 风格的数字人建模流程？

当前特别关注与以下方向相关的工作：

- Textoon-style pipeline
- Text-to-Live2D
- Stable Diffusion-based anime character generation
- Layered character assets
- Character part decomposition
- Identity-consistent character editing
- Pose and expression control
- Reference-guided character customization
- Live2D-compatible asset generation

---

## 📊 Trend Tracking

报告中会持续观察以下趋势：

- 角色生成是否从单图生成转向分层、可编辑、可驱动建模
- Stable Diffusion / LDM 是否仍是主流底座
- ControlNet、LoRA、IP-Adapter、DreamBooth 在角色控制中的使用情况
- 角色一致性与身份保持方法的发展
- 动漫角色生成是否出现更多结构化、部件级、Live2D-ready 的方法
- 代码、模型权重和 demo 的开放情况
- 哪些工作对 Text-to-Live2D 研究最有迁移价值

---

## ⚠️ Reliability Rules

本仓库遵循以下原则：

- 不伪造论文、代码、作者、发布日期或实验结论
- 不把第三方转载页当作唯一依据
- 不把一般 text-to-image 论文误判为角色建模论文
- 不把一般动漫图像生成工具误判为 Text-to-Live2D
- 不把名称相似的第三方仓库误判为官方代码
- 不声称某项目支持 Live2D，除非论文、项目页或 README 明确说明
- 遇到信息冲突时，优先参考：
  - 论文主页
  - arXiv
  - 官方项目页
  - 官方 GitHub
  - 作者主页
  - 会议页面

当证据不足时，项目会被保守标注为 **pending** 或放入 **待人工确认**。

---

## 📌 Maintainer

Maintained by [@lucas-lizhiwei](https://github.com/lucas-lizhiwei)

Research interests:

- Generative AI
- Computer Vision
- Digital Humans
- Anime Character Generation
- Text-to-Live2D
- Stable Diffusion
- Controllable Character Editing
