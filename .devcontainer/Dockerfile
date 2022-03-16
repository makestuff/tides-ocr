FROM debian
RUN apt-get update
RUN apt-get -y install --no-install-recommends python3 python3-dev python3-venv python3-pip git wget openssh-client nodejs imagemagick ghostscript
RUN useradd -c "VSCode User" -g 100 -m -N -s /bin/bash -u 1000 vscode
RUN pip3 install opencv-python-headless matplotlib jupyterlab
RUN sed -i 's#<policy domain="coder" rights="none" pattern="PDF" />#<policy domain="coder" rights="read|write" pattern="PDF" />#g' /etc/ImageMagick-6/policy.xml
