"""Summarize Tableau workbook structure without exporting business records.

Portfolio review helper, not original competition code.
Usage: python inspect_workbook.py /path/to/workbook.twbx
Supports .twb or .twbx; prints structural JSON to stdout.
Only the TWB XML is read. Hyper extracts and image files are not opened.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


def inspect(path):
    path = Path(path)
    if path.suffix.lower() == ".twbx":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            workbooks = [n for n in names if n.lower().endswith(".twb")]
            if len(workbooks) != 1:
                raise ValueError("Expected exactly one TWB file in the package")
            root = ET.fromstring(archive.read(workbooks[0]))
            extract_count = sum(n.lower().endswith(".hyper") for n in names)
    elif path.suffix.lower() == ".twb":
        root = ET.parse(path).getroot()
        extract_count = None
    else:
        raise ValueError("Expected a .twb or .twbx file")

    all_sources = root.findall("datasources/datasource")
    sources = [s for s in all_sources if s.get("name") != "Parameters"]
    params = [s for s in all_sources if s.get("name") == "Parameters"]
    worksheets = {w.get("name"): w for w in root.findall("worksheets/worksheet")}

    dashboards = []
    for dashboard in root.findall("dashboards/dashboard"):
        sheet_names = sorted({
            zone.get("name") for zone in dashboard.findall(".//zone")
            if zone.get("name") in worksheets
        })
        dependencies = sorted({
            source.get("caption", source.get("name"))
            for name in sheet_names
            for source in worksheets[name].findall(".//datasource")
        })
        size = dashboard.find("size")
        dashboards.append({
            "name": dashboard.get("name"),
            "layout": dict(size.attrib) if size is not None else {},
            "worksheets": sheet_names,
            "data_sources": dependencies,
        })

    source_counts = [
        {
            "name": s.get("caption", s.get("name")),
            "calculated_columns": sum(
                c.find("calculation") is not None for c in s.findall("column")
            ),
        }
        for s in sources
    ]
    return {
        "review_type": "structural_xml_inspection",
        "business_records_exported": False,
        "worksheet_count": len(worksheets),
        "dashboard_count": len(dashboards),
        "business_data_source_count": len(sources),
        "embedded_hyper_file_count": extract_count,
        "source_defined_calculated_columns": sum(
            s["calculated_columns"] for s in source_counts
        ),
        "parameter_count": sum(len(s.findall("column")) for s in params),
        "all_xml_calculation_elements": len(root.findall(".//calculation")),
        "data_sources": source_counts,
        "dashboards": dashboards,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.workbook), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
