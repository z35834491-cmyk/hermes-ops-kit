# 克隆后运行 / Clone and run

克隆 Hermes Ops Kit 之后可以做什么。公开模板不连接真实基础设施。
What to do after cloning Hermes Ops Kit. The public template does not connect to real infrastructure.

## 1. 克隆 / Clone

```bash
git clone <REPO_URL> hermes-ops-kit
cd hermes-ops-kit
```

## 2. 跑公开模板检查 / Run public template checks

```bash
make check
```

会验证 Verifies:

- Python 脚本能编译 / scripts compile
- 没有被跟踪的私有 env-map / 凭据类文件 / no tracked private env-map or credential-like files
- 脱敏扫描通过 / sanitize scan passes
- JSON 模板合法 / JSON templates are valid
- 巡检骨架能生成 JSON/Markdown / inspection skeleton can generate JSON/Markdown
- onboard 能生成 env-map 候选 / onboarding can generate an env-map candidate
- env-map include 与 check catalog 对齐 / env-map include lists match the check catalog

`make check` **不会**检查本机正在运行的 Hermes。下面是可选模板，不是门禁：
`make check` does **not** inspect a running local Hermes. Optional template, not a gate:

```bash
make health-check
```

## 3. 创建私有 env-map / Create a private local env-map

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
```

只填本地路径、别名、凭据来源，不要填凭据值。
Fill only local paths, aliases, and credential sources. Do not put credential values in this file.

## 4. 跑巡检骨架 / Run the inspection skeleton

```bash
python3 scripts/validate_env_map.py config/env-map.local.yaml --expect-env test --catalog config/check-catalog.yaml
python3 scripts/inspect.py test --config config/env-map.local.yaml --catalog config/check-catalog.yaml --plan --json
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

公开模板不连接 Kubernetes、SSH、数据库或外部服务，只演示输出合同。
The public template does not connect to Kubernetes, SSH, databases, or external services. It only demonstrates the output contract.

预期本地产物 Expected local output:

```text
reports/test/inspection-<run_id>.json
reports/test/inspection-<run_id>.md
```

## 5. 生成 onboarding 候选 / Generate an onboarding candidate

```bash
python3 scripts/onboard.py --env test --output config/env-map.generated.yaml --force
```

生成文件只是候选。复制进 `env-map.local.yaml` 之前必须人工审阅。
The generated file is a candidate only. Review it manually before copying anything into `env-map.local.yaml`.

## 6. 可选 / Optional

```bash
python3 scripts/render_summary.py examples/inspection-result.example.json --only-abnormal
```

## 当前限制 / Current limitation

本仓库目前是模板/契约包。真实环境发现和真实巡检检查必须在私有 overlay 上、按 schema 安全实现。
This repository is a template/contract kit. Real discovery and real inspection checks must be implemented privately and safely on top of the schemas.
