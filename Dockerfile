FROM amancevice/pandas:0.23.4-python3

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install argparse \
                synapseclient \
                git+https://github.com/larssono/bridgeclient.git \
                git+https://github.com/Sage-Bionetworks/synapsebridgehelpers
RUN git clone https://github.com/Sage-Bionetworks/biaffect-cirrhosis /root/biaffect-cirrhosis
