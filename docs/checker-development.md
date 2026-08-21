<p align="right">
  <b>简体中文</b> · <a href="checker-development.en.md">English</a>
</p>

# Checker 开发

Hermes Ops Kit 的 checker 是小插件，为巡检报告产出 `CheckResult`。

## 公开 vs 私有

公开仓 checker 必须保持安全：不调 Kubernetes API、不 SSH、不连数据库、不读凭据值、不做写入/修复。

`inspect.py` 会跳过 `inspection.exclude` 中的检查，以及 catalog `component` 在 env-map 里为 `mode=disabled` 的检查。Checker 不必再实现这层过滤。

公开 `run()` 在没有注入 `runner` 时不得调用 kubectl / SSH / 数据库。解析逻辑可用假 runner 做单元测试。私有部署可以替换成真实只读实现。

## 文件

```text
scripts/checkers/base.py
scripts/checkers/k8s.py
scripts/checkers/mysql.py
scripts/checkers/redis.py
scripts/checkers/rabbitmq.py
scripts/checkers/elasticsearch.py
```

## 合同

```python
def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False, runner=None) -> CheckResult:
    ...
```

返回 `CheckResult`（`id` / `component` / `status` / `severity` / `title` / `evidence` / `suggestion`）。

## 增加检查项

1. 写入 `config/check-catalog.yaml`
2. 加入对应模块的 `SUPPORTED`
3. 返回 `CheckResult`
4. 有用的话补脱敏 runbook 示例
5. 跑 `make check`

## 安全

- L0 只读可以不审批
- 任何写、重启、删除、扩缩、patch、外写都不属于 checker，应走审批/执行流
- 公开示例保持通用、脱敏
