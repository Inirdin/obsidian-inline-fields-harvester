# Obsidian inline fields harvester 🌾🪚🚜
 🍝🍝🍝 Spaghetti code 🍝🍝🍝 Pasta served right from the OWEN

Janky scripts to batch process multiple files in [Obsidian](https://obsidian.md/) vault turning inline [Dataview](https://github.com/blacksmithgu/obsidian-dataview) fileds into Obsidan properties. Any `field:: Value, Value2` gets moved to the bottom of frontmatter and formated as:

```
field:
- Value
- Value2
or
field: value
```

## Usage
1. Change the `vaultLocation` (line 6) in `1_create_list.py`
2. Run the script
3. *(Optional) You can exclude files by removing them from `list.txt`*
4. Change the `vaultLocation` (line 6) in `2_inline_fields_harvester.py`
5. Run the script

The processed files will be created in subfolder and there will not be any change in your vault. Overwriting the files is in your own hands