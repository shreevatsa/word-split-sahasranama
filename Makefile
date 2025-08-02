all:
	uv run sloka_parser_flexible_format.py slokas.txt > data.js
	uv tool run cog -P template.html > index.html
