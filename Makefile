install_dir = ${HOME}/.local/bin/
name = kadai

make:
	cd src/; zip -r ../${name}.zip *
	echo "#!/usr/bin/env python" | cat - ${name}.zip > ${name}

install:
	pip install tqdm Pillow colorthief
	install -D -m 700 ${name} ${install_dir}
	install -D -C -b -S .bak -m 700 examples/templates/colors.xresources ${HOME}/.local/share/${name}/templates/

clean:
	rm -f ${name}{,.zip}
	