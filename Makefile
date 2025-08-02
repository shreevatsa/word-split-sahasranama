# Install uv first before running this: the build command could be:
#     curl -LsSf https://astral.sh/uv/install.sh | sh && make
all:
	uv run sloka_parser_flexible_format.py slokas.txt > data.js
	uv run --with cogapp cog -P template.html > dist/index.html
