import os

def convert_list_to_clash_yaml(list_path):
    """
    将 Surge .list 文件转换为 Clash rule-provider YAML
    如果同名 .yaml 不存在，也会自动生成
    """
    yaml_path = os.path.splitext(list_path)[0] + ".yaml"

    with open(list_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    yaml_lines = ["payload:"]

    for raw_line in lines:
        line = raw_line.strip()

        # 跳过空行
        if not line:
            continue

        # 注释行完整保留
        if line.startswith("#"):
            yaml_lines.append(f"  {line}")
            continue

        rule_type = None
        value = None

        # Surge 标准语法：TYPE,VALUE[,POLICY]
        if "," in line:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2:
                rule_type = parts[0].upper()
                value = parts[1]
        else:
            # 兼容纯 list 写法
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

        # Clash rule-provider 支持的规则
        supported_rules = {
            "DOMAIN",
            "DOMAIN-SUFFIX",
            "DOMAIN-KEYWORD",
            "IP-CIDR",
            "IP-CIDR6",
            "GEOIP",
        }

        if rule_type not in supported_rules or not value:
            yaml_lines.append(f"  # 跳过不支持的 Surge 规则: {raw_line.strip()}")
            continue

        yaml_lines.append(f"  - {rule_type},{value}")

    # 写入 / 覆盖 yaml（不存在就创建，存在就更新）
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))

    print(f"✓ 生成 / 更新 Clash 规则集 → {yaml_path}")


def main():
    """
    遍历当前目录及子目录
    只要存在 .list，就确保同名 .yaml 一定存在
    """
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".list"):
                list_path = os.path.join(root, file)
                convert_list_to_clash_yaml(list_path)


if __name__ == "__main__":
    main()
