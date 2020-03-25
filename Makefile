.PHONY: deploy

deploy:
	cd deploy && ansible_playbook ansible.yml -i hosts -k -K -c paramiko
