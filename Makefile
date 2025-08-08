# Install uv first before running this: the build command could be:
#     curl -LsSf https://astral.sh/uv/install.sh | sh && make
all:
	uv run slokas_parse.py slokas.txt > data.js
	uv run --with cogapp cog -P template.html > dist/index.html
