if python build.py; then
	cd build
	git add -A .
	git commit -m "Rebuild"
	git push
fi

