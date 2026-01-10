import sys

def parse_list_file(input_path, output_path, default_policy="Direct"):
    """
    将 .list 文件转换为 Clash YAML 格式
    所有规则统一使用指定策略组（默认 Direct）
    注释行保留为 YAML 注释
    """
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    yaml_lines = ["payload:"]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("#"):
            yaml_lines.append(f"  {line}")
            continue

        # 自动识别规则类型
        if "/" in line:
            rule_type = "IP-CIDR"
        elif line.startswith("."):
            rule_type = "DOMAIN-SUFFIX"
            line = line.lstrip(".")
        elif "*" in line:
            rule_type = "DOMAIN-KEYWORD"
        else:
            rule_type = "DOMAIN"

        yaml_lines.append(f"  - {rule_type},{line},{default_policy}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))

    print(f"已生成 Clash 规则文件 → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python list_to_clash_yaml.py 输入.list 输出.yaml")
    else:
        parse_list_file(sys.argv[1], sys.argv[2])
