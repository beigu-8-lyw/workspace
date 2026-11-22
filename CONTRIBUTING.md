# 协作规范

完整版见 [docs/GitHub上传与提交规范.md](docs/GitHub上传与提交规范.md)。这里只放必须记住的几条。

## 四条铁律

1. **不在仓库里发生的事，视为没有发生。** 文件传上去不算数，走完 PR 才算。
2. **main 禁止直推。** 一律 `分支 → PR → 他人 approve → 合并`。
3. **一张图一个 PR。** 图必须交 PlantUML/Mermaid 源文件 + 导出图，只贴 PR 评论不算入库。
4. **中间产物不入库。** PDF 解析文本、临时导出、`__pycache__`、演示视频一律排除。

## 日常流程

```bash
gh issue create ...                      # 1. 先建 Issue
git switch main && git pull --ff-only
git switch -c docs/uc03-usecase          # 2. 拉分支
git add <文件>                            # 3. 只加该加的
python scripts/check_repo.py             # 4. 本地过一遍卫生检查
git commit -m "docs(model): add UC-03 use case diagram (#12)"
git push -u origin docs/uc03-usecase     # 5. 推分支
gh pr create --fill                      # 6. 发 PR，描述写 Closes #12
gh pr merge --squash --delete-branch     # 7. 评审通过后合并
```

## 分支命名

`feat/` 功能 · `docs/` 文档与模型 · `fix/` 缺陷 · `test/` 测试 · `chore/` 配置

## 提交信息

`<类型>(<范围>): <做了什么> (#Issue)`

```
docs(model): add UC-03 use case diagram (#12)
feat(auth): add OAuth2 callback handler (#21)
fix(acl): deny cross-workspace read on shared files (#34)
```

禁止：`update`、`修改`、`111`、`最终版`。

## 提交前自检

```bash
python scripts/check_repo.py   # 必须输出 ✓
git diff --cached              # 确认没有 .env / 密钥 / 中间文件
```

可选：装成本地钩子，提交时自动拦截

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

## 目录约定

```
docs/01-charter/       项目章程、选型论证
docs/02-requirements/  SRS、访谈纪要、变更记录
docs/03-models/        用例图 / 类图 / 状态图（.puml + 导出图）
docs/04-design/        概要设计、详细设计、评审单
docs/05-test/          测试计划、用例、报告
docs/06-iteration/     迭代计划、回顾报告
docs/07-ai/            AI 使用报告、关卡记录
docs/08-deploy/        部署说明、演示脚本
```
