import subprocess
# 待修改路径：
robot_state_program_path="./get_robot_state"
move_forward_path=""
trun_left_path=""
turn_right_path=""
def get_robot_state():
    # 运行可执行文件，并捕获输出
    result = subprocess.run(
        [robot_state_program_path],  # 可执行文件路径
        capture_output=True,
        text=True
    )
    
    # 检查是否成功
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get robot state: {result.stderr}")
    
    # 解析输出
    output = result.stdout
    position = None
    quaternion = None
    
    for line in output.splitlines():
        if line.startswith("position:"):
            position = list(map(float, line.split(":")[1].strip().split(", ")))
        elif line.startswith("quaternion:"):
            quaternion = list(map(float, line.split(":")[1].strip().split(", ")))
    
    return position, quaternion

def control_move_forward():
    return_code = subprocess.call(move_forward_path)
    return return_code == 0  # True=成功，False=失败

def control_turn_left():
    return_code = subprocess.call(trun_left_path)
    return return_code == 0  # True=成功，False=失败

def control_turn_right():
    return_code = subprocess.call(turn_right_path)
    return return_code == 0  # True=成功，False=失败