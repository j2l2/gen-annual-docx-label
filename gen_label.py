"""_summary_
"""

import subprocess
import sys
import zipfile
from argparse import ArgumentParser, ArgumentTypeError, Namespace, SUPPRESS

from lxml import etree

from special_days import SpecialDays




def get_options() -> Namespace:
    """Parse CLI arguments."""

    def validate_year(value: str) -> int:
        try:
            ivalue = int(value)
        except ValueError as exc:
            raise ArgumentTypeError(f"{value} 不是有效的年份") from exc
        if ivalue < 1900 or ivalue > 2100:
            raise ArgumentTypeError(f"{value} 不是有效的年份，請輸入 1900 到 2100 之間的數字。")
        return ivalue

    argparser = ArgumentParser(
        epilog="版權所有 © 2024 崇華聖道院"
    )
    argparser.add_argument("year", type=validate_year, help="產生年份，介於 1900 到 2100 之間")
    argparser.add_argument(
        "--start",
        type=int,
        default=1,
        help="從第幾個標籤位置開始列印 (1-based，預設 1)",
    )
    argparser.add_argument(
        "--preview",
        action="store_true",
        default=False,
        help="產生後開啟文件進行預覽/列印",
    )
    argparser.add_argument("--DEBUG", action="store_true", default=False, help=SUPPRESS)

    return argparser.parse_args()

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": WORD_NS}


def _field_name(instr: str) -> str | None:
    parts = instr.replace('"', " ").split()
    if len(parts) >= 2 and parts[0].upper() == "MERGEFIELD":
        return parts[1]
    return None


def _set_complex_field_result(runs: list[etree._Element], value: str) -> None:
    text_nodes: list[etree._Element] = []
    for run in runs:
        text_nodes.extend(run.xpath(".//w:t", namespaces=NS))
    if text_nodes:
        text_nodes[0].text = value
        text_nodes[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        for extra in text_nodes[1:]:
            extra.text = ""
    elif runs:
        text_node = etree.SubElement(runs[0], f"{{{WORD_NS}}}t")
        text_node.text = value
        text_node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


def merge_label_records(template_path: str, records: list[dict[str, str]], output_path: str) -> None:
    """Fill a Next Record label template with records in document order."""
    with zipfile.ZipFile(template_path) as zin:
        parts = {name: zin.read(name) for name in zin.namelist()}

    document_xml = parts.get("word/document.xml")
    if document_xml is None:
        raise ValueError("Template missing word/document.xml")

    root = etree.fromstring(document_xml)
    record_idx = 0

    # Handle simple fields.
    for fld in root.xpath("//w:fldSimple", namespaces=NS):
        instr = fld.get(f"{{{WORD_NS}}}instr", "")
        instr_upper = instr.upper()

        if "NEXT" in instr_upper.split() and "MERGEFIELD" not in instr_upper:
            record_idx += 1
            parent = fld.getparent()
            if parent is not None:
                parent.remove(fld)
            continue

        name = _field_name(instr)
        if name is None:
            continue

        value = ""
        if 0 <= record_idx < len(records):
            value = str(records[record_idx].get(name, ""))

        text_nodes = fld.xpath(".//w:t", namespaces=NS)
        if text_nodes:
            text_nodes[0].text = value
            for extra in text_nodes[1:]:
                extra.text = ""
        else:
            run = etree.SubElement(fld, f"{{{WORD_NS}}}r")
            text_node = etree.SubElement(run, f"{{{WORD_NS}}}t")
            text_node.text = value

    # Handle complex fields.
    record_idx = 0
    nodes = list(root.iter())
    i = 0
    while i < len(nodes):
        node = nodes[i]
        if node.tag != f"{{{WORD_NS}}}fldChar":
            i += 1
            continue
        fld_type = node.get(f"{{{WORD_NS}}}fldCharType", "")
        if fld_type != "begin":
            i += 1
            continue

        begin_run = node.getparent()
        if begin_run is None:
            i += 1
            continue

        instr_parts: list[str] = []
        separate_run = None
        end_run = None
        j = i + 1
        while j < len(nodes):
            n = nodes[j]
            if n.tag == f"{{{WORD_NS}}}instrText":
                instr_parts.append(n.text or "")
            elif n.tag == f"{{{WORD_NS}}}fldChar":
                n_type = n.get(f"{{{WORD_NS}}}fldCharType", "")
                if n_type == "separate":
                    separate_run = n.getparent()
                elif n_type == "end":
                    end_run = n.getparent()
                    break
            j += 1

        instr = "".join(instr_parts).strip()
        instr_upper = instr.upper()

        if "NEXT" in instr_upper.split() and "MERGEFIELD" not in instr_upper:
            record_idx += 1
            if end_run is not None and begin_run.getparent() is end_run.getparent():
                parent = begin_run.getparent()
                children = list(parent)
                try:
                    b_idx = children.index(begin_run)
                    e_idx = children.index(end_run)
                    for r in children[b_idx : e_idx + 1]:
                        parent.remove(r)
                except ValueError:
                    pass
            i = j + 1
            continue

        name = _field_name(instr)
        if name is not None and separate_run is not None and end_run is not None:
            value = ""
            if 0 <= record_idx < len(records):
                value = str(records[record_idx].get(name, ""))

            parent = separate_run.getparent()
            if parent is not None and parent is end_run.getparent():
                children = list(parent)
                try:
                    s_idx = children.index(separate_run)
                    e_idx = children.index(end_run)
                    result_runs = children[s_idx + 1 : e_idx]
                    _set_complex_field_result(result_runs, value)
                except ValueError:
                    pass

        i = j + 1

    parts["word/document.xml"] = etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in parts.items():
            zout.writestr(name, data)


def gen_label(args: Namespace) -> bool:
    """Generate one label per special day entry."""
    try:
        if args.start < 1:
            raise ValueError("--start 必須大於或等於 1")

        special_days = [
            {
                "name": s_day.name,
                "etiquette": s_day.etiquette,
            }
            for s_day in SpecialDays
        ]
        blanks = [{"name": "", "etiquette": ""} for _ in range(args.start - 1)]
        records = blanks + special_days

        output_path = f"仙佛紀念日標籤-{args.year}.docx"
        merge_label_records("標籤-5167.docx", records, output_path)
        if args.DEBUG:
            print(f"start={args.start}, blanks={len(blanks)}, records={len(records)}")
        if args.preview:
            subprocess.run(["open", output_path], check=True)
        return True

    except Exception as e:
        print(f"產生標籤失敗: {e}")
        return False

def main() -> None:
    """CLI entry point."""
    args = get_options()
    if args.DEBUG:
        for arg in vars(args):
            print(arg, getattr(args, arg))
    if not gen_label(args):
        sys.exit(1)


if __name__ == "__main__":
    main()