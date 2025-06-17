from core.computer import Computer

def main():
    """
    程序主函数。
    """
    # 1. 创建一台计算机
    computer = Computer()
    
    # 2. 定义要执行的程序 (来自实验指导书的监控程序)
    program_code = [0x44, 0x46, 0x98, 0x81, 0xF5, 0x0C, 0x00, 0x60]
    
    # 3. 将程序加载到内存
    computer.load_program(program_code)
    
    # 4. 预设外部输入设备的值
    computer.cpu.input_device_val = 0x0A

    # 5. 打印初始状态并开始运行
    print("--- Initial State ---")
    print(computer.get_full_status())
    print("\nRunning program...")

    # 6. 循环执行每一条宏指令
    for i in range(10):  # 设置一个最大指令数防止无限循环
        if computer.cpu.halted:
            print(f"\n--- HALTED after instruction {i} ---")
            break
        
        print(f"\n--- Executing Macro Instruction {i+1} (at PC=0x{computer.cpu.rf.PC.read():02X}) ---")
        computer.run_single_macro_step()
        print(computer.get_full_status())
    
    if not computer.cpu.halted:
        print("\nProgram finished or loop limit reached.")

if __name__ == '__main__':
    main()