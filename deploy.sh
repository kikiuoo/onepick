#!/bin/bash

./upload_to_git.sh

ssh -X -i ksnpick.cer -t ubuntu@3.35.16.229 "cd /home/ubuntu/picktalk/ && ./download_from_git.sh && ./update_db.sh && exit ; bash"
