#!/bin/bash
set -e

# Create directories
mkdir -p /tmp/user_files/rare/components/tabs/account
mkdir -p /tmp/user_files/rare/components/tabs/downloads
mkdir -p /tmp/user_files/rare/components/tabs/library/details
mkdir -p /tmp/user_files/rare/models
mkdir -p /tmp/user_files/rare/shared/workers
mkdir -p /tmp/user_files/rare/widgets

# Download files
wget https://github.com/user-attachments/files/24425301/_version.py -O /tmp/user_files/_version.py
wget https://github.com/user-attachments/files/24425302/main.py -O /tmp/user_files/main.py
wget https://github.com/user-attachments/files/24425303/__init__.py -O /tmp/user_files/rare/__init__.py
wget https://github.com/user-attachments/files/24425304/__main__.py -O /tmp/user_files/rare/__main__.py
wget https://github.com/user-attachments/files/24425319/__init__.py -O /tmp/user_files/rare/components/__init__.py
wget https://github.com/user-attachments/files/24425325/__init__.py -O /tmp/user_files/rare/components/tabs/account/__init__.py
wget https://github.com/user-attachments/files/24425333/__init__.py -O /tmp/user_files/rare/components/tabs/downloads/__init__.py
wget https://github.com/user-attachments/files/24425335/details.py -O /tmp/user_files/rare/components/tabs/library/details/details.py
wget https://github.com/user-attachments/files/24425336/game_slim.py -O /tmp/user_files/rare/models/game_slim.py
wget https://github.com/user-attachments/files/24425354/install.py -O /tmp/user_files/rare/models/install.py
wget https://github.com/user-attachments/files/24425345/rare_core.py -O /tmp/user_files/rare/shared/rare_core.py
wget https://github.com/user-attachments/files/24425358/cloud_sync.py -O /tmp/user_files/rare/shared/workers/cloud_sync.py
wget https://github.com/user-attachments/files/24425366/side_tab.py -O /tmp/user_files/rare/widgets/side_tab.py
wget https://github.com/user-attachments/files/24425367/sliding_stack.py -O /tmp/user_files/rare/widgets/sliding_stack.py
wget https://github.com/user-attachments/files/24425368/__init__.py -O /tmp/user_files/rare/widgets/__init__.py
wget https://github.com/user-attachments/files/24425369/button_edit.py -O /tmp/user_files/rare/widgets/button_edit.py
wget https://github.com/user-attachments/files/24425370/collapsible_widget.py -O /tmp/user_files/rare/widgets/collapsible_widget.py
wget https://github.com/user-attachments/files/24425371/dialogs.py -O /tmp/user_files/rare/widgets/dialogs.py
wget https://github.com/user-attachments/files/24425372/elide_label.py -O /tmp/user_files/rare/widgets/elide_label.py
wget https://github.com/user-attachments/files/24425373/flow_layout.py -O /tmp/user_files/rare/widgets/flow_layout.py
wget https://github.com/user-attachments/files/24425374/image_widget.py -O /tmp/user_files/rare/widgets/image_widget.py
wget https://github.com/user-attachments/files/24425375/indicator_edit.py -O /tmp/user_files/rare/widgets/indicator_edit.py
wget https://github.com/user-attachments/files/24425377/library_layout.py -O /tmp/user_files/rare/widgets/library_layout.py
wget https://github.com/user-attachments/files/24425378/loading_widget.py -O /tmp/user_files/rare/widgets/loading_widget.py
wget https://github.com/user-attachments/files/24425379/rare_app.py -O /tmp/user_files/rare/widgets/rare_app.py
wget https://github.com/user-attachments/files/24425380/rare_style.py -O /tmp/user_files/rare/widgets/rare_style.py

echo "All files downloaded successfully."
