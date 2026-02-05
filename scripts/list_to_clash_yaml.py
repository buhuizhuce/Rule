import os

def convert_list_to_clash_yaml(list_path):
    """
    将单个 Surge .list 文件转换为 Clash rule-provider YAML
    输出到同目录、同文件名，仅后缀改为 .yaml
    """
    yaml_path = os.path.splitext(list_path)[0] + ".yaml"

    with open(list_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    yaml_lines = ["payload:"]

    for raw_line in lines:
        line = raw_line.strip()

        # 空行
        if not line:
            continue

        # 注释行（完整保留）
        if line.startswith("#"):
            yaml_lines.append(f"  {line}")
            continue

        # 如果是 Surge 标准语法（带逗号），只取第一个参数
        # 如：DOMAIN,example.com,Proxy
        if "," in line:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2:
                rule_type = parts[0].upper()
                value = parts[1]
            else:
                continue
        else:
            # 兼容“纯 list”写法
            value = line
            if "/" in value:
                rule_type = "IP-CIDR"
            elif value.startswith("."):
                rule_type = "DOMAIN-SUFFIX"
                value = value.lstrip(".")
            elif "*" in value:
                rule_type = "DOMAIN-KEYWORD"
                value = value.replace("*", "")
            else:
                rule_type = "DOMAIN"

        # 仅输出 Clash 常用可识别规则
        supported = {
            "DOMAIN",
            "DOMAIN-SUFFIX",
            "DOMAIN-KEYWORD",
            "IP-CIDR",
            "IP-CIDR6",
            "GEOIP",
        }

        if rule_type not in supported:
            yaml_lines.append(f"  # 跳过不支持的 Surge 规则: {raw_line.strip()}")
            continue

        yaml_lines.append(f"  - {rule_type},{value}")

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))

    print(f"生成 Clash 规则集 → {yaml_path}")


def main():
    """
    遍历当前目录及子目录下所有 .list 文件
    并在同目录生成对应的 .yaml
    """
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".list"):
                list_path = os.path.join(root, file)
                convert_list_to_clash_yaml(list_path)


if __name__ == "__main__":
    main()
