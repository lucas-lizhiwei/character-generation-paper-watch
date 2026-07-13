# 已确认记录

更新日期：2026-07-13

## 1. See-through: Single-image Layer Decomposition for Anime Characters

- 标准标题：See-through: Single-image Layer Decomposition for Anime Characters
- 别名：See-through
- 论文链接：https://arxiv.org/abs/2602.03749
- 代码链接：https://github.com/shitagaki-lab/see-through
- 首次记录日期：2026-05-18
- SD / LDM 关系：是。README 明确说明 LayerDiff 3D 基于 SDXL。
- Live2D 关系：强相关。论文明确使用商业 Live2D 模型引导监督，输出可编辑分层结果。
- 代码状态：官方完整开源（推理、训练、Demo、模型权重）。
- 备注：当前最值得优先跟进的公开项目之一。

## 2. MRT: Masked Region Transformer for Layered Image Generation and Editing at Scale

- 标准标题：MRT: Masked Region Transformer for Layered Image Generation and Editing at Scale
- 别名：MRT；Masked Region Transformer
- 论文链接：https://arxiv.org/abs/2605.27235
- 代码链接：未找到
- 首次记录日期：2026-06-01
- SD / LDM 关系：不是 Stable Diffusion 路线；论文描述为 masked region diffusion / multi-layer transparent image generation framework。
- Live2D 关系：间接强相关。它不直接支持 Live2D 或动漫角色，但 text-to-layers / image-to-layers 是 Text-to-Live2D 的关键中间能力。
- 代码状态：未开源。
- 备注：2026-05-26 公开，CVPR 2026。作为通用分层图像生成基线纳入。

## 3. RealDiffusion: Physics-informed Attention for Multi-character Storybook Generation

- 标准标题：RealDiffusion: Physics-informed Attention for Multi-character Storybook Generation
- 别名：RealDiffusion
- 论文链接：https://arxiv.org/abs/2605.11927
- 代码链接：https://github.com/ShmilyQi-CN/RealDiffusion
- 首次记录日期：2026-06-01
- SD / LDM 关系：是。官方 README 明确 built on Stable Diffusion XL，并测试 Playground v2.5。
- Live2D 关系：间接相关。不生成 Live2D 层或绑定结构，但对多角色身份保持、跨帧一致性、多姿态素材生成有启发。
- 代码状态：官方代码，偏推理实现；仓库较小，需后续实测。
- 备注：2026-05-12 公开，CVPR 2026。本次作为补录项加入。

## 4. AnimeAdapter: Fine-grained and Consistent Zero-shot Anime Character Generation

- 标准标题：AnimeAdapter: Fine-grained and Consistent Zero-shot Anime Character Generation
- 别名：AnimeAdapter
- 论文链接：https://arxiv.org/abs/2605.20237
- 代码链接：未找到
- 首次记录日期：2026-06-01
- SD / LDM 关系：是。论文明确为 Stable Diffusion 设计轻量 appearance adapter。
- Live2D 关系：间接强相关。不输出 Live2D 图层，但直接解决动漫角色一致性、参考图控制和姿态条件生成。
- 代码状态：未开源；论文称 acceptance 后发布代码、权重和数据集。
- 备注：2026-05-17 公开。本次作为补录项加入，后续重点追踪开源状态。

## 5. Textoon: Generating Vivid 2D Cartoon Characters from Text Descriptions

- 标准标题：Textoon: Generating Vivid 2D Cartoon Characters from Text Descriptions
- 别名：Textoon
- 论文链接：https://arxiv.org/abs/2501.10020
- 项目链接：https://human3daigc.github.io/Textoon_webpage/
- 代码链接：https://github.com/Human3DAIGC/Textoon
- 首次记录日期：2026-06-08
- SD / LDM 关系：是。官方 README 要求使用 SDXL cartoon / anime checkpoint，并依赖 ComfyUI 工作流。
- Live2D 关系：核心相关。论文和 README 均明确从文本描述生成 Live2D 格式 2D cartoon character，并支持 MediaPipe / ARKit 风格驱动渲染。
- 代码状态：官方完整开源（ComfyUI 工作流、主程序、Gradio demo、Live2D render / drive 代码、TextoonPromptParsing 模型链接）。
- 备注：论文 2025-01-17 公开，本次作为历史核心基线补录；后续应重点复现实验和检查生成模型/素材许可限制。

## 6. SCAIL-2: Unifying Controlled Character Animation with End-to-end In-Context Conditioning

- 标准标题：SCAIL-2: Unifying Controlled Character Animation with End-to-end In-Context Conditioning
- 别名：SCAIL-2
- 论文链接：https://arxiv.org/abs/2606.10804
- 项目链接：https://teal024.github.io/SCAIL-2/
- 代码链接：https://github.com/zai-org/SCAIL-2
- 模型权重：https://huggingface.co/zai-org/SCAIL-2
- 首次记录日期：2026-06-15
- SD / LDM 关系：不是 Stable Diffusion 路线；官方实现基于 Wan 2.1 / video diffusion 体系，README 提供 LoRA 集成和 DPO LoRA 说明。
- Live2D 关系：间接相关。不生成 Live2D 层或绑定结构，但面向参考角色 + 驱动视频的可控角色动画，可作为生成角色后续驱动和角色替换支线参考。
- 代码状态：官方推理代码 + 模型权重；README 提供预处理、单卡推理、角色替换和多参考输入说明，未发现完整训练代码。
- 备注：2026-06-09 公开，相关性 3/5。本周最值得阅读的新工作，尤其适合观察角色动画从骨骼/姿态中间表示转向端到端视觉条件的趋势。

## 7. SketchKeyAnime: Reference-anchored Sparse Key-Sketch Animation Synthesis

- 标准标题：SketchKeyAnime: Reference-anchored Sparse Key-Sketch Animation Synthesis
- 别名：SketchKeyAnime
- 论文链接：https://arxiv.org/abs/2606.19958
- 代码链接：未找到
- 首次记录日期：2026-06-22
- SD / LDM 关系：未确认。论文摘要明确为 video diffusion framework，但未发现 Stable Diffusion / SDXL / ControlNet / LoRA / IP-Adapter 证据。
- Live2D 关系：间接强相关。不生成 Live2D 层、绑定结构或模型，但使用单张角色参考图和稀疏关键草图生成动漫动画，适合作为 Text-to-Live2D 后续动画控制支线。
- 代码状态：未开源。
- 备注：2026-06-18 公开，相关性 4/5。本周唯一确认新增的 3 分及以上项目。

## 8. CartoonAlive: Towards Expressive Live2D Modeling from Single Portraits

- 标准标题：CartoonAlive: Towards Expressive Live2D Modeling from Single Portraits
- 别名：CartoonAlive
- 论文链接：https://arxiv.org/abs/2507.17327
- 项目链接：https://human3daigc.github.io/CartoonAlive_webpage/
- 代码链接：https://github.com/Human3DAIGC/CartoonAlive
- 首次记录日期：2026-06-29
- SD / LDM 关系：未确认。论文摘要强调 foundation models、分割、关键点和 Live2D blendshape 建模，未明确说明基于 Stable Diffusion / LDM。
- Live2D 关系：核心相关。论文明确从单张输入人像生成高质量、可表情驱动的 Live2D 数字人。
- 代码状态：官方仓库已公开，但当前更像项目材料/占位仓库；未发现完整推理、训练、数据处理或权重代码。
- 备注：论文 2025-07-23 公开，本次作为历史核心基线补录。它与 Textoon 互补，可作为 image-to-Live2D / portrait-to-Live2D 路线重点参考。

## 9. Visual Persona: Foundation Model for Full-Body Human Customization

- 标准标题：Visual Persona: Foundation Model for Full-Body Human Customization
- 别名：Visual Persona
- 论文链接：https://arxiv.org/abs/2503.15406
- 项目链接：https://cvlab-kaist.github.io/Visual-Persona/
- 代码链接：https://github.com/cvlab-kaist/Visual-Persona
- 首次记录日期：2026-07-06
- SD / LDM 关系：是扩散模型个性化 / 参考图条件生成路线；官方 README 明确基于 IP-Adapter，并提供 ControlNet 推理脚本。
- Live2D 关系：间接相关。不生成 Live2D 层或 rig，但对全身角色一致性、姿态控制、换装和 anime / character customization 有迁移价值。
- 代码状态：官方推理代码 + 预训练权重；未发现完整训练代码。
- 备注：历史补录，CVPR 2025。相关性 3/5，适合作为角色一致性和全身外观保持模块参考。

## 10. DreamShot: Personalized Storyboard Synthesis with Video Diffusion Prior

- 标准标题：DreamShot: Personalized Storyboard Synthesis with Video Diffusion Prior
- 别名：DreamShot
- 论文链接：https://arxiv.org/abs/2604.17195
- 项目链接：https://ll3rd.github.io/DreamShot/
- 代码链接：https://github.com/dihy16/DreamShot-Code
- 模型权重：https://huggingface.co/LL3RD/DreamShot
- 首次记录日期：2026-07-13
- SD / LDM 关系：不是 Stable Diffusion 主线；基于 video diffusion prior，README 提到可结合 LightX2V 4-step LoRA distillation 加速。
- Live2D 关系：间接相关。不生成 Live2D 层或绑定结构，但对多镜头角色一致性、参考角色身份保持和连续分镜素材生成有启发。
- 代码状态：官方推理代码 + 模型权重；数据集和训练代码尚未发布。
- 备注：论文 v2 于 2026-07-06 修订并标注 CVPR 2026 Highlight。相关性 3/5。
