# 实际命令与结果

调用器：`python output/run_compilation.py`；工作目录为本任务目录。以下命令由调用器以 subprocess 参数数组真实运行；所有 CLI 操作的 cwd 均为当前提供的 `h3-model-protocol`。完整命令、参数、stdout/stderr 路径和退出码也见 `command-log.json`。

M11.4 的退出码 2 是实际预期阻塞。没有为其伪造提案，也没有将错误输出当作成功提案接受。各 stderr 文件均为空；诊断由 stdout 的结构化 JSON 返回。

## 00-help — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py --help
```

stdout：`logs/00-help.stdout.txt`（443 bytes）；stderr：`logs/00-help.stderr.txt`（0 bytes）。

## 11-route — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py route /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-1-request.json
```

stdout：`logs/11-route.stdout.txt`（809 bytes）；stderr：`logs/11-route.stderr.txt`（0 bytes）。

## 12-propose — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py propose /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-1-request.json
```

stdout：`logs/12-propose.stdout.txt`（8220 bytes）；stderr：`logs/12-propose.stderr.txt`（0 bytes）。

## 13-check — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py check /workspace/scratch/9caa7b23478d/m11-forward-use/output/proposals/m11-1-proposal.json --request /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-1-request.json
```

stdout：`logs/13-check.stdout.txt`（830 bytes）；stderr：`logs/13-check.stderr.txt`（0 bytes）。

## 21-route — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py route /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-2-request.json
```

stdout：`logs/21-route.stdout.txt`（859 bytes）；stderr：`logs/21-route.stderr.txt`（0 bytes）。

## 22-propose — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py propose /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-2-request.json
```

stdout：`logs/22-propose.stdout.txt`（19989 bytes）；stderr：`logs/22-propose.stderr.txt`（0 bytes）。

## 23-check — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py check /workspace/scratch/9caa7b23478d/m11-forward-use/output/proposals/m11-2-proposal.json --request /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-2-request.json
```

stdout：`logs/23-check.stdout.txt`（830 bytes）；stderr：`logs/23-check.stderr.txt`（0 bytes）。

## 31-route — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py route /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-3-request.json
```

stdout：`logs/31-route.stdout.txt`（859 bytes）；stderr：`logs/31-route.stderr.txt`（0 bytes）。

## 32-propose — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py propose /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-3-request.json
```

stdout：`logs/32-propose.stdout.txt`（63877 bytes）；stderr：`logs/32-propose.stderr.txt`（0 bytes）。

## 33-check — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py check /workspace/scratch/9caa7b23478d/m11-forward-use/output/proposals/m11-3-proposal.json --request /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-3-request.json
```

stdout：`logs/33-check.stdout.txt`（830 bytes）；stderr：`logs/33-check.stderr.txt`（0 bytes）。

## 41-route — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py route /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-4-request.json
```

stdout：`logs/41-route.stdout.txt`（859 bytes）；stderr：`logs/41-route.stderr.txt`（0 bytes）。

## 42-propose-blocked — exit 2

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py propose /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/m11-4-request.json
```

stdout：`logs/42-propose-blocked.stdout.txt`（513 bytes）；stderr：`logs/42-propose-blocked.stderr.txt`（0 bytes）。

## 50-accept — exit 0

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/9caa7b23478d/m11-forward-use/h3-model-protocol/scripts/m11_contract.py accept /workspace/scratch/9caa7b23478d/m11-forward-use/output/proposals/accepted-proposals.json --requests /workspace/scratch/9caa7b23478d/m11-forward-use/output/requests/accepted-requests.json --state /workspace/scratch/9caa7b23478d/m11-forward-use/output/state-empty.json
```

stdout：`logs/50-accept.stdout.txt`（257818 bytes）；stderr：`logs/50-accept.stderr.txt`（0 bytes）。
