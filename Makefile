all:
	uv run sloka_parser_flexible_format.py slokas.txt > data.js
	uv run --with cogapp cog -P template.html > index.html
	cp index.html dist/
