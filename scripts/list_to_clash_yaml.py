import sys

def parse_list_file(input_path, output_path):
    """
    将 .list 文件转换为 Clash YAML 格式
    输出为纯规则集，不包含策略组名
    注释行保留为 YAML 注释
    """
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    yaml_lines = ["payload:"]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 注释行
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

        # 纯规则，不带策略组
        yaml_lines.append(f"  - {rule_type},{line}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))

    print(f"已生成 Clash 规则文件 → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python list_to_clash_yaml.py 输入.list 输出.yaml")
    else:
        parse_list_file(sys.argv[1], sys.argv[2])
