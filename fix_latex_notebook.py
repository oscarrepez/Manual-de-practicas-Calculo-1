import json
import re

def fix_eqnarray(content):
    def replacer(match):
        inner = match.group(1).strip()
        
        # Si está vacío → eliminar
        if not inner:
            return ""
        
        return "$$\n\\begin{aligned}\n" + inner + "\n\\end{aligned}\n$$"

    content = re.sub(
        r"\\begin\{eqnarray\*\}(.*?)\\end\{eqnarray\*\}",
        replacer,
        content,
        flags=re.DOTALL
    )

    return content

def remove_empty_math(content):
    # Elimina bloques $$ vacíos
    content = re.sub(r"\$\$\s*\$\$", "", content)
    
    # Elimina aligned vacío
    content = re.sub(
        r"\$\$\s*\\begin\{aligned\}\s*\\end\{aligned\}\s*\$\$",
        "",
        content,
        flags=re.DOTALL
    )
    
    return content

def process_notebook(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            source = "".join(cell["source"])
            source = fix_eqnarray(source)
            source = remove_empty_math(source)
            cell["source"] = [source]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

    print(f"Notebook limpio guardado en: {output_file}")


# === USO ===
input_file = "practica1.ipynb"
output_file = "practica1_fixed2.ipynb"

process_notebook(input_file, output_file)