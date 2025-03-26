import subprocess
import re
import time
import os

def format_sbatch_options(options_dict):
    """
    주어진 딕셔너리를 #SBATCH 형식 문자열 리스트로 변환합니다.
    
    Parameters:
        options_dict (dict): sbatch에 사용할 옵션들
    
    Returns:
        list[str]: --key=value 형식의 문자열 리스트
    """
    return [f"#SBATCH --{key}={value}" for key, value in options_dict.items()]

def submit_job(script_path):
    """
    주어진 배치 스크립트를 sbatch로 제출하고 작업 ID를 반환합니다.
    
    Parameters:
        script_path (str): SLURM 작업 스크립트 경로
        options (dict or None): sbatch 명령어에 사용할 옵션 (기본값: None)
    
    Returns:
        str or None: 작업 ID (실패 시 None)
    """
    
    sbatch_cmd = ["sbatch", script_path]

    result = subprocess.run(sbatch_cmd, capture_output=True, text=True)

    # 실패 시 에러 메시지 출력 추가
    if result.returncode != 0:
        print("[Error] sbatch execution failed.")
        print("STDOUT:", result.stdout.strip())
        print("STDERR:", result.stderr.strip())

    match = re.search(r'Submitted batch job (\d+)', result.stdout)
    return match.group(1) if match else None

def is_job_running(job_id):
    """
    주어진 작업 ID가 현재 실행 중인지 확인합니다.
    
    Parameters:
        job_id (str): SLURM 작업 ID
    
    Returns:
        bool: 실행 중이면 True, 아니면 False
    """
    result = subprocess.run(["squeue", "--job", job_id], capture_output=True, text=True)
    return job_id in result.stdout

def get_job_status(job_id):
    """
    작업이 완료된 후 최종 상태를 반환합니다.
    
    Parameters:
        job_id (str): SLURM 작업 ID
    
    Returns:
        str or None: 작업 상태(COMPLETED, FAILED 등), 찾을 수 없으면 None
    """
    result = subprocess.run(
        ["sacct", "-j", job_id, "--format=JobID,State", "--parsable2", "--noheader"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().splitlines()
    for line in lines:
        parts = line.split('|')
        if parts[0] == job_id:
            return parts[1]
    return None

def generate_sh_with_options(original_script, output_path, options_dict):
    """
    sbatch 옵션을 포함한 새로운 .sh 스크립트를 생성
    
    Parameters:
        original_script (str): 기존 .sh 경로
        output_path (str): 생성될 .sh 경로
        options_dict (dict): sbatch 옵션들
    """
    with open(original_script, 'r') as f:
        original_lines = f.readlines()

    sbatch_lines = format_sbatch_options(options_dict)
    new_lines = []

    for line in original_lines:
        if line.startswith("#!"):  # 첫 줄은 유지
            new_lines.append(line)
        elif line.startswith("#SBATCH"):
            continue  # 기존 SBATCH는 제거
        else:
            break

    # 나머지 스크립트 본문 추가
    start_idx = len(new_lines)
    body_lines = original_lines[start_idx:]

    # 최종 구성
    with open(output_path, 'w') as f:
        f.writelines(new_lines)
        f.write('\n')
        for sb in sbatch_lines:
            f.write(sb + '\n')
        f.write('\n')
        f.writelines(body_lines)
        
def run_batch(script_path, save_dir, sbatch_options=None, max_retries=3, wait_interval=10, verbose=True):
    """
    작업 제출 후 완료까지 대기하며, 실패 시 재시도. save_dir이 지정되면 해당 디렉토리에 스크립트 및 로그 저장.
    
    Parameters:
        script_path (str): 실행할 .sh 스크립트 경로
        save_dir (str): 저장 디렉토리 경로
        sbatch_options (dict): sbatch 옵션 딕셔너리
        max_retries (int): 최대 재시도 횟수
        wait_interval (int): 상태 확인 주기 (초)  
        verbose (bool): 상태 출력 여부
    """
    # 저장 디렉토리 준비
    os.makedirs(save_dir, exist_ok=True)

    # 로그 경로도 save_dir로 설정
    log_path = os.path.join(save_dir, "%A.log")
    sbatch_options["output"] = log_path

    # 새로운 .sh 파일 생성
    script_name = os.path.basename(script_path)
    new_script_path = os.path.join(save_dir, script_name)
    generate_sh_with_options(script_path, new_script_path, sbatch_options)
    script_path = new_script_path

    attempt = 0
    while attempt < max_retries:
        print(f"[Attempt {attempt + 1}] Submitting job...")
        job_id = submit_job(script_path)
        if not job_id:
            print("Job submission failed.")
            return

        print(f"Job ID {job_id} submitted. Waiting for completion...")

        while is_job_running(job_id):
            if verbose:
                print(f"Job is still running... Waiting {wait_interval} seconds")
            time.sleep(wait_interval)

        status = get_job_status(job_id)
        print(f"Job status: {status}")

        if status == "COMPLETED":
            print("Job completed successfully.")
            return
        else:
            print(f"Job failed or ended unexpectedly ({status}). Retrying...")
            attempt += 1

    print("Maximum retry limit exceeded. Job failed.")
