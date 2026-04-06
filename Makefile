template-Makefile:
	curl https://raw.githubusercontent.com/quintenroets/package-dev-tools/refs/heads/main/template-Makefile -o template-Makefile

include template-Makefile

integration-test:
	tests/integration-test.sh
