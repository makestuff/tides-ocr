FROM debian
RUN apt-get update
RUN apt-get -y install --no-install-recommends python3 python3-venv wget imagemagick ghostscript
RUN useradd -c "VSCode User" -g 100 -m -N -s /bin/bash -u 1000 vscode
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install pytz opencv-python-headless matplotlib jupyterlab
RUN pip install pandas scipy
RUN sed -i 's#</policymap>#  <policy domain="coder" rights="read|write" pattern="PDF" />\n</policymap>#g;s#<policy domain="resource" name="disk" value="2GiB"/>#<policy domain="resource" name="disk" value="8GiB"/>#g' /etc/ImageMagick-7/policy.xml
