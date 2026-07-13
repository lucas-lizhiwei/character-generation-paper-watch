# 待人工确认候选

更新日期：2026-07-13

## 1. LPM 1.0: Video-based Character Performance Model

- 链接：
  - https://arxiv.org/abs/2604.07823
  - https://github.com/large-performance-model/large-performance-model.github.io
- 疑点：
  - 偏角色表演视频生成，不是 2D / Live2D 分层建模。
  - GitHub 仓库更像项目主页仓库，尚未确认是否会放出正式代码。
- 后续确认方向：
  - 若后续放出真正推理 / 训练代码，可作为“可动画化角色”支线保留。

## 2. AniGen: Unified S^3 Fields for Animatable 3D Asset Generation

- 链接：
  - https://arxiv.org/abs/2604.08746
  - https://github.com/VAST-AI-Research/AniGen
- 疑点：
  - 明确是 3D animatable asset generation，不直接面向动漫 2D / Live2D。
- 后续确认方向：
  - 关注其 rig-aware representation 是否可迁移到 2D / 2.5D 可驱动角色表示。

## 3. DreamCoser: Controllable Layered 3D Character Generation and Editing

- 链接：
  - https://cic.tju.edu.cn/faculty/likun/projects/DreamCoser/index.html
  - https://github.com/liam6699/DreamCoser
- 疑点：
  - “分层 + 可编辑”很贴近主线，但目标是 3D 角色。
  - GitHub 仓库为空，代码尚未真正发布。
- 后续确认方向：
  - 等待正式代码、更多实验材料或后续扩展工作。

## 4. Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition

- 链接：
  - https://arxiv.org/abs/2512.15603
  - https://github.com/QwenLM/Qwen-Image-Layered
- 疑点：
  - 通用图像分层模型，不是角色 / 动漫 / Live2D 专用。
  - 公开时间较早，不属于本周新增；但近期 MRT、See-through 生态都将其作为重要对照或相关路线。
- 后续确认方向：
  - 判断是否作为“通用分层图像基线”正式纳入主索引。
  - 若纳入，需明确标注不支持 Live2D 自动绑定，不应误报为 Text-to-Live2D。

## 5. Live2D / AI VTuber 工具仓库集合

- 链接：
  - https://github.com/topics/ai-waifu
- 疑点：
  - 搜索中出现大量 LLM + TTS/STT + Live2D 渲染项目，多数只加载现有 Live2D 模型并控制表情或口型。
  - 不生成角色图像、分层素材、绑定结构或 Live2D 模型。
- 后续确认方向：
  - 除非项目加入自动角色生成、图层分解、自动 rigging 或模型生成，否则不纳入主索引。

## 6. AvatarMix: Identity-Preserving Cross-Avatar Composition for Outfit Personalization

- 链接：
  - https://arxiv.org/abs/2606.03506
  - https://larsph.github.io/avatarmix/
- 疑点：
  - 2026-06-02 新公开，时间上属于本周，但核心目标是 3D Gaussian avatar outfit personalization。
  - 论文使用局部 diffusion refinement 维护头发/脖颈接缝和服装外观，对“角色身份保持 + 服装替换”有启发，但不是 2D / Live2D / 动漫角色生成。
- 后续确认方向：
  - 若后续代码开放，可观察其 head/body compositional editing 是否可迁移为 2D 角色部件级换装或分层编辑思路。

## 7. Anime-Ready: Controllable 3D Anime Character Generation with Body-Aligned Component-Wise Garment Modeling

- 链接：
  - https://openreview.net/forum?id=BRoAjhYWoQ
- 疑点：
  - ICLR 2026 Poster，公开时间早于本周；方向是 text / image to animation-ready 3D anime character。
  - 它明确面向动漫角色、component-wise garment、skeleton 与 facial expression control，但不是 2D / Live2D 分层素材生成。
- 后续确认方向：
  - 可作为“动漫角色结构化部件建模 / 可动画化角色表示”的 3D 参考，不应误报为 Text-to-Live2D。

## 8. Stretchy Studio

- 链接：
  - https://github.com/MangoLion/stretchystudio
  - https://editor.stretchy.studio
- 疑点：
  - 它是 FOSS 2D animation / auto-rigging 工具，不是论文或生成模型。
  - README 明确面向 See-through 输出的 PSD，并提供自动 rig、mesh deformation、shape keys、Spine export 等制作功能。
- 后续确认方向：
  - 判断是否需要建立“工具链项目”索引；它对验证 See-through -> 可动画角色闭环很有价值，但不应与论文条目混在一起。

## 9. Lip Forcing: Few-Step Autoregressive Diffusion for Real-time Lip Synchronization

- 链接：
  - https://arxiv.org/abs/2606.11180
  - https://cvlab-kaist.github.io/LipForcing/
- 疑点：
  - 2026-06-09 新公开，属于本周窗口。
  - 方向是 V2V lip synchronization / talking avatar 加速，不生成角色、不做分层建模，也不是动漫或 Live2D 专用。
  - 项目页有 Code 入口，但本轮未确认正式 GitHub 代码是否已可用。
- 后续确认方向：
  - 若代码开放且能支持任意 2D / 动漫头像的实时口型驱动，可作为 Live2D 数字人驱动支线保留；否则仅作为 talking avatar 加速参考。

## 10. AnimaSpark: A Feed-Forward Method for Animating Arbitrary 3D Objects

- 链接：
  - https://arxiv.org/abs/2606.10988
- 疑点：
  - 2026-06-09 新公开，提出从 rigged static 3D model 渲染多层 mesh / skeleton 表示，再用视频生成模型与关键点跟踪恢复 3D 动画。
  - 目标是 3D 物体 / 角色动画，不是 2D / Live2D，也没有面向动漫角色或 Stable Diffusion 角色生成。
- 后续确认方向：
  - 仅在其“多层渲染表示 + 2D 视频运动估计 + 动画回写”思路可迁移到 2.5D / Live2D 驱动时继续跟踪。

## 11. FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining

- 链接：
  - https://arxiv.org/abs/2606.20506
  - https://github.com/Blue2Giant/FreeStyle
  - https://blue2giant.github.io/FreeStyle/
- 疑点：
  - 2026-06-18 新公开，官方仓库已包含 LoRA data pipeline、benchmark inference、model inference、数据集、benchmark、模型权重和 LoRA metadata。
  - 方向是通用 style-content dual-reference generation，不是角色 / 动漫 / Live2D 专用。
  - 相关性评分约 2/5，按规则不进入“新发现”。
- 后续确认方向：
  - 判断其 community LoRA mining 和 content/style reference triplets 是否可迁移到角色身份保持、角色换装、发型/服装/风格分离控制。

## 12. Avatar V: Scaling Video-Reference Avatar Video Generation

- 链接：
  - https://arxiv.org/abs/2606.13872
  - https://www.heygen.com/research/avatar-v-model
- 疑点：
  - arXiv 提交日期为 2026-06-11，不属于本周严格窗口；上轮未纳入记录。
  - 偏视频参考 talking avatar / 商业数字人生成，不是 2D / Live2D / 动漫角色分层建模。
  - 未找到公开代码或模型权重。
- 后续确认方向：
  - 若后续发布代码、权重或可用于 2D / stylized avatar 的条件控制模块，可作为数字人驱动支线记录。

## 13. Cinematic Compositing Using Character-Environment-Harmonized Video Generation Models

- 链接：
  - https://arxiv.org/abs/2606.20233
- 疑点：
  - 2026-06-17 公开，主要处理绿幕角色与环境视频的物理交互、光照协调和道具替换。
  - 不生成角色，不做动漫 / Live2D / 分层角色建模。
- 后续确认方向：
  - 仅在研究生成角色素材与场景合成、光照/接触一致性时作为间接参考。

## 14. Vera: A Layered Diffusion Model for Content-Preserving Video Editing

- 链接：
  - https://arxiv.org/abs/2606.23610
  - https://huggingface.co/datasets/netflix/Vera-Layered-Video-Dataset
- 疑点：
  - 2026-06-22 公开，提出生成 edit layer + alpha matte 的分层视频编辑框架，并发布 layered video dataset。
  - 不是角色 / 动漫 / Live2D 专用；主要目标是通用视频内容保持编辑。
  - 相关性评分约 2/5，按规则不进入“新发现”。
- 后续确认方向：
  - 关注是否开源代码。
  - 判断其 edit layer / alpha matte 机制是否可迁移到角色服装、发型、表情等局部图层编辑。

## 15. L2MAS: Live2D Multi-Agent Animation System

- 链接：
  - https://github.com/XucroYuri/L2MAS
- 疑点：
  - 2026-06-27 有仓库更新，是 Live2D 多智能体动画原型，不是论文或新生成模型。
  - README 提到 Textoon、Live2D Cubism、ComfyUI、FFmpeg 和 `model.live2d.generate` 能力接口，但当前状态仍描述为 mock MVP + local FFmpeg smoke path。
  - 相关性评分约 2/5，偏工程编排工具。
- 后续确认方向：
  - 确认是否真的接入可用 Textoon / image-to-Live2D provider。
  - 如果后续提供可运行的 Text-to-Live2D 自动化流水线，可作为工具链项目单列追踪。

## 16. NanoLive2D / Open Avatar

- 链接：
  - https://github.com/GBSOSS/nano-live2d
  - https://avatar.gbase.ai/
- 疑点：
  - 使用 Gemini API 对既有 Live2D texture atlas 做服装替换，支持文本描述和参考服装图。
  - 不生成新的 Live2D 模型、分层素材或绑定结构，也没有论文。
  - 相关性评分约 2/5，适合作为“已有 rig 下的纹理 / 服装编辑”工程线索。
- 后续确认方向：
  - 检查它是否能稳定保持 atlas 布局和 rig 兼容性。
  - 判断是否可替换为 Stable Diffusion / IP-Adapter / LoRA / ControlNet 工作流。

## 17. ContextAnyone: Context-Aware Diffusion for Character-Consistent Text-to-Video Generation

- 链接：
  - https://arxiv.org/abs/2512.07328
  - https://github.com/ziyang1106/ContextAnyone
- 疑点：
  - 论文提交于 2025-12-08，不是本周新论文。
  - 方向是 reference-guided character-consistent text-to-video，不是动漫或 Live2D 专用。
  - 官方仓库目前只有 “Coming soon” 和 arXiv 链接，尚无实际代码。
- 后续确认方向：
  - 等待正式代码、权重或 demo。
  - 如果其 reference-aware DiT 机制能迁移到动漫角色或 Live2D 后续动画，可提升优先级。

## 18. Go-with-the-Track: Video Compositing and Motion Control with Point Tracking

- 链接：
  - https://arxiv.org/abs/2606.20891
  - https://eyeline-labs.github.io/Go-with-the-Track/
- 疑点：
  - SIGGRAPH 2026 工作，核心是 reference-anchored point tracks 的视频合成和运动控制。
  - 不生成角色、不做 Live2D / 分层角色建模。
  - 对角色素材合成、参考主体运动控制有间接价值，相关性评分约 2/5。
- 后续确认方向：
  - 关注是否开源。
  - 判断其多参考合成和点轨迹控制是否能用于动漫角色素材与镜头运动控制。

## 19. Anime2.5DRig

- 链接：
  - https://github.com/852wa/Anime2.5DRig
  - https://852wa.github.io/Anime2.5DRig/
- 疑点：
  - 第三方浏览器自动 rig 工具，不是论文或生成模型。
  - 不做单图分层，主要接收 See-through 等工具输出的分层 PSD。
- 后续确认方向：
  - 测试 See-through / Textoon 输出 PSD 的兼容性。
  - 确认是否能导出 Live2D Cubism，或仅在自有 WebGL runtime 中运行。

## 20. Paper Doll Studio

- 链接：
  - https://github.com/Khurramali1997/paper-doll-studio
- 疑点：
  - 本地化 anime paper doll / wardrobe 工具链，不是论文。
  - 使用 See-through 19 类 anime SAM、SD 1.5 anime inpainting、IP-Adapter、ControlNet-ready reference pack 等组件，方向接近部件级服装编辑，但不生成 Live2D rig。
- 后续确认方向：
  - 判断是否单列工具链索引。
  - 验证 per-garment generation 与 naked-body invariant 是否适合 Text-to-Live2D 部件编辑实验。

## 21. Outline and Detail: A Semantic-Driven Framework for Layered 2D Character Generation

- 链接：
  - https://dl.acm.org/doi/10.1145/3746059.3747707
  - https://www.milab.design/team-2/sun-qirui
- 疑点：
  - UIST 2025 论文，方向高度贴近 layered 2D character generation。
  - 本轮未找到开放全文、项目页、代码或模型权重，无法确认是否使用 SD / LDM 或是否支持 Live2D 可绑定结构。
- 后续确认方向：
  - 获取论文全文。
  - 确认方法是否输出可编辑图层、是否支持自动 rig、是否与 Text2AC / Textoon 有技术关联。

## 22. SyncCache: Exploiting Asymmetric Dynamics for Fast Audio-Driven Portrait Animation

- 链接：
  - https://arxiv.org/abs/2606.30849
- 疑点：
  - ECCV 2026，偏 DiT-based audio-driven portrait animation 加速，不生成角色或 Live2D 层。
  - 相关性评分约 2/5。
- 后续确认方向：
  - 关注是否开源。
  - 判断其 spatially-asymmetric caching 是否能迁移到 Live2D / talking avatar 的实时驱动或后处理。

## 23. FacePlex: Full-Duplex Joint Speech-Facial Motion Generation for Conversational Avatars

- 链接：
  - https://arxiv.org/abs/2606.30145
  - https://hahminlew.github.io/FacePlex/
- 疑点：
  - 偏 conversational avatar / facial motion，不是动漫角色生成或 Live2D 建模。
  - 相关性评分约 2/5。
- 后续确认方向：
  - 关注是否开源。
  - 判断 rolling flow matching / rolling cross-attention 是否可用于 Live2D 数字人的实时口型与表情控制。

## 24. InterTalk: Towards Flexible, Natural, Efficient Interaction for Conversational Talking Face Generation

- 链接：
  - https://arxiv.org/abs/2606.31088
- 疑点：
  - ECCV 2026，支持多轮、多参与者 talking face generation，但不是角色建模或 Live2D。
  - 相关性评分约 2/5。
- 后续确认方向：
  - 关注是否开源。
  - 判断多参与者 motion feedback 是否可用于多 Live2D 角色对话驱动。

## 25. GaussianEmoTalker: Real-Time Emotional Talking Head Synthesis with Audio-Driven and Blendshape-Based 3D Gaussian Splatting

- 链接：
  - https://arxiv.org/abs/2607.00959
  - https://njust-yang.github.io/GaussianEmoTalker/
- 疑点：
  - 3D Gaussian Splatting talking head，不是 2D / Live2D / anime 角色生成。
  - 相关性评分约 2/5。
- 后续确认方向：
  - 关注是否开源。
  - 判断 emotion-conditioned residual deformation 是否能启发 Live2D 表情参数和情绪强度控制。

## 26. Vidu S1: A Real-Time Interactive Video Generation Model

- 链接：
  - https://arxiv.org/abs/2607.03118
  - https://github.com/shengshu-ai/Vidu-S1
  - https://vidu.com/vidu-stream
- 疑点：
  - 支持上传动漫风格角色图并用语音实时控制数字角色视频，但不是角色建模、分层生成或 Live2D。
  - GitHub 仓库主要是 README、文档和试玩入口，未发现本地推理 / 训练代码或模型权重。
- 后续确认方向：
  - 若后续开放可本地运行的模型、权重或训练/推理代码，可作为实时 interactive avatar 支线继续跟踪。

## 27. DreamCharacter-1: From 3D Generative Foundation Models to Product-Ready Character Generation

- 链接：
  - https://arxiv.org/abs/2607.07817
  - https://dreamcharacter-x.github.io
- 疑点：
  - 2026-07-08 新提交，但目标是 3D production-ready character asset generation。
  - 未找到公开代码或权重；与 2D / Live2D / 动漫分层角色生成没有直接关系。
- 后续确认方向：
  - 关注其 geometry / texture post-adaptation 是否可迁移到 2D / 2.5D 角色素材质量提升。

## 28. Live2D Automation MCP Server

- 链接：
  - https://github.com/J621111/live2d-automation
- 疑点：
  - README 描述单图到 mock intermediate Live2D package 的工程流程，但明确说明导出不是 production-ready Live2D runtime model。
  - `ready_for_cubism_editor` 仍为 false，最终验证和导出仍依赖 Cubism Editor。
- 后续确认方向：
  - 确认是否真正接入可用分层模型、真实 Cubism 导出和可生产 rigging；若只是 PoC，不纳入主索引核心条目。
