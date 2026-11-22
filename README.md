# workspace

2026 年秋季《软件工程课程设计》项目仓库。

## 项目定位

轻量级协作办公平台，主要包含：

- **个人工作区**：个人资料、文件、日程等，仅本人可管理。
- **共享工作区**：多人共同使用，可以共享资料、查看或安排日程。
- **资料存储**：上传、分类、查看、下载和管理文件。
- **日程管理**：创建日程、修改日程、查看日程，未来可能支持共享日程。

## 过程模型

采用**用例驱动的增量迭代**：Scrum 做迭代节奏，UP 的用例驱动做文档骨架，规格先行（SDD）做 AI 协作闸门。
完整论证见 [docs/01-charter/过程模型选型论证.md](docs/01-charter/过程模型选型论证.md)。

| 增量 | 范围 | 状态 |
|---|---|---|
| v0.1 | 个人工作区：账号、资料上传、个人日程 | 未开始 |
| v0.2 | 共享工作区：成员与权限、共享资料、共享日程 | 未开始 |
| v0.3 | 外部集成、通知提醒、审计与打磨 | 未开始 |

## 仓库结构

```
docs/          课程交付物，按 8 个知识单元编号组织（见 docs/README.md）
src/           应用源码
tests/         单元测试与集成测试
scripts/       仓库卫生检查等工具
.github/       CI、PR/Issue 模板
.githooks/     本地提交前检查
```

## 快速开始

```bash
git clone https://github.com/beigu-8-lyw/workspace.git
cd workspace
cp .env.example .env          # 填入本地配置，.env 不会入库
git config core.hooksPath .githooks && chmod +x .githooks/pre-commit
python3 scripts/check_repo.py  # 仓库卫生自检
```

## 协作规范

**main 禁止直推**，一律走 `分支 → PR → 他人 approve → 合并`。
细则见 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [docs/GitHub上传与提交规范.md](docs/GitHub上传与提交规范.md)。

## 交付物索引

| # | 交付物 | 位置 |
|---|---|---|
| ① | 项目章程（含选型论证） | [docs/01-charter/](docs/01-charter/) |
| ② | 需求规约与变更记录 | [docs/02-requirements/](docs/02-requirements/) |
| ③ | 需求分析模型包 | [docs/03-models/](docs/03-models/) |
| ④ | 设计规约与评审单 | [docs/04-design/](docs/04-design/) |
| ⑤ | 代码仓库（含 CI 与评审记录） | 本仓库 |
| ⑥ | 测试计划与报告 | [docs/05-test/](docs/05-test/) |
| ⑦ | 迭代计划与回顾 | [docs/06-iteration/](docs/06-iteration/) |
| ⑧ | 部署系统与演示脚本 | [docs/08-deploy/](docs/08-deploy/) |
| ⑨ | AI 使用报告 | [docs/07-ai/](docs/07-ai/) |
| ⑩ | 组内贡献度互评表 | [docs/06-iteration/](docs/06-iteration/) |
