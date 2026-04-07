config/template-Makefile:
<<<<<<< HEAD
	curl --create-dirs https://raw.githubusercontent.com/quintenroets/package-dev-tools/refs/heads/main/config/template-Makefile -o config/template-Makefile

include config/template-Makefile

integration-test:
	tests/integration-test.sh
=======
	curl https://raw.githubusercontent.com/quintenroets/package-dev-tools/refs/heads/main/config/template-Makefile --create-dirs -o config/template-Makefile

include config/template-Makefile
>>>>>>> template
