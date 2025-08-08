# Install uv first before running this: the build command could be:
#     curl -LsSf https://astral.sh/uv/install.sh | sh && make
all:
	uv run slokas_parse.py slokas.txt > data.js
	npx tailwindcss@3.4.17 -i tailwind.input.css -o dist/tailwind.3.4.17.css --minify --content template.html
	uv run --with cogapp cog -P template.html > dist/index.html
	rm dist/tailwind.3.4.17.css
