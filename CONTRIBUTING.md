# 贡献指南 (Contributing Guide)

感谢你愿意为 **Awesome AI Projects** 做出贡献！本项目致力于收录优质、活跃且具实用价值的开源 AI 项目与工程工具。

---

## 收录标准

在提交项目前，请确保项目满足以下要求：

1. **开源且有活跃度**：仓库具有明确的开源协议，近期有持续维护或更新。
2. **文档完备**：仓库包含清晰的 README、快速上手指南或 Demo。
3. **定位清晰**：在所属分类（如 Agent 编排、RAG、推理引擎等）中有代表性或独特的工程价值。
4. **拒绝纯导流/广告**：不收录空壳项目、未实现的商业引流项目。

---

## 提交格式规范

请严格遵循以下 Markdown 格式新增条目：

```markdown
- [owner/repo](https://github.com/owner/repo) ![GitHub Stars](https://img.shields.io/github/stars/owner/repo?style=social) - 一句话精炼介绍（建议 30 字以内，清晰说明核心功能与特色）。
```

### 示例

```markdown
- [multica-ai/multica](https://github.com/multica-ai/multica) ![GitHub Stars](https://img.shields.io/github/stars/multica-ai/multica?style=social) - 开源的多 Agent 协作与项目管理平台，支持将多种编程 Agent 接入任务看板。
```

---

## 提交 PR 流程

1. **Fork** 本仓库到你的 GitHub 账号。
2. **新建分支**：`git checkout -b feat/add-project-name`。
3. **编辑内容**：
   - 将项目添加到 [README.md](README.md) 中最合适的分类下。
   - 保持同类目下条目排版整齐规范。
   - 若属于新分类，请同步更新目录（TOC）。
4. **提交并推送**：
   ```bash
   git commit -m "feat(scope): add <owner/repo>"
   git push origin feat/add-project-name
   ```
5. **创建 Pull Request**：
   - 简要说明推荐该项目的理由及亮点。
   - 每次 PR 建议只添加 1~3 个同类项目，便于快速 review 与合并。

---

再次感谢你对开源社区的贡献！
