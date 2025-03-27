# SLURM Batch Manager

SLURM 클러스터 환경에서 `.sh` 배치 스크립트를 자동으로 제출하고, 완료 여부를 모니터링하며, 실패 시 재시도하는 Python 기반의 간단한 유틸리티입니다.

이 도구는 다음 기능을 제공합니다:
- SLURM 작업 스크립트 자동 생성 (`#SBATCH` 옵션 포함)
- 작업 제출 (`sbatch`)
- 작업 상태 확인 (`squeue`, `sacct`)
- 실패 시 자동 재시도
- 로그 및 `.sh` 파일 자동 저장

---

## 📦 기능 요약

| 기능 | 설명 |
|------|------|
| `generate_sh_with_options` | 기존 `.sh` 파일에 `#SBATCH` 옵션을 삽입해 새로운 스크립트 생성 |
| `submit_job` | `sbatch` 명령어로 SLURM 작업 제출 |
| `is_job_running` | `squeue`를 통해 작업 실행 여부 확인 |
| `get_job_status` | `sacct`를 통해 작업 최종 상태 확인 |
| `run_batch` | 전체 프로세스 실행 (제출 → 대기 → 재시도 등)

---

## 🚀 사용 방법

### 기본 .sh 파일이 있을 때
```python
from slurm_manager.utils import run_batch

run_batch(
    script_path="base_script.sh",
    save_dir="runs/job_0326",
    sbatch_options={
        "job-name": "comsol_simulation",
        "partition": "all",
        "nodelist": "node32",
        "time": "10-40:00:00",
        "mem": "8G"
    },
    max_retries=3,
    wait_interval=30,
    verbose=True
)
```

### 함수를 실행하고 싶을 때 (인자가 없는 경우)

```python
from slurm_manager.utils import run_batch_with_function

script_path = "backbone.sh"

sbatch_options = {
    "partition": "all",
    "job-name": "comsol_job",
    "time": "10-40:00:00",
    "nodelist": "node32"
}

save_dir = "log/test_function"

run_batch_with_function(save_dir=save_dir, 
                        sbatch_options=sbatch_options, 
                        module_name="task",
                        function_name="main",
                        wait_interval=2,
                        verbose=True)
```

### 함수를 실행하고 싶을 때 (인자가 있는 경우)

```python
from slurm_manager.utils import run_batch_with_function

sbatch_options = {
    "partition": "all",
    "job-name": "comsol_job",
    "time": "10-40:00:00",
    "nodelist": "node32"
}

save_dir = "log/test_function_with_args"

function_args = {"path1" : "'task.txt'",
                 "path2" : "'task.txt'"}

run_batch_with_function(save_dir=save_dir, 
                        sbatch_options=sbatch_options, 
                        module_name="task",
                        function_name="read_txt",
                        function_args=function_args,
                        wait_interval=2,
                        max_retries=1,
                        verbose=True)
```


### 함수를 실행하고 싶을 때 (Python path 설정)

```python
from slurm_manager.utils import run_batch_with_function

sbatch_options = {
    "partition": "all",
    "job-name": "comsol_job",
    "time": "10-40:00:00",
    "nodelist": "node32"
}

save_dir = "log/test_function_with_args_python_path"

function_args = {"path1" : "'task.txt'",
                 "path2" : "'task.txt'"}

python_path = "your python path"

run_batch_with_function(save_dir=save_dir, 
                        sbatch_options=sbatch_options, 
                        module_name="task",
                        function_name="read_txt",
                        function_args=function_args,
                        python_path=python_path,
                        wait_interval=2,
                        max_retries=1,
                        verbose=True)
```
