def format_example(example):

    code = example["input"]
    family = example["family"]
    line = example["error_line"]
    col = example["error_col"]

    prompt = f"""repair_code
error_family: {family}
error_line: {line}
error_col: {col}

{code}
"""

    return {
        "input_text": prompt.strip(),
        "target_text": example["target"]
    }


def format_dataset(dataset):
    return [format_example(x) for x in dataset]